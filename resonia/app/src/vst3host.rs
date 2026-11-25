//! A small VST3 test host: loads a plugin bundle, lists its real parameters
//! (names, ranges, defaults, as the plugin itself reports them) and runs audio
//! through it, so Resonia can be measured side by side with another plugin.

use crate::vst3tool::{com_uid, FreeLibrary, GetProcAddress, LoadLibraryExW};
use std::ffi::c_void;
use std::path::Path;

type Obj = *mut c_void;
const K_OK: i32 = 0;
const K_NO_INTERFACE: i32 = 0x80004002u32 as i32;
const K_NOT_IMPLEMENTED: i32 = 0x80004001u32 as i32;

fn iid_funknown() -> [u8; 16] {
    com_uid(0x00000000, 0x00000000, 0xC0000000, 0x00000046)
}
fn iid_host_application() -> [u8; 16] {
    com_uid(0x58E595CC, 0xDB2D4969, 0x8B6AAF8C, 0x36A664E5)
}
fn iid_plugin_factory2() -> [u8; 16] {
    com_uid(0x0007B650, 0xF24B4C0B, 0xA464EDB9, 0xF00B2ABB)
}
fn iid_component() -> [u8; 16] {
    com_uid(0xE831FF31, 0xF2D54301, 0x928EBBEE, 0x25697802)
}
fn iid_audio_processor() -> [u8; 16] {
    com_uid(0x42043F99, 0xB7DA453C, 0xA569E79D, 0x9AAEC33D)
}
fn iid_edit_controller() -> [u8; 16] {
    com_uid(0xDCD7BBE3, 0x7742448D, 0xA874AACC, 0x979C759E)
}
fn iid_param_changes() -> [u8; 16] {
    com_uid(0xA4779663, 0x0BB64A56, 0xB44384A8, 0x466FEB9D)
}
fn iid_param_queue() -> [u8; 16] {
    com_uid(0x01263A18, 0xED074F6F, 0x98C9D356, 0x4686F9BA)
}

// ------------------------------------------------------------------ plugin side vtables

#[repr(C)]
struct UnknownVt {
    query_interface: unsafe extern "system" fn(Obj, *const [u8; 16], *mut Obj) -> i32,
    add_ref: unsafe extern "system" fn(Obj) -> u32,
    release: unsafe extern "system" fn(Obj) -> u32,
}

#[repr(C)]
struct PClassInfo2 {
    cid: [u8; 16],
    cardinality: i32,
    category: [u8; 32],
    name: [u8; 64],
    class_flags: u32,
    subcategories: [u8; 128],
    vendor: [u8; 64],
    version: [u8; 64],
    sdk_version: [u8; 64],
}

#[repr(C)]
struct FactoryVt {
    base: UnknownVt,
    get_factory_info: unsafe extern "system" fn(Obj, *mut c_void) -> i32,
    count_classes: unsafe extern "system" fn(Obj) -> i32,
    get_class_info: unsafe extern "system" fn(Obj, i32, *mut c_void) -> i32,
    create_instance: unsafe extern "system" fn(Obj, *const [u8; 16], *const [u8; 16], *mut Obj) -> i32,
    get_class_info2: unsafe extern "system" fn(Obj, i32, *mut PClassInfo2) -> i32,
}

#[repr(C)]
struct ComponentVt {
    base: UnknownVt,
    initialize: unsafe extern "system" fn(Obj, Obj) -> i32,
    terminate: unsafe extern "system" fn(Obj) -> i32,
    get_controller_class_id: unsafe extern "system" fn(Obj, *mut [u8; 16]) -> i32,
    set_io_mode: unsafe extern "system" fn(Obj, i32) -> i32,
    get_bus_count: unsafe extern "system" fn(Obj, i32, i32) -> i32,
    get_bus_info: unsafe extern "system" fn(Obj, i32, i32, i32, *mut c_void) -> i32,
    get_routing_info: unsafe extern "system" fn(Obj, *mut c_void, *mut c_void) -> i32,
    activate_bus: unsafe extern "system" fn(Obj, i32, i32, i32, u8) -> i32,
    set_active: unsafe extern "system" fn(Obj, u8) -> i32,
}

