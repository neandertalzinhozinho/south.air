//! host — Host VST3 **somente leitura** do oráculo da etapa I.
//!
//! CLI: `host <plugin.vst3> <in.wav> <out.wav> [blocos]`
//!
//! O que este programa faz, e só isso:
//!   1. `LoadLibraryW` no plugin (nenhum patch, nenhum hook, nenhuma injeção);
//!   2. `GetProcAddress("GetPluginFactory")` e chamada da factory VST3;
//!   3. enumera as classes da factory e escolhe a de categoria `Audio Module Class`;
//!   4. `createInstance` -> `IComponent` + `IAudioProcessor`;
//!   5. `initialize` -> `setupProcessing` -> `setActive(true)` -> `setProcessing(true)`;
//!   6. processa o WAV inteiro em blocos e grava um WAV float32 estéreo.
//!
//! Honestidade: toda chamada COM é registrada com ordem, endereço e RVA relativo ao
//! módulo. Se qualquer passo falhar, o programa aborta **antes** de gravar o WAV de
//! saída e imprime o HRESULT simbólico exato. Nunca grava silêncio como se fosse
//! sucesso.
//!
//! Convenções de ABI (x86_64-windows):
//!   * `PLUGIN_API` do SDK VST3 é `__stdcall`, que em x64 é a ABI padrão do
//!     Windows -> `extern "system"` (idêntico a `extern "C"` aqui).
//!   * `COM_COMPATIBLE` é 1 no Windows no SDK: os TUIDs são gravados no layout
//!     **GUID/COM** (Data1 LE32, Data2 = parte alta de l2 LE16, Data3 = parte
//!     baixa de l2 LE16, Data4 big-endian) e os `tresult` são HRESULTs COM
//!     (`kResultFalse` = `S_FALSE` = 0x00000001). Ver NOTAS.md.
//!
//! Esta é a única dependência do crate além de `std`: a FFI declarada no fim do
//! arquivo (kernel32).

#![allow(non_snake_case)]

use std::env;
use std::ffi::{c_void, OsStr};
use std::fs;
use std::io::Write;
use std::os::windows::ffi::OsStrExt;
use std::ptr;
use std::sync::atomic::{AtomicU32, AtomicUsize, Ordering};

// ---------------------------------------------------------------------------
// Resultados / HRESULTs do VST3 no Windows (COM_COMPATIBLE = 1)
// ---------------------------------------------------------------------------

type Hr = i32; // tresult

const K_RESULT_OK: Hr = 0x0000_0000; // kResultOk == kResultTrue == S_OK
const K_RESULT_FALSE: Hr = 0x0000_0001; // S_FALSE
const K_NO_INTERFACE: Hr = 0x8000_4002u32 as Hr; // E_NOINTERFACE
const K_INVALID_ARGUMENT: Hr = 0x8007_0057u32 as Hr; // E_INVALIDARG
const K_NOT_IMPLEMENTED: Hr = 0x8000_4001u32 as Hr; // E_NOTIMPL
const K_INTERNAL_ERROR: Hr = 0x8000_4005u32 as Hr; // E_FAIL
const K_NOT_INITIALIZED: Hr = 0x8000_FFFFu32 as Hr; // E_UNEXPECTED
const K_OUT_OF_MEMORY: Hr = 0x8007_000Eu32 as Hr; // E_OUTOFMEMORY

fn hr_name(hr: Hr) -> &'static str {
    match hr {
        K_RESULT_OK => "kResultOk/kResultTrue (S_OK)",
        K_RESULT_FALSE => "kResultFalse (S_FALSE)",
        K_NO_INTERFACE => "kNoInterface (E_NOINTERFACE)",
        K_INVALID_ARGUMENT => "kInvalidArgument (E_INVALIDARG)",
        K_NOT_IMPLEMENTED => "kNotImplemented (E_NOTIMPL)",
        K_INTERNAL_ERROR => "kInternalError (E_FAIL)",
        K_NOT_INITIALIZED => "kNotInitialized (E_UNEXPECTED)",
        K_OUT_OF_MEMORY => "kOutOfMemory (E_OUTOFMEMORY)",
        _ => "HRESULT desconhecido",
    }
}

// ---------------------------------------------------------------------------
// Constantes VST3 usadas
// ---------------------------------------------------------------------------

const MEDIA_TYPE_AUDIO: i32 = 0; // Vst::kAudio
const BUS_DIR_INPUT: i32 = 0; // Vst::kInput
const BUS_DIR_OUTPUT: i32 = 1; // Vst::kOutput

const SYMBOLIC_SAMPLE_32: i32 = 0; // Vst::kSample32
const PROCESS_MODE_REALTIME: i32 = 0; // Vst::kRealtime
const PROCESS_MODE_OFFLINE: i32 = 2; // Vst::kOffline

/// TUID a partir de 4 palavras de 32 bits no layout **GUID/COM** que o SDK usa
/// no Windows (`COM_COMPATIBLE = 1`):
///   Data1 = l1 em little-endian (4 B), Data2 = (l2>>16) em LE (2 B),
///   Data3 = (l2&0xFFFF) em LE (2 B), Data4 = l3,l4 em big-endian (4+4 B).
///
/// É exatamente o que `INLINE_UID` do `funknown.h` expande. Confirmado neste
/// binário por desmontagem: `initialize` consulta `IHostApplication` com os
/// bytes `cc95e558 2ddb6949 8b6aaf8c 36a664e5` e o `queryInterface` compara
/// `IPluginBase` com `db8d8822 6e15ae45 8358b348 08190625`. Ver NOTAS.md.
const fn tuid(l1: u32, l2: u32, l3: u32, l4: u32) -> [u8; 16] {
    let a = l1.to_le_bytes();
    let b = ((l2 >> 16) as u16).to_le_bytes();
    let c = ((l2 & 0xFFFF) as u16).to_le_bytes();
    let d = l3.to_be_bytes();
    let e = l4.to_be_bytes();
    [
        a[0], a[1], a[2], a[3], b[0], b[1], c[0], c[1], d[0], d[1], d[2], d[3], e[0], e[1], e[2],
        e[3],
    ]
}

/// `FUnknown` = IUnknown do COM: 00000000-0000-0000-C000-000000000046
const IID_FUNKNOWN: [u8; 16] = tuid(0x00000000, 0x00000000, 0xC0000000, 0x00000046);

/// `Steinberg::IPluginBase` = 22888DDB-156E-45AE-8358-B34808190625
#[allow(dead_code)]
const IID_IPLUGINBASE: [u8; 16] = tuid(0x22888DDB, 0x156E45AE, 0x8358B348, 0x08190625);

/// `Vst::IComponent` = E831FF31-F2D5-4301-928E-BBEE25697802
const IID_ICOMPONENT: [u8; 16] = tuid(0xE831FF31, 0xF2D54301, 0x928EBBEE, 0x25697802);

/// `Vst::IAudioProcessor` = 42043F99-B7DA-453C-A569-E79D9AAEC33D
const IID_IAUDIOPROCESSOR: [u8; 16] = tuid(0x42043F99, 0xB7DA453C, 0xA569E79D, 0x9AAEC33D);

/// `Vst::IHostApplication` = 58E595CC-DB2D-4969-8B6A-AF8C36A664E5
const IID_IHOSTAPPLICATION: [u8; 16] = tuid(0x58E595CC, 0xDB2D4969, 0x8B6AAF8C, 0x36A664E5);

// ---------------------------------------------------------------------------
// Placar de chamadas / log
// ---------------------------------------------------------------------------

static CALL_SEQ: AtomicU32 = AtomicU32::new(0);
/// Profundidade de aninhamento: o plugin chama de volta IHostApplication durante
/// `initialize`, então as chamadas internas são indentadas para não se misturar.
static DEPTH: AtomicU32 = AtomicU32::new(0);
static MODULE_BASE: AtomicUsize = AtomicUsize::new(0);
static MODULE_SIZE: AtomicUsize = AtomicUsize::new(0);

fn flush_out() {
    let _ = std::io::stdout().flush();
}

/// Escreve uma linha de diagnóstico (sempre com flush, para sobreviver a crash).
fn say(msg: &str) {
    println!("{msg}");
    flush_out();
}

fn indent() -> String {
    let d = DEPTH.load(Ordering::Relaxed).min(8) as usize;
    "  ".repeat(d)
}