#[repr(C)]
struct ProcessorVt {
    base: UnknownVt,
    set_bus_arrangements: unsafe extern "system" fn(Obj, *mut u64, i32, *mut u64, i32) -> i32,
    get_bus_arrangement: unsafe extern "system" fn(Obj, i32, i32, *mut u64) -> i32,
    can_process_sample_size: unsafe extern "system" fn(Obj, i32) -> i32,
    get_latency_samples: unsafe extern "system" fn(Obj) -> u32,
    setup_processing: unsafe extern "system" fn(Obj, *const ProcessSetup) -> i32,
    set_processing: unsafe extern "system" fn(Obj, u8) -> i32,
    process: unsafe extern "system" fn(Obj, *mut ProcessData) -> i32,
    get_tail_samples: unsafe extern "system" fn(Obj) -> u32,
}

#[repr(C)]
struct ControllerVt {
    base: UnknownVt,
    initialize: unsafe extern "system" fn(Obj, Obj) -> i32,
    terminate: unsafe extern "system" fn(Obj) -> i32,
    set_component_state: unsafe extern "system" fn(Obj, Obj) -> i32,
    set_state: unsafe extern "system" fn(Obj, Obj) -> i32,
    get_state: unsafe extern "system" fn(Obj, Obj) -> i32,
    get_parameter_count: unsafe extern "system" fn(Obj) -> i32,
    get_parameter_info: unsafe extern "system" fn(Obj, i32, *mut ParameterInfo) -> i32,
    get_param_string_by_value: unsafe extern "system" fn(Obj, u32, f64, *mut [u16; 128]) -> i32,
    get_param_value_by_string: unsafe extern "system" fn(Obj, u32, *const u16, *mut f64) -> i32,
    normalized_param_to_plain: unsafe extern "system" fn(Obj, u32, f64) -> f64,
    plain_param_to_normalized: unsafe extern "system" fn(Obj, u32, f64) -> f64,
    get_param_normalized: unsafe extern "system" fn(Obj, u32) -> f64,
    set_param_normalized: unsafe extern "system" fn(Obj, u32, f64) -> i32,
}

#[repr(C)]
struct ConnectionVt {
    base: UnknownVt,
    connect: unsafe extern "system" fn(Obj, Obj) -> i32,
    disconnect: unsafe extern "system" fn(Obj, Obj) -> i32,
    notify: unsafe extern "system" fn(Obj, Obj) -> i32,
}

#[repr(C)]
pub struct ParameterInfo {
    id: u32,
    title: [u16; 128],
    short_title: [u16; 128],
    units: [u16; 128],
    step_count: i32,
    default_normalized: f64,
    unit_id: i32,
    flags: i32,
}

#[repr(C)]
struct ProcessSetup {
    process_mode: i32,
    symbolic_sample_size: i32,
    max_samples_per_block: i32,
    sample_rate: f64,
}

#[repr(C)]
struct AudioBusBuffers {
    num_channels: i32,
    silence_flags: u64,
    channel_buffers32: *mut *mut f32,
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
    input_param_changes: Obj,
    output_param_changes: Obj,
    input_events: Obj,
    output_events: Obj,
    context: *mut ProcessContext,
}

#[repr(C)]
#[derive(Default)]
struct ProcessContext {
    state: u32,
    sample_rate: f64,
    project_time_samples: i64,
    system_time: i64,
    continous_time_samples: i64,
    project_time_music: f64,
    bar_position_music: f64,
    cycle_start_music: f64,
    cycle_end_music: f64,
    tempo: f64,
    time_sig_numerator: i32,
    time_sig_denominator: i32,
    chord_key_note: u8,
    chord_root_note: u8,
    chord_mask: i16,
    smpte_offset_subframes: i32,
    frame_rate_fps: u32,
    frame_rate_flags: u32,
    samples_to_next_clock: i32,
}

// ------------------------------------------------------------------ host side objects

#[repr(C)]
struct HostAppVt {
    base: UnknownVt,
    get_name: unsafe extern "system" fn(Obj, *mut [u16; 128]) -> i32,
    create_instance: unsafe extern "system" fn(Obj, *const [u8; 16], *const [u8; 16], *mut Obj) -> i32,
}
#[repr(C)]
struct HostApp {
    vt: *const HostAppVt,
}