fn rva_suffix(addr: usize) -> String {
    let base = MODULE_BASE.load(Ordering::Relaxed);
    let size = MODULE_SIZE.load(Ordering::Relaxed);
    if base != 0 && addr >= base && addr < base + size {
        format!("  rva=+0x{:X}", addr - base)
    } else {
        String::new()
    }
}

/// Registra a intenção de chamar `label`; o resultado é impresso numa linha
/// seguinte e indentada, de modo que callbacks aninhados (IHostApplication)
/// não se misturem com a chamada externa.
fn log_call(label: &str, fnaddr: usize) {
    let n = CALL_SEQ.fetch_add(1, Ordering::Relaxed) + 1;
    println!(
        "{}[{n:02}] {label:<46} fn=0x{fnaddr:X}{}",
        indent(),
        rva_suffix(fnaddr)
    );
    flush_out();
}

fn log_hr(hr: Hr) {
    println!("{}     -> {:<28} (0x{:08X})", indent(), hr_name(hr), hr as u32);
    flush_out();
}

/// Resultado de uma chamada que não devolve HRESULT (contagem, latência, ponteiro).
fn log_value(msg: &str) {
    println!("{}     -> {msg}", indent());
    flush_out();
}

/// Loga a chamada, executa, loga o HRESULT. Devolve o HRESULT.
fn call0(label: &str, fnaddr: usize, f: impl FnOnce() -> Hr) -> Hr {
    log_call(label, fnaddr);
    DEPTH.fetch_add(1, Ordering::Relaxed);
    let hr = f();
    DEPTH.fetch_sub(1, Ordering::Relaxed);
    log_hr(hr);
    hr
}

/// Como `call0`, mas para métodos que devolvem um valor simples (contagem,
/// latência, ponteiro) em vez de um HRESULT. Não formata esses valores como
/// se fossem HRESULT — o `countClasses` devolve 3, não `S_FALSE`.
fn call_value<T>(
    label: &str,
    fnaddr: usize,
    f: impl FnOnce() -> T,
    fmt: impl FnOnce(&T) -> String,
) -> T {
    log_call(label, fnaddr);
    DEPTH.fetch_add(1, Ordering::Relaxed);
    let v = f();
    DEPTH.fetch_sub(1, Ordering::Relaxed);
    log_value(&fmt(&v));
    v
}

fn fail(msg: &str) -> ! {
    println!();
    println!("!!! FALHA: {msg}");
    flush_out();
    std::process::exit(1);
}

// ---------------------------------------------------------------------------
// Estruturas C do VST3
// ---------------------------------------------------------------------------

#[repr(C)]
#[derive(Clone, Copy)]
struct ProcessSetup {
    process_mode: i32,
    symbolic_sample_size: i32,
    max_samples_per_block: i32,
    sample_rate: f64,
}

#[repr(C)]
#[derive(Clone, Copy)]
struct AudioBusBuffers {
    num_channels: i32,
    silence_flags: u64,
    channel_buffers32: *mut *mut f32,
}

impl Default for AudioBusBuffers {
    fn default() -> Self {
        AudioBusBuffers {
            num_channels: 0,
            silence_flags: 0,
            channel_buffers32: ptr::null_mut(),
        }
    }
}

#[repr(C)]
struct ProcessData {
    process_mode: i32,
    symbolic_sample_size: i32,
    num_samples: i32,
    num_inputs: i32,
    num_outputs: i32,
    inputs: *mut AudioBusBuffers,
    outputs: *mut AudioBusBuffers,
    input_parameter_changes: *mut c_void,
    output_parameter_changes: *mut c_void,
    input_events: *mut c_void,
    output_events: *mut c_void,
    process_context: *mut c_void,
}

#[repr(C)]
struct PFactoryInfo {
    vendor: [u8; 64],
    url: [u8; 256],
    email: [u8; 128],
    flags: i32,
}

#[repr(C)]
struct PClassInfo {
    cid: [u8; 16],
    cardinality: i32,
    category: [u8; 32],
    name: [u8; 64],
}

#[repr(C)]
struct BusInfo {
    media_type: i32,
    bus_direction: i32,
    channel_count: i32,
    name: [u16; 128],
    bus_type: i32,
    flags: u32,
}

// ---------------------------------------------------------------------------
// Vtables (ordem exata do SDK; 0..3 é FUnknown)
// ---------------------------------------------------------------------------

#[repr(C)]
struct FUnknownVtbl {
    query_interface: unsafe extern "system" fn(*mut c_void, *const u8, *mut *mut c_void) -> Hr,
    add_ref: unsafe extern "system" fn(*mut c_void) -> u32,
    release: unsafe extern "system" fn(*mut c_void) -> u32,
}

#[repr(C)]
struct FactoryVtbl {
    base: FUnknownVtbl,
    get_factory_info: unsafe extern "system" fn(*mut c_void, *mut PFactoryInfo) -> Hr,
    count_classes: unsafe extern "system" fn(*mut c_void) -> i32,
    get_class_info: unsafe extern "system" fn(*mut c_void, i32, *mut PClassInfo) -> Hr,
    create_instance:
        unsafe extern "system" fn(*mut c_void, *const u8, *const u8, *mut *mut c_void) -> Hr,
}

/// `IComponent` (inclui `IPluginBase`).
#[repr(C)]
struct ComponentVtbl {
    base: FUnknownVtbl,
    initialize: unsafe extern "system" fn(*mut c_void, *mut c_void) -> Hr,
    terminate: unsafe extern "system" fn(*mut c_void) -> Hr,
    get_controller_class_id: unsafe extern "system" fn(*mut c_void, *mut u8) -> Hr,
    set_io_mode: unsafe extern "system" fn(*mut c_void, i32) -> Hr,
    get_bus_count: unsafe extern "system" fn(*mut c_void, i32, i32) -> i32,
    get_bus_info: unsafe extern "system" fn(*mut c_void, i32, i32, i32, *mut BusInfo) -> Hr,
    get_routing_info: unsafe extern "system" fn(*mut c_void, *mut c_void, *mut c_void) -> Hr,
    activate_bus: unsafe extern "system" fn(*mut c_void, i32, i32, i32, u8) -> Hr,
    set_active: unsafe extern "system" fn(*mut c_void, u8) -> Hr,
    set_state: unsafe extern "system" fn(*mut c_void, *mut c_void) -> Hr,
    get_state: unsafe extern "system" fn(*mut c_void, *mut c_void) -> Hr,
}

/// `IAudioProcessor`.
#[repr(C)]
struct ProcessorVtbl {
    base: FUnknownVtbl,
    set_bus_arrangements:
        unsafe extern "system" fn(*mut c_void, *mut u64, i32, *mut u64, i32) -> Hr,
    get_bus_arrangement: unsafe extern "system" fn(*mut c_void, i32, i32, *mut u64) -> Hr,
    can_process_sample_size: unsafe extern "system" fn(*mut c_void, i32) -> Hr,
    get_latency_samples: unsafe extern "system" fn(*mut c_void) -> u32,
    setup_processing: unsafe extern "system" fn(*mut c_void, *mut ProcessSetup) -> Hr,
    set_processing: unsafe extern "system" fn(*mut c_void, u8) -> Hr,
    process: unsafe extern "system" fn(*mut c_void, *mut ProcessData) -> Hr,
    get_tail_samples: unsafe extern "system" fn(*mut c_void) -> u32,
}

unsafe fn vt_factory(obj: *mut c_void) -> *const FactoryVtbl {
    *(obj as *const *const FactoryVtbl)
}
unsafe fn vt_component(obj: *mut c_void) -> *const ComponentVtbl {
    *(obj as *const *const ComponentVtbl)
}
unsafe fn vt_processor(obj: *mut c_void) -> *const ProcessorVtbl {
    *(obj as *const *const ProcessorVtbl)
}

// ---------------------------------------------------------------------------
// Helpers de FUnknown
// ---------------------------------------------------------------------------

unsafe fn release(obj: *mut c_void, label: &str) {
    if obj.is_null() {
        return;
    }
    let vt = *(obj as *const *const FUnknownVtbl);
    let f = (*vt).release;
    call_value(label, f as usize, || f(obj), |n| {
        format!("refs restantes={n}")
    });
}

unsafe fn add_ref(obj: *mut c_void, label: &str) {
    if obj.is_null() {
        return;
    }
    let vt = *(obj as *const *const FUnknownVtbl);
    let f = (*vt).add_ref;
    call_value(label, f as usize, || f(obj), |n| format!("refs={n}"));
}