unsafe extern "system" fn static_add_ref(_: Obj) -> u32 {
    1
}
unsafe extern "system" fn host_qi(this: Obj, iid: *const [u8; 16], out: *mut Obj) -> i32 {
    if *iid == iid_funknown() || *iid == iid_host_application() {
        *out = this;
        K_OK
    } else {
        *out = std::ptr::null_mut();
        K_NO_INTERFACE
    }
}
unsafe extern "system" fn host_get_name(_: Obj, name: *mut [u16; 128]) -> i32 {
    let n: Vec<u16> = "Resonia test host".encode_utf16().collect();
    let buf = &mut *name;
    buf.iter_mut().for_each(|c| *c = 0);
    buf[..n.len()].copy_from_slice(&n);
    K_OK
}
unsafe extern "system" fn host_create_instance(_: Obj, _: *const [u8; 16], _: *const [u8; 16], out: *mut Obj) -> i32 {
    *out = std::ptr::null_mut();
    K_NOT_IMPLEMENTED
}

#[repr(C)]
struct QueueVt {
    base: UnknownVt,
    get_parameter_id: unsafe extern "system" fn(Obj) -> u32,
    get_point_count: unsafe extern "system" fn(Obj) -> i32,
    get_point: unsafe extern "system" fn(Obj, i32, *mut i32, *mut f64) -> i32,
    add_point: unsafe extern "system" fn(Obj, i32, f64, *mut i32) -> i32,
}
#[repr(C)]
struct Queue {
    vt: *const QueueVt,
    id: u32,
    value: f64,
    points: i32,
}
unsafe extern "system" fn queue_qi(this: Obj, iid: *const [u8; 16], out: *mut Obj) -> i32 {
    if *iid == iid_funknown() || *iid == iid_param_queue() {
        *out = this;
        K_OK
    } else {
        *out = std::ptr::null_mut();
        K_NO_INTERFACE
    }
}
unsafe extern "system" fn queue_id(this: Obj) -> u32 {
    (*(this as *mut Queue)).id
}
unsafe extern "system" fn queue_count(this: Obj) -> i32 {
    (*(this as *mut Queue)).points
}
unsafe extern "system" fn queue_get(this: Obj, index: i32, offset: *mut i32, value: *mut f64) -> i32 {
    let q = &*(this as *mut Queue);
    if index != 0 || q.points == 0 {
        return K_NOT_IMPLEMENTED;
    }
    *offset = 0;
    *value = q.value;
    K_OK
}
unsafe extern "system" fn queue_add(this: Obj, _offset: i32, value: f64, index: *mut i32) -> i32 {
    let q = &mut *(this as *mut Queue);
    q.value = value;
    q.points = 1;
    if !index.is_null() {
        *index = 0;
    }
    K_OK
}

#[repr(C)]
struct ChangesVt {
    base: UnknownVt,
    get_parameter_count: unsafe extern "system" fn(Obj) -> i32,
    get_parameter_data: unsafe extern "system" fn(Obj, i32) -> Obj,
    add_parameter_data: unsafe extern "system" fn(Obj, *const u32, *mut i32) -> Obj,
}
#[repr(C)]
struct Changes {
    vt: *const ChangesVt,
    queues: Vec<Box<Queue>>,
    active: usize,
    /// output changes: one scratch queue that accepts whatever the plugin writes
    scratch: Box<Queue>,
    is_output: bool,
}
unsafe extern "system" fn changes_qi(this: Obj, iid: *const [u8; 16], out: *mut Obj) -> i32 {
    if *iid == iid_funknown() || *iid == iid_param_changes() {
        *out = this;
        K_OK
    } else {
        *out = std::ptr::null_mut();
        K_NO_INTERFACE
    }
}
unsafe extern "system" fn changes_count(this: Obj) -> i32 {
    let c = &*(this as *mut Changes);
    if c.is_output {
        0
    } else {
        c.active as i32
    }
}
unsafe extern "system" fn changes_get(this: Obj, index: i32) -> Obj {
    let c = &mut *(this as *mut Changes);
    match c.queues.get_mut(index as usize) {
        Some(q) if (index as usize) < c.active => &mut **q as *mut Queue as Obj,
        _ => std::ptr::null_mut(),
    }
}
unsafe extern "system" fn changes_add(this: Obj, id: *const u32, index: *mut i32) -> Obj {
    let c = &mut *(this as *mut Changes);
    c.scratch.id = if id.is_null() { 0 } else { *id };
    c.scratch.points = 0;
    if !index.is_null() {
        *index = 0;
    }
    &mut *c.scratch as *mut Queue as Obj
}

static HOST_VT: HostAppVt = HostAppVt {
    base: UnknownVt { query_interface: host_qi, add_ref: static_add_ref, release: static_add_ref },
    get_name: host_get_name,
    create_instance: host_create_instance,
};
static QUEUE_VT: QueueVt = QueueVt {
    base: UnknownVt { query_interface: queue_qi, add_ref: static_add_ref, release: static_add_ref },
    get_parameter_id: queue_id,
    get_point_count: queue_count,
    get_point: queue_get,
    add_point: queue_add,
};
static CHANGES_VT: ChangesVt = ChangesVt {
    base: UnknownVt { query_interface: changes_qi, add_ref: static_add_ref, release: static_add_ref },
    get_parameter_count: changes_count,
    get_parameter_data: changes_get,
    add_parameter_data: changes_add,
};

fn new_queue(id: u32, value: f64) -> Box<Queue> {
    Box::new(Queue { vt: &QUEUE_VT, id, value, points: 1 })
}
fn new_changes(is_output: bool) -> Box<Changes> {
    Box::new(Changes { vt: &CHANGES_VT, queues: Vec::new(), active: 0, scratch: new_queue(0, 0.0), is_output })
}

// ------------------------------------------------------------------ public API

fn wide(s: &str) -> Vec<u16> {
    s.encode_utf16().chain(Some(0)).collect()
}
fn from_wide(b: &[u16]) -> String {
    let end = b.iter().position(|&c| c == 0).unwrap_or(b.len());
    String::from_utf16_lossy(&b[..end])
}
fn cstr(b: &[u8]) -> String {
    let end = b.iter().position(|&x| x == 0).unwrap_or(b.len());
    String::from_utf8_lossy(&b[..end]).to_string()
}
unsafe fn vt<T>(o: Obj) -> &'static T {
    &**(o as *mut *const T)
}

#[derive(Clone, Debug)]
pub struct Param {
    pub id: u32,
    pub title: String,
    pub units: String,
    pub steps: i32,
    pub default: f64,
    pub flags: i32,
    pub default_text: String,
    pub min_text: String,
    pub max_text: String,
}

pub struct Plugin {
    module: Obj,
    name: String,
    component: Obj,
    processor: Obj,
    controller: Obj,
    separate_controller: bool,
    host: Box<HostApp>,
    pub params: Vec<Param>,
    pub latency: u32,
    active: bool,
    in_changes: Box<Changes>,
    out_changes: Box<Changes>,
    context: Box<ProcessContext>,
    sr: f64,
    block: usize,
    sample_pos: i64,
}

impl Plugin {
    pub fn name(&self) -> &str {
        &self.name
    }