/// `queryInterface` com a assinatura VST3 (`const TUID`, `void**`).
unsafe fn query_interface(
    obj: *mut c_void,
    iid: &[u8; 16],
    label: &str,
) -> Result<*mut c_void, Hr> {
    let vt = *(obj as *const *const FUnknownVtbl);
    let f = (*vt).query_interface;
    let mut out: *mut c_void = ptr::null_mut();
    let hr = call0(label, f as usize, || f(obj, iid.as_ptr(), &mut out));
    if hr == K_RESULT_OK && !out.is_null() {
        Ok(out)
    } else {
        Err(hr)
    }
}

// ---------------------------------------------------------------------------
// IHostApplication mínimo (contexto obrigatório de `initialize`)
// ---------------------------------------------------------------------------

#[repr(C)]
struct HostVtbl {
    query_interface: unsafe extern "system" fn(*mut c_void, *const u8, *mut *mut c_void) -> Hr,
    add_ref: unsafe extern "system" fn(*mut c_void) -> u32,
    release: unsafe extern "system" fn(*mut c_void) -> u32,
    get_name: unsafe extern "system" fn(*mut c_void, *mut u16) -> Hr,
    create_instance:
        unsafe extern "system" fn(*mut c_void, *const u8, *const u8, *mut *mut c_void) -> Hr,
}

#[repr(C)]
struct HostObj {
    vtbl: *const HostVtbl,
    refs: AtomicU32,
}

static HOST_VTBL: HostVtbl = HostVtbl {
    query_interface: host_query_interface,
    add_ref: host_add_ref,
    release: host_release,
    get_name: host_get_name,
    create_instance: host_create_instance,
};

// O objeto vive em memória estática e só é usado na thread principal; o
// compilador exige `Sync` porque é um `static`, não porque haja concorrência.
unsafe impl Sync for HostObj {}
unsafe impl Send for HostObj {}

static HOST_OBJ: HostObj = HostObj {
    vtbl: &HOST_VTBL,
    refs: AtomicU32::new(1),
};

unsafe extern "system" fn host_query_interface(
    this: *mut c_void,
    iid: *const u8,
    out: *mut *mut c_void,
) -> Hr {
    let this = &*(this as *const HostObj);
    log_call("IHostApplication::queryInterface", host_query_interface as *const () as usize);
    if out.is_null() {
        log_hr(K_INVALID_ARGUMENT);
        return K_INVALID_ARGUMENT;
    }
    let iid = std::slice::from_raw_parts(iid, 16);
    let known = iid == IID_FUNKNOWN || iid == IID_IHOSTAPPLICATION;
    if known {
        this.refs.fetch_add(1, Ordering::Relaxed);
        *out = this as *const HostObj as *mut c_void;
        log_hr(K_RESULT_OK);
        K_RESULT_OK
    } else {
        *out = ptr::null_mut();
        log_hr(K_NO_INTERFACE);
        K_NO_INTERFACE
    }
}

unsafe extern "system" fn host_add_ref(this: *mut c_void) -> u32 {
    let this = &*(this as *const HostObj);
    let n = this.refs.fetch_add(1, Ordering::Relaxed) + 1;
    log_call("IHostApplication::addRef", host_add_ref as *const () as usize);
    log_value(&format!("refs={n}"));
    n
}

unsafe extern "system" fn host_release(this: *mut c_void) -> u32 {
    let this = &*(this as *const HostObj);
    let n = this.refs.fetch_sub(1, Ordering::Relaxed) - 1;
    log_call("IHostApplication::release", host_release as *const () as usize);
    log_value(&format!("refs={n}"));
    n
}

unsafe extern "system" fn host_get_name(_this: *mut c_void, name: *mut u16) -> Hr {
    log_call("IHostApplication::getName", host_get_name as *const () as usize);
    let s: Vec<u16> = "soultree-host-oracle\0".encode_utf16().collect();
    if !name.is_null() {
        ptr::copy_nonoverlapping(s.as_ptr(), name, s.len().min(128));
    }
    log_hr(K_RESULT_OK);
    K_RESULT_OK
}

unsafe extern "system" fn host_create_instance(
    _this: *mut c_void,
    _cid: *const u8,
    _iid: *const u8,
    out: *mut *mut c_void,
) -> Hr {
    // Não implementamos IMessage/IAttributeList: o host é somente leitura e
    // só processa áudio. Reportamos a ausência em vez de fingir sucesso.
    log_call("IHostApplication::createInstance", host_create_instance as *const () as usize);
    if !out.is_null() {
        *out = ptr::null_mut();
    }
    log_hr(K_NOT_IMPLEMENTED);
    K_NOT_IMPLEMENTED
}

// ---------------------------------------------------------------------------
// WAV
// ---------------------------------------------------------------------------

struct WavIn {
    sample_rate: u32,
    channels: u16,
    frames: usize,
    /// Amostras intercaladas, já em f32 e já em estéreo (mono é duplicado).
    samples: Vec<f32>,
}

fn rd_u16(b: &[u8], o: usize) -> u16 {
    u16::from_le_bytes([b[o], b[o + 1]])
}
fn rd_u32(b: &[u8], o: usize) -> u32 {
    u32::from_le_bytes([b[o], b[o + 1], b[o + 2], b[o + 3]])
}

fn read_wav(path: &OsStr) -> Result<WavIn, String> {
    let data = fs::read(path).map_err(|e| format!("não foi possível ler o WAV: {e}"))?;
    if data.len() < 44 || &data[0..4] != b"RIFF" || &data[8..12] != b"WAVE" {
        return Err("arquivo não é RIFF/WAVE válido".into());
    }

    let mut fmt: Option<(u16, u16, u32, u16)> = None; // (tag, canais, taxa, bits)
    let mut data_range: Option<(usize, usize)> = None;

    let mut pos = 12usize;
    while pos + 8 <= data.len() {
        let id = &data[pos..pos + 4];
        let size = rd_u32(&data, pos + 4) as usize;
        let body = pos + 8;
        if body + size > data.len() {
            break;
        }
        match id {
            b"fmt " => {
                if size < 16 {
                    return Err("chunk 'fmt ' truncado".into());
                }
                let mut tag = rd_u16(&data, body);
                let channels = rd_u16(&data, body + 2);
                let rate = rd_u32(&data, body + 4);
                let bits = rd_u16(&data, body + 14);
                if tag == 0xFFFE {
                    // WAVE_FORMAT_EXTENSIBLE: o código real está no GUID de subtipo.
                    if size < 40 {
                        return Err("'fmt ' extensível truncado".into());
                    }
                    tag = rd_u16(&data, body + 24);
                }
                fmt = Some((tag, channels, rate, bits));
            }
            b"data" => data_range = Some((body, size)),
            _ => {}
        }
        pos = body + size + (size & 1);
    }

    let (tag, channels, rate, bits) = fmt.ok_or("chunk 'fmt ' ausente")?;
    let (off, len) = data_range.ok_or("chunk 'data' ausente")?;
    if channels == 0 {
        return Err("WAV com 0 canais".into());
    }

    let bytes_per_sample = (bits as usize + 7) / 8;
    if bytes_per_sample == 0 {
        return Err("WAV com bits_per_sample = 0".into());
    }
    let frame_bytes = bytes_per_sample * channels as usize;
    if frame_bytes == 0 {
        return Err("block align inválido".into());
    }
    let frames = len / frame_bytes;
    let raw = &data[off..off + frames * frame_bytes];

    let mut mono_or_stereo: Vec<f32> = Vec::with_capacity(frames * channels as usize);
    for f in 0..frames {
        for c in 0..channels as usize {
            let b = &raw[(f * channels as usize + c) * bytes_per_sample
                ..(f * channels as usize + c + 1) * bytes_per_sample];
            let v: f32 = match (tag, bits) {
                (1, 8) => (b[0] as f32 - 128.0) / 128.0,
                (1, 16) => i16::from_le_bytes([b[0], b[1]]) as f32 / 32768.0,
                (1, 24) => {
                    let x = ((b[2] as i32) << 24 | (b[1] as i32) << 16 | (b[0] as i32) << 8) >> 8;
                    x as f32 / 8_388_608.0
                }
                (1, 32) => {
                    i32::from_le_bytes([b[0], b[1], b[2], b[3]]) as f32 / 2_147_483_648.0
                }
                (3, 32) => f32::from_le_bytes([b[0], b[1], b[2], b[3]]),
                (3, 64) => {
                    f64::from_le_bytes([b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7]]) as f32
                }
                _ => {
                    return Err(format!(
                        "formato WAV não suportado: tag={tag} bits={bits} (aceito PCM 8/16/24/32 e float 32/64)"
                    ))
                }
            };
            mono_or_stereo.push(v);
        }
    }

    // Normaliza para estéreo: mono -> duplica; >2 canais -> usa os dois primeiros.
    let mut samples = Vec::with_capacity(frames * 2);
    match channels {
        1 => {
            for v in mono_or_stereo {
                samples.push(v);
                samples.push(v);
            }
        }
        2 => samples = mono_or_stereo,
        n => {
            for f in 0..frames {
                samples.push(mono_or_stereo[f * n as usize]);
                samples.push(mono_or_stereo[f * n as usize + 1]);
            }
        }
    }

    Ok(WavIn {
        sample_rate: rate,
        channels,
        frames,
        samples,
    })
}