    /// Load the binary inside a .vst3 bundle (or a bare .vst3/.dll file).
    pub fn load(path: &Path) -> Result<Plugin, String> {
        let bin = if path.is_dir() { crate::vst3tool::binary_in(path) } else { path.to_path_buf() };
        unsafe {
            let w: Vec<u16> = bin.as_os_str().to_string_lossy().encode_utf16().chain(Some(0)).collect();
            let module = LoadLibraryExW(w.as_ptr(), std::ptr::null_mut(), 0x8);
            if module.is_null() {
                return Err(format!("could not load {}", bin.display()));
            }
            let init = GetProcAddress(module, b"InitDll\0".as_ptr());
            if !init.is_null() {
                let f: unsafe extern "system" fn() -> u8 = std::mem::transmute(init);
                f();
            }
            let gpf = GetProcAddress(module, b"GetPluginFactory\0".as_ptr());
            if gpf.is_null() {
                return Err("GetPluginFactory not exported".into());
            }
            let gpf: unsafe extern "system" fn() -> Obj = std::mem::transmute(gpf);
            let factory = gpf();
            if factory.is_null() {
                return Err("the plugin returned no factory (licence or protection check?)".into());
            }
            let mut f2: Obj = std::ptr::null_mut();
            (vt::<UnknownVt>(factory).query_interface)(factory, &iid_plugin_factory2(), &mut f2);
            if f2.is_null() {
                return Err("factory has no IPluginFactory2".into());
            }
            let fvt = vt::<FactoryVt>(f2);
            let mut audio_cid = None;
            let mut name = String::new();
            for i in 0..(fvt.count_classes)(f2) {
                let mut ci: PClassInfo2 = std::mem::zeroed();
                if (fvt.get_class_info2)(f2, i, &mut ci) == K_OK && cstr(&ci.category) == "Audio Module Class" {
                    audio_cid = Some(ci.cid);
                    name = cstr(&ci.name);
                    break;
                }
            }
            let cid = audio_cid.ok_or("no audio module class")?;
            let host = Box::new(HostApp { vt: &HOST_VT });
            let host_ptr = &*host as *const HostApp as Obj;
            let mut component: Obj = std::ptr::null_mut();
            let r = (fvt.create_instance)(f2, &cid, &iid_component(), &mut component);
            if r != K_OK || component.is_null() {
                return Err(format!("createInstance(component) failed: 0x{r:08X}"));
            }
            let cvt = vt::<ComponentVt>(component);
            let r = (cvt.initialize)(component, host_ptr);
            if r != K_OK {
                return Err(format!("component initialize failed: 0x{r:08X}"));
            }
            let mut processor: Obj = std::ptr::null_mut();
            (cvt.base.query_interface)(component, &iid_audio_processor(), &mut processor);
            if processor.is_null() {
                return Err("component has no IAudioProcessor".into());
            }
            // controller: same object, or a separate class
            let mut controller: Obj = std::ptr::null_mut();
            let mut separate = false;
            (cvt.base.query_interface)(component, &iid_edit_controller(), &mut controller);
            if controller.is_null() {
                let mut ccid = [0u8; 16];
                if (cvt.get_controller_class_id)(component, &mut ccid) == K_OK {
                    (fvt.create_instance)(f2, &ccid, &iid_edit_controller(), &mut controller);
                    if !controller.is_null() {
                        separate = true;
                        let r = (vt::<ControllerVt>(controller).initialize)(controller, host_ptr);
                        if r != K_OK {
                            return Err(format!("controller initialize failed: 0x{r:08X}"));
                        }
                        // connect the two halves, as hosts do (JUCE plugins publish
                        // their parameters to the controller this way)
                        let iid_cp = com_uid(0x70A4156F, 0x6E6E4026, 0x989148BF, 0xAA60D8D1);
                        let mut cp_comp: Obj = std::ptr::null_mut();
                        let mut cp_ctrl: Obj = std::ptr::null_mut();
                        (cvt.base.query_interface)(component, &iid_cp, &mut cp_comp);
                        (vt::<UnknownVt>(controller).query_interface)(controller, &iid_cp, &mut cp_ctrl);
                        if !cp_comp.is_null() && !cp_ctrl.is_null() {
                            (vt::<ConnectionVt>(cp_comp).connect)(cp_comp, cp_ctrl);
                            (vt::<ConnectionVt>(cp_ctrl).connect)(cp_ctrl, cp_comp);
                        }
                    }
                }
            }
            let mut p = Plugin {
                module,
                name,
                component,
                processor,
                controller,
                separate_controller: separate,
                host,
                params: Vec::new(),
                latency: 0,
                active: false,
                in_changes: new_changes(false),
                out_changes: new_changes(true),
                context: Box::new(ProcessContext::default()),
                sr: 48000.0,
                block: 512,
                sample_pos: 0,
            };
            p.read_params();
            Ok(p)
        }
    }