fn write_wav_f32(path: &OsStr, sample_rate: u32, channels: u16, samples: &[f32]) -> Result<(), String> {
    let bits = 32u16;
    let frame_bytes = 4u16 * channels;
    let data_bytes = (samples.len() * 4) as u32;
    let frames = samples.len() / channels as usize;

    let mut out = Vec::with_capacity(58 + samples.len() * 4);
    out.extend_from_slice(b"RIFF");
    out.extend_from_slice(&(36u32 + 4 + data_bytes).to_le_bytes()); // +4 = chunk 'fact'
    out.extend_from_slice(b"WAVE");

    out.extend_from_slice(b"fmt ");
    out.extend_from_slice(&16u32.to_le_bytes());
    out.extend_from_slice(&3u16.to_le_bytes()); // WAVE_FORMAT_IEEE_FLOAT
    out.extend_from_slice(&channels.to_le_bytes());
    out.extend_from_slice(&sample_rate.to_le_bytes());
    out.extend_from_slice(&(sample_rate * frame_bytes as u32).to_le_bytes());
    out.extend_from_slice(&frame_bytes.to_le_bytes());
    out.extend_from_slice(&bits.to_le_bytes());

    out.extend_from_slice(b"fact");
    out.extend_from_slice(&4u32.to_le_bytes());
    out.extend_from_slice(&(frames as u32).to_le_bytes());

    out.extend_from_slice(b"data");
    out.extend_from_slice(&data_bytes.to_le_bytes());
    for s in samples {
        out.extend_from_slice(&s.to_le_bytes());
    }

    fs::write(path, &out).map_err(|e| format!("não foi possível gravar o WAV: {e}"))
}

fn peak_rms(samples: &[f32]) -> (f32, f32) {
    let mut peak = 0.0f32;
    let mut sq = 0.0f64;
    for &s in samples {
        let a = s.abs();
        if a > peak {
            peak = a;
        }
        sq += (s as f64) * (s as f64);
    }
    let rms = if samples.is_empty() {
        0.0
    } else {
        (sq / samples.len() as f64).sqrt() as f32
    };
    (peak, rms)
}