    fn read_params(&mut self) {
        if self.controller.is_null() {
            return;
        }
        unsafe {
            let c = self.controller;
            let v = vt::<ControllerVt>(c);
            let n = (v.get_parameter_count)(c);
            for i in 0..n {
                let mut info: ParameterInfo = std::mem::zeroed();
                if (v.get_parameter_info)(c, i, &mut info) != K_OK {
                    continue;
                }
                let text = |x: f64| {
                    let mut s = [0u16; 128];
                    if (v.get_param_string_by_value)(c, info.id, x, &mut s) == K_OK {
                        from_wide(&s)
                    } else {
                        String::new()
                    }
                };
                self.params.push(Param {
                    id: info.id,
                    title: from_wide(&info.title),
                    units: from_wide(&info.units),
                    steps: info.step_count,
                    default: info.default_normalized,
                    flags: info.flags,
                    default_text: text(info.default_normalized),
                    min_text: text(0.0),
                    max_text: text(1.0),
                });
            }
        }
    }

    /// Text the plugin shows for a parameter at a normalized value.
    pub fn text_at(&self, id: u32, x: f64) -> String {
        unsafe {
            let c = self.controller;
            if c.is_null() {
                return String::new();
            }
            let mut s = [0u16; 128];
            if (vt::<ControllerVt>(c).get_param_string_by_value)(c, id, x, &mut s) == K_OK {
                from_wide(&s)
            } else {
                String::new()
            }
        }
    }

    /// Normalized value for a text the plugin understands ("6.0"), if it can parse it.
    pub fn value_from_text(&self, id: u32, text: &str) -> Option<f64> {
        unsafe {
            let c = self.controller;
            if c.is_null() {
                return None;
            }
            let mut out = 0.0;
            let w = wide(text);
            if (vt::<ControllerVt>(c).get_param_value_by_string)(c, id, w.as_ptr(), &mut out) == K_OK {
                Some(out)
            } else {
                None
            }
        }
    }

    pub fn find_param(&self, title: &str) -> Option<&Param> {
        let t = title.to_lowercase();
        self.params.iter().find(|p| p.title.to_lowercase() == t)
    }

    /// Prepare for stereo processing at the given rate.
    pub fn activate(&mut self, sr: f64, block: usize) -> Result<(), String> {
        unsafe {
            let cvt = vt::<ComponentVt>(self.component);
            let pvt = vt::<ProcessorVt>(self.processor);
            let n_in = (cvt.get_bus_count)(self.component, 0, 0).max(1);
            let mut ins = vec![3u64; n_in as usize];
            let mut outs = [3u64];
            (pvt.set_bus_arrangements)(self.processor, ins.as_mut_ptr(), n_in, outs.as_mut_ptr(), 1);
            (cvt.activate_bus)(self.component, 0, 0, 0, 1);
            (cvt.activate_bus)(self.component, 0, 1, 0, 1);
            for b in 1..n_in {
                (cvt.activate_bus)(self.component, 0, 0, b, 0);
            }
            let setup = ProcessSetup { process_mode: 2, symbolic_sample_size: 0, max_samples_per_block: block as i32, sample_rate: sr };
            let r = (pvt.setup_processing)(self.processor, &setup);
            if r != K_OK {
                return Err(format!("setupProcessing failed: 0x{r:08X}"));
            }
            let r = (cvt.set_active)(self.component, 1);
            if r != K_OK {
                return Err(format!("setActive failed: 0x{r:08X}"));
            }
            (pvt.set_processing)(self.processor, 1);
            self.latency = (pvt.get_latency_samples)(self.processor);
            self.active = true;
            self.sr = sr;
            self.block = block;
            self.context.sample_rate = sr;
            self.context.tempo = 120.0;
            self.context.time_sig_numerator = 4;
            self.context.time_sig_denominator = 4;
            self.context.state = (1 << 10) | (1 << 13) | (1 << 1);
        }
        Ok(())
    }

    /// Parameters to send with the next block (normalized values).
    pub fn set_params(&mut self, values: &[(u32, f64)]) {
        let c = &mut self.in_changes;
        c.queues = values.iter().map(|&(id, v)| new_queue(id, v)).collect();
        c.active = c.queues.len();
        unsafe {
            if !self.controller.is_null() {
                for &(id, v) in values {
                    (vt::<ControllerVt>(self.controller).set_param_normalized)(self.controller, id, v);
                }
            }
        }
    }

    /// Process a whole stereo signal; returns the output (same length) and the latency
    /// reported after the run.
    pub fn run(&mut self, input: &[Vec<f32>; 2]) -> Result<[Vec<f32>; 2], String> {
        let len = input[0].len();
        let mut out = [vec![0.0f32; len], vec![0.0f32; len]];
        let mut inl = vec![0.0f32; self.block];
        let mut inr = vec![0.0f32; self.block];
        let mut ol = vec![0.0f32; self.block];
        let mut or = vec![0.0f32; self.block];
        let mut scl = vec![0.0f32; self.block];
        let mut scr = vec![0.0f32; self.block];
        let n_in = unsafe { (vt::<ComponentVt>(self.component).get_bus_count)(self.component, 0, 0).max(1) } as usize;
        let mut pos = 0;
        while pos < len {
            let n = self.block.min(len - pos);
            inl[..n].copy_from_slice(&input[0][pos..pos + n]);
            inr[..n].copy_from_slice(&input[1][pos..pos + n]);
            let mut in_ptrs = [inl.as_mut_ptr(), inr.as_mut_ptr()];
            let mut sc_ptrs = [scl.as_mut_ptr(), scr.as_mut_ptr()];
            let mut out_ptrs = [ol.as_mut_ptr(), or.as_mut_ptr()];
            let mut in_bus = vec![AudioBusBuffers { num_channels: 2, silence_flags: 0, channel_buffers32: in_ptrs.as_mut_ptr() }];
            for _ in 1..n_in {
                in_bus.push(AudioBusBuffers { num_channels: 2, silence_flags: 3, channel_buffers32: sc_ptrs.as_mut_ptr() });
            }
            let mut out_bus = AudioBusBuffers { num_channels: 2, silence_flags: 0, channel_buffers32: out_ptrs.as_mut_ptr() };
            self.context.project_time_samples = self.sample_pos;
            self.context.continous_time_samples = self.sample_pos;
            let mut data = ProcessData {
                process_mode: 2,
                symbolic_sample_size: 0,
                num_samples: n as i32,
                num_inputs: n_in as i32,
                num_outputs: 1,
                inputs: in_bus.as_mut_ptr(),
                outputs: &mut out_bus,
                input_param_changes: &mut *self.in_changes as *mut Changes as Obj,
                output_param_changes: &mut *self.out_changes as *mut Changes as Obj,
                input_events: std::ptr::null_mut(),
                output_events: std::ptr::null_mut(),
                context: &mut *self.context,
            };
            let r = unsafe { (vt::<ProcessorVt>(self.processor).process)(self.processor, &mut data) };
            if r != K_OK {
                return Err(format!("process failed: 0x{r:08X}"));
            }
            self.in_changes.active = 0;
            out[0][pos..pos + n].copy_from_slice(&ol[..n]);
            out[1][pos..pos + n].copy_from_slice(&or[..n]);
            pos += n;
            self.sample_pos += n as i64;
        }
        self.latency = unsafe { (vt::<ProcessorVt>(self.processor).get_latency_samples)(self.processor) };
        Ok(out)
    }
}

impl Drop for Plugin {
    fn drop(&mut self) {
        unsafe {
            if self.active {
                (vt::<ProcessorVt>(self.processor).set_processing)(self.processor, 0);
                (vt::<ComponentVt>(self.component).set_active)(self.component, 0);
            }
            if self.separate_controller && !self.controller.is_null() {
                (vt::<ControllerVt>(self.controller).terminate)(self.controller);
                (vt::<UnknownVt>(self.controller).release)(self.controller);
            } else if !self.controller.is_null() {
                (vt::<UnknownVt>(self.controller).release)(self.controller);
            }
            (vt::<UnknownVt>(self.processor).release)(self.processor);
            (vt::<ComponentVt>(self.component).terminate)(self.component);
            (vt::<UnknownVt>(self.component).release)(self.component);
            let exit = GetProcAddress(self.module, b"ExitDll\0".as_ptr());
            if !exit.is_null() {
                let f: unsafe extern "system" fn() -> u8 = std::mem::transmute(exit);
                f();
            }
            FreeLibrary(self.module);
        }
        let _ = &self.host;
    }
}