fn to_db(x: f32) -> f32 {
    if x > 0.0 {
        20.0 * x.log10()
    } else {
        f32::NEG_INFINITY
    }
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 4 {
        eprintln!("uso: host <plugin.vst3> <in.wav> <out.wav> [blocos]");
        eprintln!();
        eprintln!("  <plugin.vst3>  caminho do .vst3 (DLL PE renomeada) — carregado somente leitura");
        eprintln!("  <in.wav>       WAV de entrada (PCM 8/16/24/32 ou float 32/64, 44.1 ou 48 kHz)");
        eprintln!("  <out.wav>      WAV float32 estéreo de saída (mesmo nº de frames da entrada)");
        eprintln!("  [blocos]       tamanho do bloco em frames (padrão 512)");
        std::process::exit(2);
    }

    let plugin_path = &args[1];
    let in_path = &args[2];
    let out_path = &args[3];
    let block_size: i32 = if args.len() > 4 {
        args[4]
            .parse::<i32>()
            .unwrap_or_else(|_| fail(&format!("[blocos] inválido: '{}'", args[4])))
    } else {
        512
    };
    if block_size <= 0 {
        fail("tamanho de bloco precisa ser > 0");
    }

    say("=== soultree host VST3 (oráculo etapa I) — somente leitura ===");
    say(&format!("plugin : {plugin_path}"));
    say(&format!("entrada: {in_path}"));
    say(&format!("saída  : {out_path}"));
    say(&format!("bloco  : {block_size} frames"));
    say("");

    // ---------------- 1. WAV de entrada ----------------
    let input = match read_wav(OsStr::new(in_path)) {
        Ok(w) => w,
        Err(e) => fail(&format!("entrada: {e}")),
    };
    let (in_peak, in_rms) = peak_rms(&input.samples);
    say(&format!(
        "WAV entrada: {} Hz, {} canal(is), {} frames ({:.3} s), pico {:.4} ({:.1} dBFS), RMS {:.1} dBFS",
        input.sample_rate,
        input.channels,
        input.frames,
        input.frames as f64 / input.sample_rate as f64,
        in_peak,
        to_db(in_peak),
        to_db(in_rms)
    ));
    if input.channels != 2 {
        say(&format!(
            "AVISO: entrada tem {} canal(is); convertida para estéreo (mono duplicado / 2 primeiros canais).",
            input.channels
        ));
    }
    let probe = env::var("SOULTREE_PROBE").map_or(false, |v| v == "1");
    if !probe && input.sample_rate != 44_100 && input.sample_rate != 48_000 {
        fail(&format!(
            "taxa de amostragem {} Hz não suportada nesta versão (use 44100 ou 48000). \
             Nada foi gravado.",
            input.sample_rate
        ));
    }
    if input.frames == 0 {
        fail("WAV de entrada sem frames");
    }
    say("");

    // ---------------- 2. carregar a DLL ----------------
    let wide: Vec<u16> = OsStr::new(plugin_path)
        .encode_wide()
        .chain(std::iter::once(0))
        .collect();
    log_call("kernel32!LoadLibraryW", LoadLibraryW as *const () as usize);
    let hmod = unsafe { LoadLibraryW(wide.as_ptr()) };
    if hmod.is_null() {
        let err = unsafe { GetLastError() };
        println!();
        fail(&format!(
            "LoadLibraryW falhou (GetLastError = {err} / 0x{err:08X}). \
             A DLL não carregou; nada foi processado. (Rota do dump repachado é sabidamente morta — §19.7.)"
        ));
    }
    let base = hmod as usize;
    let size = unsafe { image_size(base) };
    MODULE_BASE.store(base, Ordering::Relaxed);
    MODULE_SIZE.store(size, Ordering::Relaxed);
    log_value(&format!(
        "hmod=0x{:X}  base=0x{:X}  SizeOfImage=0x{:X}",
        hmod as usize, base, size
    ));

    // ---------------- 3. entry point VST3 ----------------
    let name = b"GetPluginFactory\0";
    log_call("kernel32!GetProcAddress(\"GetPluginFactory\")", GetProcAddress as *const () as usize);
    let proc = unsafe { GetProcAddress(hmod, name.as_ptr()) };
    log_value(&format!("0x{:X}", proc.map(|f| f as usize).unwrap_or(0)));
    let get_factory = match proc {
        Some(f) => f,
        None => fail(
            "o módulo não exporta GetPluginFactory — não é um plugin VST3 carregável. \
             (DllGetClassObject não é usado: o entry point VST3 é GetPluginFactory.)",
        ),
    };

    log_call("GetPluginFactory", get_factory as usize);
    let factory = unsafe { get_factory() };
    log_value(&format!("IPluginFactory*=0x{:X}", factory as usize));
    if factory.is_null() {
        fail("GetPluginFactory devolveu ponteiro nulo");
    }

    let factory_vt = unsafe { vt_factory(factory) };
    if factory_vt.is_null() {
        fail("IPluginFactory sem vtable (ponteiro inválido)");
    }

    unsafe { add_ref(factory, "FUnknown::addRef (factory)") };

    // info da factory
    let mut fi = PFactoryInfo {
        vendor: [0; 64],
        url: [0; 256],
        email: [0; 128],
        flags: 0,
    };
    let f = unsafe { (*factory_vt).get_factory_info };
    let hr = call0("IPluginFactory::getFactoryInfo", f as usize, || unsafe {
        f(factory, &mut fi)
    });
    if hr == K_RESULT_OK {
        say(&format!(
            "     vendor='{}' url='{}' email='{}' flags=0x{:X}",
            cstr(&fi.vendor),
            cstr(&fi.url),
            cstr(&fi.email),
            fi.flags
        ));
    }

    // classes
    let f = unsafe { (*factory_vt).count_classes };
    let count = call_value(
        "IPluginFactory::countClasses",
        f as usize,
        || unsafe { f(factory) },
        |n| format!("{n} classe(s) exportada(s)"),
    );
    let count = count.max(0);

    let mut chosen: Option<([u8; 16], String)> = None;
    for i in 0..count {
        let mut ci = PClassInfo {
            cid: [0; 16],
            cardinality: 0,
            category: [0; 32],
            name: [0; 64],
        };
        let f = unsafe { (*factory_vt).get_class_info };
        let hr = call0(
            &format!("IPluginFactory::getClassInfo({i})"),
            f as usize,
            || unsafe { f(factory, i, &mut ci) },
        );
        if hr != K_RESULT_OK {
            continue;
        }
        let cat = cstr(&ci.category);
        let nm = cstr(&ci.name);
        say(&format!(
            "     [{i}] cid={} cardinality={} category='{}' name='{}'",
            hex16(&ci.cid),
            ci.cardinality,
            cat,
            nm
        ));
        if cat == "Audio Module Class" && chosen.is_none() {
            chosen = Some((ci.cid, nm));
        }
    }

    let (cid, class_name) = match chosen {
        Some(c) => c,
        None => fail("nenhuma classe com categoria 'Audio Module Class' na factory"),
    };
    say(&format!(
        "     classe escolhida: '{}' cid={}",
        class_name,
        hex16(&cid)
    ));
    say("");

    // ---------------- 4. createInstance ----------------
    let f = unsafe { (*factory_vt).create_instance };
    log_call("IPluginFactory::createInstance(cid, IComponent)", f as usize);
    let mut comp: *mut c_void = ptr::null_mut();
    let hr0 = unsafe { f(factory, cid.as_ptr(), IID_ICOMPONENT.as_ptr(), &mut comp) };
    log_hr(hr0);

    if hr0 != K_RESULT_OK || comp.is_null() {
        // Segunda tentativa honesta: pedir só FUnknown e depois queryInterface.
        say("     createInstance com IComponent falhou; tentando FUnknown + queryInterface(IComponent)");
        log_call("IPluginFactory::createInstance(cid, FUnknown)", f as usize);
        let mut unk: *mut c_void = ptr::null_mut();
        let hr1 = unsafe { f(factory, cid.as_ptr(), IID_FUNKNOWN.as_ptr(), &mut unk) };
        log_hr(hr1);
        if hr1 != K_RESULT_OK || unk.is_null() {
            fail(&format!(
                "createInstance falhou nas duas variantes (IComponent: 0x{:08X} = {}; FUnknown: 0x{:08X} = {})",
                hr0 as u32,
                hr_name(hr0),
                hr1 as u32,
                hr_name(hr1)
            ));
        }
        match unsafe {
            query_interface(unk, &IID_ICOMPONENT, "FUnknown::queryInterface(IComponent)")
        } {
            Ok(c) => {
                unsafe { release(unk, "FUnknown::release (FUnknown temporário)") };
                comp = c;
            }
            Err(e) => fail(&format!(
                "queryInterface(IComponent) falhou: 0x{:08X} = {}",
                e as u32,
                hr_name(e)
            )),
        }
    } else {
        // `createInstance` já devolveu IComponent com uma referência nossa;
        // não chamamos addRef (a contagem inicial é 1).
    }
    say(&format!("     IComponent*=0x{:X}", comp as usize));

    let comp_vt = unsafe { vt_component(comp) };
    if comp_vt.is_null() {
        fail("IComponent sem vtable");
    }

    let proc_obj = match unsafe {
        query_interface(
            comp,
            &IID_IAUDIOPROCESSOR,
            "IComponent::queryInterface(IAudioProcessor)",
        )
    } {
        Ok(p) => {
            say(&format!("     IAudioProcessor*=0x{:X}", p as usize));
            p
        }
        Err(e) => fail(&format!(
            "queryInterface(IAudioProcessor) falhou: 0x{:08X} = {}",
            e as u32,
            hr_name(e)
        )),
    };
    let proc_vt = unsafe { vt_processor(proc_obj) };
    say("");

    // ---------------- 5. initialize ----------------
    let host_ctx = &HOST_OBJ as *const HostObj as *mut c_void;
    let f = unsafe { (*comp_vt).initialize };
    let hr = call0("IComponent::initialize(hostContext)", f as usize, || unsafe {
        f(comp, host_ctx)
    });
    if hr != K_RESULT_OK {
        fail(&format!(
            "initialize falhou: 0x{:08X} = {}",
            hr as u32,
            hr_name(hr)
        ));
    }

    // ---------------- 6. busses ----------------
    let f = unsafe { (*comp_vt).get_bus_count };
    let n_in = call_value(
        "IComponent::getBusCount(kAudio, kInput)",
        f as usize,
        || unsafe { f(comp, MEDIA_TYPE_AUDIO, BUS_DIR_INPUT) },
        |n| format!("{n}"),
    );
    let n_out = call_value(
        "IComponent::getBusCount(kAudio, kOutput)",
        f as usize,
        || unsafe { f(comp, MEDIA_TYPE_AUDIO, BUS_DIR_OUTPUT) },
        |n| format!("{n}"),
    );
    say(&format!("     busses de áudio: entrada={n_in}, saída={n_out}"));
    if n_in < 1 || n_out < 1 {
        fail(&format!(
            "plugin declara {n_in} entrada(s) e {n_out} saída(s) de áudio; esperado ≥1 de cada"
        ));
    }

    #[derive(Clone)]
    struct BusDesc {
        channels: i32,
        bus_type: i32,
    }
    let mut in_buses: Vec<BusDesc> = Vec::new();
    let mut out_buses: Vec<BusDesc> = Vec::new();

    for (dir, dirname, vec) in [
        (BUS_DIR_INPUT, "kInput", &mut in_buses as *mut Vec<BusDesc>),
        (BUS_DIR_OUTPUT, "kOutput", &mut out_buses as *mut Vec<BusDesc>),
    ] {
        let n = if dir == BUS_DIR_INPUT { n_in } else { n_out };
        for i in 0..n {
            let mut bi = BusInfo {
                media_type: 0,
                bus_direction: 0,
                channel_count: 0,
                name: [0; 128],
                bus_type: 0,
                flags: 0,
            };
            let f = unsafe { (*comp_vt).get_bus_info };
            let hr = call0(
                &format!("IComponent::getBusInfo(kAudio, {dirname}, {i})"),
                f as usize,
                || unsafe { f(comp, MEDIA_TYPE_AUDIO, dir, i, &mut bi) },
            );
            if hr != K_RESULT_OK {
                fail(&format!(
                    "getBusInfo(kAudio, {dirname}, {i}) falhou: 0x{:08X} = {}",
                    hr as u32,
                    hr_name(hr)
                ));
            }
            say(&format!(
                "     bus {dirname}[{i}] canal(is)={} tipo={} flags=0x{:X} nome='{}'",
                bi.channel_count,
                if bi.bus_type == 0 { "kMain" } else { "kAux" },
                bi.flags,
                utf16z(&bi.name)
            ));

            // arranjo atual do bus (apenas informativo)
            let mut arr: u64 = 0;
            let f = unsafe { (*proc_vt).get_bus_arrangement };
            let hr = call0(
                &format!("IAudioProcessor::getBusArrangement({dirname}, {i})"),
                f as usize,
                || unsafe { f(proc_obj, dir, i, &mut arr) },
            );
            if hr == K_RESULT_OK {
                say(&format!("         SpeakerArrangement=0x{arr:016X}"));
            }

            unsafe {
                (*vec).push(BusDesc {
                    channels: bi.channel_count,
                    bus_type: bi.bus_type,
                });
            }
        }
    }

    // Ativa só os buses principais (índice 0) e desativa o resto (ex.: sidechain).
    for (dir, dirname, n) in [
        (BUS_DIR_INPUT, "kInput", n_in),
        (BUS_DIR_OUTPUT, "kOutput", n_out),
    ] {
        for i in 0..n {
            let on = i == 0;
            let f = unsafe { (*comp_vt).activate_bus };
            let hr = call0(
                &format!(
                    "IComponent::activateBus(kAudio, {dirname}, {i}, {})",
                    on as u8
                ),
                f as usize,
                || unsafe { f(comp, MEDIA_TYPE_AUDIO, dir, i, on as u8) },
            );
            if hr != K_RESULT_OK && on {
                fail(&format!(
                    "activateBus(kAudio, {dirname}, {i}, true) falhou: 0x{:08X} = {}",
                    hr as u32,
                    hr_name(hr)
                ));
            }
        }
    }

    let main_in_ch = in_buses[0].channels;
    let main_out_ch = out_buses[0].channels;
    if main_in_ch != 2 || main_out_ch != 2 {
        fail(&format!(
            "este host só trata bus principal estéreo; o plugin declarou entrada={main_in_ch} saída={main_out_ch} canais"
        ));
    }
    if in_buses[0].bus_type != 0 || out_buses[0].bus_type != 0 {
        say("AVISO: o bus de índice 0 não é kMain; usando-o mesmo assim.");
    }
    say("");

    // ---------------- 7. amostras / latência ----------------
    let f = unsafe { (*proc_vt).can_process_sample_size };
    let hr = call0("IAudioProcessor::canProcessSampleSize(kSample32)", f as usize, || unsafe {
        f(proc_obj, SYMBOLIC_SAMPLE_32)
    });
    if hr != K_RESULT_OK {
        fail(&format!(
            "plugin não aceita sample size 32-bit: 0x{:08X} = {}",
            hr as u32,
            hr_name(hr)
        ));
    }

    let f = unsafe { (*proc_vt).get_latency_samples };
    let latency = call_value(
        "IAudioProcessor::getLatencySamples",
        f as usize,
        || unsafe { f(proc_obj) },
        |n| format!("{n} amostras"),
    );
    if latency > input.frames as u32 {
        say(&format!(
            "AVISO: latência reportada ({latency}) maior que o WAV de entrada ({} frames); \
             a saída estará dominada pelo atraso.",
            input.frames
        ));
    }

    let f = unsafe { (*proc_vt).get_tail_samples };
    let tail = call_value(
        "IAudioProcessor::getTailSamples",
        f as usize,
        || unsafe { f(proc_obj) },
        |n| format!("{n} amostras"),
    );
    let _ = tail;
    say("");

    // ---------------- 8. setupProcessing ----------------
    let mut setup = ProcessSetup {
        process_mode: PROCESS_MODE_OFFLINE,
        symbolic_sample_size: SYMBOLIC_SAMPLE_32,
        max_samples_per_block: block_size,
        sample_rate: input.sample_rate as f64,
    };
    let f = unsafe { (*proc_vt).setup_processing };
    let hr_offline = call0("IAudioProcessor::setupProcessing(kOffline)", f as usize, || unsafe {
        f(proc_obj, &mut setup)
    });
    let mut mode_used = PROCESS_MODE_OFFLINE;
    if hr_offline != K_RESULT_OK {
        say("     kOffline recusado; tentando kRealtime");
        setup.process_mode = PROCESS_MODE_REALTIME;
        let hr_rt = call0("IAudioProcessor::setupProcessing(kRealtime)", f as usize, || unsafe {
            f(proc_obj, &mut setup)
        });
        if hr_rt != K_RESULT_OK {
            fail(&format!(
                "setupProcessing falhou nos dois modos: kOffline=0x{:08X} ({}), kRealtime=0x{:08X} ({}). \
                 Nada foi processado nem gravado.",
                hr_offline as u32,
                hr_name(hr_offline),
                hr_rt as u32,
                hr_name(hr_rt)
            ));
        }
        mode_used = PROCESS_MODE_REALTIME;
    }
    say(&format!(
        "     setup: modo={}, sampleSize={}, maxBloco={}, taxa={} Hz",
        if mode_used == PROCESS_MODE_OFFLINE {
            "kOffline"
        } else {
            "kRealtime"
        },
        "kSample32",
        block_size,
        input.sample_rate
    ));
    say("");

    // ---------------- 9. ativar / processar ----------------
    let f = unsafe { (*comp_vt).set_active };
    let hr = call0("IComponent::setActive(true)", f as usize, || unsafe {
        f(comp, 1)
    });
    if hr != K_RESULT_OK {
        fail(&format!(
            "setActive(true) falhou: 0x{:08X} = {}",
            hr as u32,
            hr_name(hr)
        ));
    }

    let f = unsafe { (*proc_vt).set_processing };
    let hr = call0("IAudioProcessor::setProcessing(true)", f as usize, || unsafe {
        f(proc_obj, 1)
    });
    if hr != K_RESULT_OK {
        fail(&format!(
            "setProcessing(true) falhou: 0x{:08X} = {}",
            hr as u32,
            hr_name(hr)
        ));
    }
    say("");

    let bs = block_size as usize;
    let mut in_l = vec![0f32; bs];
    let mut in_r = vec![0f32; bs];
    let mut out_l = vec![0f32; bs];
    let mut out_r = vec![0f32; bs];

    // Arrays de ponteiros de canal para o bus principal.
    let mut in_ptrs: Vec<*mut f32> = vec![in_l.as_mut_ptr(), in_r.as_mut_ptr()];
    let mut out_ptrs: Vec<*mut f32> = vec![out_l.as_mut_ptr(), out_r.as_mut_ptr()];

    // Um AudioBusBuffers por bus declarado. Buses inativos vão com 0 canais e
    // ponteiro nulo (permitido pela spec), para não alimentar o sidechain.
    let mut inputs = vec![AudioBusBuffers::default(); n_in as usize];
    let mut outputs = vec![AudioBusBuffers::default(); n_out as usize];
    inputs[0].num_channels = 2;
    inputs[0].channel_buffers32 = in_ptrs.as_mut_ptr();
    outputs[0].num_channels = 2;
    outputs[0].channel_buffers32 = out_ptrs.as_mut_ptr();

    let mut total = vec![0f32; input.frames * 2];
    let mut pos = 0usize;
    let mut blocks = 0u32;
    let mut worst_hr = K_RESULT_OK;

    say(&format!(
        "processando {} frames em blocos de até {} ...",
        input.frames, block_size
    ));

    while pos < input.frames {
        let n = (input.frames - pos).min(bs);

        // Desintercala L/R (corrigido em 2026-11-25, M7: antes copiava a faixa intercalada
        // `samples[pos*2..pos*2+n]` inteira para `in_l`, o que dava L,R,L,R... ao plugin).
        for i in 0..n {
            in_l[i] = input.samples[(pos + i) * 2];
            in_r[i] = input.samples[(pos + i) * 2 + 1];
        }
        for i in n..bs {
            in_l[i] = 0.0;
            in_r[i] = 0.0;
        }
        for i in 0..bs {
            out_l[i] = 0.0;
            out_r[i] = 0.0;
        }

        let mut data = ProcessData {
            process_mode: mode_used,
            symbolic_sample_size: SYMBOLIC_SAMPLE_32,
            num_samples: n as i32,
            num_inputs: n_in,
            num_outputs: n_out,
            inputs: inputs.as_mut_ptr(),
            outputs: outputs.as_mut_ptr(),
            input_parameter_changes: ptr::null_mut(),
            output_parameter_changes: ptr::null_mut(),
            input_events: ptr::null_mut(),
            output_events: ptr::null_mut(),
            process_context: ptr::null_mut(), // opcional pela spec; sem transporte
        };

        let f = unsafe { (*proc_vt).process };
        let hr = call0(
            &format!("IAudioProcessor::process(#{blocks}, numSamples={n})"),
            f as usize,
            || unsafe { f(proc_obj, &mut data) },
        );
        if hr != K_RESULT_OK {
            worst_hr = hr;
            say(&format!(
                "     process devolveu 0x{:08X} = {} no bloco #{blocks} (frames {pos}..{})",
                hr as u32,
                hr_name(hr),
                pos + n
            ));
            break;
        }

        // Intercala L/R (corrigido em 2026-11-25, M7: antes gravava `out_l` contíguo em
        // `total[pos*2..pos*2+n]`, o que deixava metade de cada bloco sem escrita).
        for i in 0..n {
            total[(pos + i) * 2] = out_l[i];
            total[(pos + i) * 2 + 1] = out_r[i];
        }

        pos += n;
        blocks += 1;
        if let Ok(dir) = env::var("SOULTREE_PROBE_EACH") {
            probe_dump_engine(&dir, blocks as usize);
        }
    }

    if worst_hr != K_RESULT_OK {
        unsafe {
            let f = (*proc_vt).set_processing;
            log_call("IAudioProcessor::setProcessing(false)", f as usize);
            let hr = f(proc_obj, 0);
            log_hr(hr);
        }
        fail(&format!(
            "processamento abortado no bloco #{blocks} ({} de {} frames processados). \
             WAV de saída NÃO foi gravado. HRESULT: 0x{:08X} = {}",
            pos,
            input.frames,
            worst_hr as u32,
            hr_name(worst_hr)
        ));
    }

    if env::var("SOULTREE_PROBE").map_or(false, |v| v == "1") {
        probe_state("apos_process");
    }

    // ---------------- 10. desligar com honestidade ----------------
    let f = unsafe { (*proc_vt).set_processing };
    let hr = call0("IAudioProcessor::setProcessing(false)", f as usize, || unsafe {
        f(proc_obj, 0)
    });
    if hr != K_RESULT_OK {
        say(&format!(
            "AVISO: setProcessing(false) devolveu 0x{:08X} = {}",
            hr as u32,
            hr_name(hr)
        ));
    }
    let f = unsafe { (*comp_vt).set_active };
    let hr = call0("IComponent::setActive(false)", f as usize, || unsafe {
        f(comp, 0)
    });
    if hr != K_RESULT_OK {
        say(&format!(
            "AVISO: setActive(false) devolveu 0x{:08X} = {}",
            hr as u32,
            hr_name(hr)
        ));
    }
    let f = unsafe { (*comp_vt).terminate };
    let hr = call0("IComponent::terminate", f as usize, || unsafe { f(comp) });
    if hr != K_RESULT_OK {
        say(&format!(
            "AVISO: terminate devolveu 0x{:08X} = {}",
            hr as u32,
            hr_name(hr)
        ));
    }

    unsafe {
        release(proc_obj, "IAudioProcessor::release");
        release(comp, "IComponent::release");
        release(factory, "IPluginFactory::release");
    }

    say("");

    // ---------------- 11. validação e gravação ----------------
    if pos != input.frames {
        fail(&format!(
            "processou {pos} frames de {} — recusando gravar",
            input.frames
        ));
    }

    let (out_peak, out_rms) = peak_rms(&total);
    say(&format!(
        "frames processados: {} (entrada {})  blocos: {}",
        pos, input.frames, blocks
    ));
    say(&format!(
        "saída: pico {:.6} ({:.1} dBFS), RMS {:.1} dBFS",
        out_peak,
        to_db(out_peak),
        to_db(out_rms)
    ));

    if out_peak == 0.0 && in_peak > 0.0 {
        fail("saída é silêncio absoluto com entrada não silenciosa — recusando gravar (não é sucesso)");
    }
    if !total.iter().all(|s| s.is_finite()) {
        fail("saída contém NaN/Inf — recusando gravar");
    }

    // diffs úteis para o null-test
    let mut d_direct = 0f32;
    for i in 0..total.len() {
        let d = (total[i] - input.samples[i]).abs();
        if d > d_direct {
            d_direct = d;
        }
    }
    say(&format!(
        "diferença saída-entrada (sem alinhar): pico {:.6} ({:.1} dBFS)",
        d_direct,
        to_db(d_direct)
    ));
    if latency > 0 && (latency as usize) < input.frames {
        let lat = latency as usize;
        let mut d_shift = 0f32;
        let mut sq = 0f64;
        let mut cnt = 0usize;
        for f in 0..(input.frames - lat) {
            let d = (total[(f + lat) * 2] - input.samples[f * 2]).abs();
            if d > d_shift {
                d_shift = d;
            }
            sq += (d as f64) * (d as f64);
            cnt += 1;
        }
        say(&format!(
            "diferença alinhada por latência ({lat} amostras): pico {:.6} ({:.1} dBFS), RMS {:.1} dBFS",
            d_shift,
            to_db(d_shift),
            to_db((sq / cnt.max(1) as f64).sqrt() as f32)
        ));
    }
    if d_direct == 0.0 {
        say("NOTA: saída idêntica bit-a-bit à entrada (estado padrão sem processamento audível).");
    }

    match write_wav_f32(OsStr::new(out_path), input.sample_rate, 2, &total) {
        Ok(()) => say(&format!("WAV gravado: {out_path}")),
        Err(e) => fail(&e),
    }

    unsafe {
        log_call("kernel32!FreeLibrary", FreeLibrary as *const () as usize);
        let ok = FreeLibrary(hmod);
        log_value(if ok != 0 { "ok" } else { "falhou" });
    }

    say("");
    say("=== OK: plugin carregou, inicializou e processou ===");
}

// ---------------------------------------------------------------------------
// utilitários
// ---------------------------------------------------------------------------

fn cstr(buf: &[u8]) -> String {
    let end = buf.iter().position(|&b| b == 0).unwrap_or(buf.len());
    String::from_utf8_lossy(&buf[..end]).trim().to_string()
}

fn utf16z(buf: &[u16]) -> String {
    let end = buf.iter().position(|&c| c == 0).unwrap_or(buf.len());
    String::from_utf16_lossy(&buf[..end]).trim().to_string()
}

fn hex16(cid: &[u8; 16]) -> String {
    cid.iter().map(|b| format!("{b:02X}")).collect()
}

unsafe fn image_size(base: usize) -> usize {
    let e_lfanew = *((base + 0x3C) as *const u32) as usize;
    *((base + e_lfanew + 0x18 + 0x38) as *const u32) as usize
}

// ---------------------------------------------------------------------------
// FFI mínima (kernel32) — sem crates externos
// ---------------------------------------------------------------------------

type Hmodule = *mut c_void;
type Farproc = Option<unsafe extern "system" fn() -> *mut c_void>;

#[link(name = "kernel32")]
extern "system" {
    fn LoadLibraryW(path: *const u16) -> Hmodule;
    fn GetProcAddress(module: Hmodule, name: *const u8) -> Farproc;
    fn FreeLibrary(module: Hmodule) -> i32;
    fn GetLastError() -> u32;
    fn VirtualQuery(addr: *const c_void, info: *mut MemInfo, len: usize) -> usize;
}

#[repr(C)]
#[derive(Default)]
struct MemInfo {
    base: usize,
    alloc_base: usize,
    alloc_protect: u32,
    partition: u16,
    region_size: usize,
    state: u32,
    protect: u32,
    kind: u32,
}

// ---------------------------------------------------------------------------
// M4: sonda de estado SOMENTE LEITURA (SOULTREE_PROBE=1)
// ---------------------------------------------------------------------------
// Lê, no próprio processo do host, campos do objeto do plugin cujos offsets
// foram provados no dump (PLANO §26-M4, checks/u_sample_rate.md). Nenhuma
// escrita, nenhum hook: só VirtualQuery + leitura de memória já mapeada.

const RVA_VT_PROCESSOR: usize = 0x2037A58; // Soothe3AudioProcessor (00344DA6)
const RVA_VT_W: usize = 0x2037178; // subobjeto this+0xE40 (00336E5E/00336E65)
const RVA_API_FN1: usize = 0x862EF0; // [handle+8] (00862E89/00862E90)

fn readable(addr: usize, len: usize) -> bool {
    let mut mi = MemInfo::default();
    let r = unsafe { VirtualQuery(addr as *const c_void, &mut mi, std::mem::size_of::<MemInfo>()) };
    r != 0
        && mi.state == 0x1000 // MEM_COMMIT
        && mi.protect & 0x66 != 0 // R / RW / XR / XRW
        && mi.protect & 0x100 == 0 // não PAGE_GUARD
        && addr + len <= mi.base + mi.region_size
}

fn rd<T: Copy>(addr: usize) -> Option<T> {
    if readable(addr, std::mem::size_of::<T>()) {
        Some(unsafe { (addr as *const T).read_unaligned() })
    } else {
        None
    }
}

static ENGINE_ADDR: AtomicUsize = AtomicUsize::new(0);

/// Somente leitura: acha o engine (1ª vez por varredura) e grava engine[0..0x600] por bloco.
fn probe_dump_engine(dir: &str, blk: usize) {
    let mut eng = ENGINE_ADDR.load(Ordering::Relaxed);
    if eng == 0 {
        let base = MODULE_BASE.load(Ordering::Relaxed);
        let want = (base + RVA_VT_PROCESSOR) as u64;
        let mut a = 0x10000usize;
        'scan: while a < 0x7FFF_FFFF_0000 {
            let mut mi = MemInfo::default();
            let r = unsafe { VirtualQuery(a as *const c_void, &mut mi, std::mem::size_of::<MemInfo>()) };
            if r == 0 {
                break;
            }
            if mi.state == 0x1000 && mi.protect == 0x04 && mi.kind == 0x20000 {
                let p = mi.base as *const u64;
                for i in 0..mi.region_size / 8 {
                    if unsafe { p.add(i).read() } == want {
                        let obj = mi.base + 8 * i;
                        let h = rd::<u64>(obj + 0xE40 + 0x68).unwrap_or(0) as usize;
                        if h != 0 && rd::<u64>(h + 8).unwrap_or(0) as usize == base + RVA_API_FN1 {
                            eng = rd::<u64>(h).unwrap_or(0) as usize;
                            break 'scan;
                        }
                    }
                }
            }
            a = mi.base + mi.region_size;
        }
        ENGINE_ADDR.store(eng, Ordering::Relaxed);
    }
    if eng == 0 {
        return;
    }
    let mut buf = vec![0u8; 0x600];
    for (i, b) in buf.iter_mut().enumerate() {
        *b = rd::<u8>(eng + i).unwrap_or(0);
    }
    let _ = std::fs::write(format!("{dir}/blk{blk:03}.bin"), &buf);
}

fn probe_state(tag: &str) {
    let base = MODULE_BASE.load(Ordering::Relaxed);
    let want = (base + RVA_VT_PROCESSOR) as u64;
    let mut hits = Vec::new();
    let mut a = 0x10000usize;
    while a < 0x7FFF_FFFF_0000 {
        let mut mi = MemInfo::default();
        let r = unsafe { VirtualQuery(a as *const c_void, &mut mi, std::mem::size_of::<MemInfo>()) };
        if r == 0 {
            break;
        }
        let next = mi.base + mi.region_size;
        if mi.state == 0x1000 && mi.protect == 0x04 && mi.kind == 0x20000 {
            let n = mi.region_size / 8;
            let p = mi.base as *const u64;
            for i in 0..n {
                if unsafe { p.add(i).read() } == want {
                    hits.push(mi.base + 8 * i);
                }
            }
        }
        if next <= a {
            break;
        }
        a = next;
    }
    println!("PROBE[{tag}] processors={}", hits.len());
    for obj in hits {
        let w = obj + 0xE40;
        let vtw = rd::<u64>(w).unwrap_or(0) as usize;
        let h = rd::<u64>(w + 0x68).unwrap_or(0) as usize;
        let fn1 = if h != 0 { rd::<u64>(h + 8).unwrap_or(0) as usize } else { 0 };
        println!(
            "PROBE[{tag}] obj=0x{obj:X} [W]=+0x{:X} (esperado +0x{RVA_VT_W:X}) handle=0x{h:X} [h+8]=+0x{:X} (esperado +0x{RVA_API_FN1:X})",
            vtw.wrapping_sub(base),
            fn1.wrapping_sub(base)
        );
        if h == 0 || fn1 != base + RVA_API_FN1 {
            continue;
        }
        // M4-callback: [W+0x28]/[W+0x30] (chamados por 0x33A630 em 0033A657/0033A65F),
        // [W+0x70] (descritor, 00336EA6) e [[W+0x70]] (base das entradas de parâmetro).
        let w28 = rd::<u64>(w + 0x28).unwrap_or(0) as usize;
        let w30 = rd::<u64>(w + 0x30).unwrap_or(0) as usize;
        let w70 = rd::<u64>(w + 0x70).unwrap_or(0) as usize;
        let tab = if w70 != 0 { rd::<u64>(w70).unwrap_or(0) as usize } else { 0 };
        println!(
            "PROBE[{tag}] [W+0x28]=+0x{:X} [W+0x30]=+0x{:X} [W+0x70]=+0x{:X} [[W+0x70]]=+0x{:X}",
            w28.wrapping_sub(base), w30.wrapping_sub(base), w70.wrapping_sub(base), tab.wrapping_sub(base)
        );
        let mut hfns = String::new();
        for o in (0..=0x50).step_by(8) {
            let v = rd::<u64>(h + o).unwrap_or(0) as usize;
            hfns.push_str(&format!(" +0x{o:X}=+0x{:X}", v.wrapping_sub(base)));
        }
        println!("PROBE[{tag}] handle:{hfns}");
        let eng = rd::<u64>(h).unwrap_or(0) as usize;
        let a28 = rd::<f32>(eng + 0x28);
        let k2c = rd::<i32>(eng + 0x2C);
        println!("PROBE[{tag}] engine=0x{eng:X} [eng+0x28]f32={a28:?} [eng+0x2C]i32={k2c:?}");
        // M6: interface do host ([eng+0], 008634CD) e config ([eng+8], 008634D7)
        let iface = rd::<u64>(eng).unwrap_or(0) as usize;
        let cfg = rd::<u64>(eng + 8).unwrap_or(0) as usize;
        let mut fi = String::new();
        for o in (0..=0x40).step_by(8) {
            let v = rd::<u64>(iface + o).unwrap_or(0) as usize;
            fi.push_str(&format!(" +0x{o:X}=+0x{:X}", v.wrapping_sub(base)));
        }
        println!("PROBE[{tag}] iface=0x{iface:X}:{fi}");
        let iobj = rd::<u64>(iface).unwrap_or(0) as usize;
        println!("PROBE[{tag}] [[iface]+0x94] (habilita saídas do host, 0x338BA0) = {:?}", rd::<u8>(iobj + 0x94));
        let mut fc = String::new();
        for o in (0..0x40).step_by(4) {
            fc.push_str(&format!(" +0x{o:X}={:#x}", rd::<u32>(cfg + o).unwrap_or(0xDEAD)));
        }
        println!("PROBE[{tag}] cfg=0x{cfg:X}:{fc}");
        println!(
            "PROBE[{tag}] eng+0x10={:?} eng+0x14={:?} eng+0x4C={:?} eng+0x50={:?} eng+0xA7..AA={:?}",
            rd::<i32>(eng + 0x10), rd::<i32>(eng + 0x14), rd::<i32>(eng + 0x4C), rd::<i32>(eng + 0x50),
            rd::<[u8; 4]>(eng + 0xA7)
        );
        if let Ok(path) = env::var("SOULTREE_PROBE_DUMP") {
            let mut buf = vec![0u8; 0x600];
            for (i, b) in buf.iter_mut().enumerate() {
                *b = rd::<u8>(eng + i).unwrap_or(0);
            }
            let _ = std::fs::write(&path, &buf);
            println!("PROBE[{tag}] engine[0..0x600] gravado em {path}");
        }
        println!("PROBE[{tag}] flags 0x863070 [eng+0x234..0x238]={:?} [eng+0x278]={:?} [eng+0xAB]={:?}", rd::<[u8; 4]>(eng + 0x234), rd::<i32>(eng + 0x278), rd::<u8>(eng + 0xAB));
        // estado = engine+0x54 (etapa G); campos xmm6 (valor do callback +0x50)
        let st = eng + 0x54;
        let mut sv = String::new();
        for (i, o) in [(0, 0x00), (5, 0x04), (6, 0x08), (7, 0x0C), (8, 0x10), (9, 0x14), (10, 0x18), (11, 0x1C), (12, 0x20), (13, 0x24), (17, 0x28), (18, 0x3C), (21, 0xBC), (22, 0xC0), (23, 0xC4), (24, 0xC8), (25, 0xCC)] {
            sv.push_str(&format!(" p{i}={:?}", rd::<f32>(st + o)));
        }
        println!("PROBE[{tag}] state(engine+0x54):{sv}");
        for (nm, off) in [("A", 0x5ED0 + 8), ("B", 0x5ED0 + 0x2C50)] {
            let c = eng + off;
            println!(
                "PROBE[{tag}] ctx{nm}=eng+0x{off:X} +0x20f32={:?} +0x28={:?} +0x38={:?} +0x40={:?} +0x58={:?} +0x59={:?} +0x5C f32={:?} +0x60={:?}",
                rd::<f32>(c + 0x20),
                rd::<i64>(c + 0x28),
                rd::<i64>(c + 0x38),
                rd::<i64>(c + 0x40),
                rd::<u8>(c + 0x58),
                rd::<u8>(c + 0x59),
                rd::<f32>(c + 0x5C),
                rd::<i64>(c + 0x60),
            );
        }
    }
}

// ---------------------------------------------------------------------------
// placeholders (mantidos para clareza de intenção; ver NOTAS.md)
// ---------------------------------------------------------------------------
// `tuid()` fica disponível para presets/estado futuro, mas o host usa as
// constantes IID_* acima. Nenhum preset é aplicado nesta versão.
#[allow(dead_code)]
fn _unused_tuid_doc() {
    let _ = tuid(0, 0, 0, 0);
}
