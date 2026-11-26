//! Builds the South.air.vst3 bundle with the same layout as a standard VST3 bundle
//! (Contents/x86_64-win/<name>.vst3 + Contents/Resources/moduleinfo.json) and
//! validates it by loading the plugin and asking its factory what it contains.

use std::ffi::c_void;
use std::path::{Path, PathBuf};

#[repr(C)]
struct PFactoryInfo {
    vendor: [u8; 64],
    url: [u8; 256],
    email: [u8; 128],
    flags: i32,
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

type Obj = *mut c_void;

#[repr(C)]
struct FactoryVt {
    query_interface: unsafe extern "system" fn(Obj, *const [u8; 16], *mut Obj) -> i32,
    add_ref: unsafe extern "system" fn(Obj) -> u32,
    release: unsafe extern "system" fn(Obj) -> u32,
    get_factory_info: unsafe extern "system" fn(Obj, *mut PFactoryInfo) -> i32,
    count_classes: unsafe extern "system" fn(Obj) -> i32,
    get_class_info: unsafe extern "system" fn(Obj, i32, *mut c_void) -> i32,
    create_instance: unsafe extern "system" fn(Obj, *const [u8; 16], *const [u8; 16], *mut Obj) -> i32,
    get_class_info2: unsafe extern "system" fn(Obj, i32, *mut PClassInfo2) -> i32,
}

#[repr(C)]
struct ComponentVt {
    query_interface: unsafe extern "system" fn(Obj, *const [u8; 16], *mut Obj) -> i32,
    add_ref: unsafe extern "system" fn(Obj) -> u32,
    release: unsafe extern "system" fn(Obj) -> u32,
    initialize: unsafe extern "system" fn(Obj, Obj) -> i32,
    terminate: unsafe extern "system" fn(Obj) -> i32,
    get_controller_class_id: unsafe extern "system" fn(Obj, *mut [u8; 16]) -> i32,
    set_io_mode: unsafe extern "system" fn(Obj, i32) -> i32,
    get_bus_count: unsafe extern "system" fn(Obj, i32, i32) -> i32,
}

/// Interface ids in the byte order Windows (COM-compatible) VST3 uses.
pub fn com_uid(l1: u32, l2: u32, l3: u32, l4: u32) -> [u8; 16] {
    let a = l1.to_le_bytes();
    let b = l2.to_be_bytes();
    let c = l3.to_be_bytes();
    let d = l4.to_be_bytes();
    [a[0], a[1], a[2], a[3], b[1], b[0], b[3], b[2], c[0], c[1], c[2], c[3], d[0], d[1], d[2], d[3]]
}

/// The text form of a class id used in moduleinfo.json (inverse of `com_uid`).
pub fn cid_string(c: &[u8; 16]) -> String {
    let d1 = u32::from_le_bytes([c[0], c[1], c[2], c[3]]);
    let d2 = u16::from_le_bytes([c[4], c[5]]);
    let d3 = u16::from_le_bytes([c[6], c[7]]);
    let mut s = format!("{d1:08X}{d2:04X}{d3:04X}");
    for b in &c[8..] {
        s.push_str(&format!("{b:02X}"));
    }
    s
}

fn cstr(b: &[u8]) -> String {
    let end = b.iter().position(|&x| x == 0).unwrap_or(b.len());
    String::from_utf8_lossy(&b[..end]).to_string()
}

fn json_str(s: &str) -> String {
    let mut o = String::from("\"");
    for ch in s.chars() {
        match ch {
            '"' => o.push_str("\\\""),
            '\\' => o.push_str("\\\\"),
            c if (c as u32) < 0x20 => o.push_str(&format!("\\u{:04x}", c as u32)),
            c => o.push(c),
        }
    }
    o.push('"');
    o
}

#[cfg_attr(windows, link(name = "kernel32"))]
extern "system" {
    pub fn LoadLibraryExW(name: *const u16, file: Obj, flags: u32) -> Obj;
    pub fn LoadLibraryW(name: *const u16) -> Obj;
    pub fn GetProcAddress(module: Obj, name: *const u8) -> Obj;
    pub fn FreeLibrary(module: Obj) -> i32;
}

pub struct ClassInfo {
    pub cid: [u8; 16],
    pub category: String,
    pub name: String,
    pub flags: u32,
    pub subcategories: String,
    pub vendor: String,
    pub version: String,
    pub sdk_version: String,
}

pub struct ModuleReport {
    pub vendor: String,
    pub url: String,
    pub email: String,
    pub factory_flags: i32,
    pub classes: Vec<ClassInfo>,
    pub audio_inputs: i32,
    pub audio_outputs: i32,
}

/// Load the plugin binary, read its factory and create one instance of each class.
pub fn inspect(dll: &Path) -> Result<ModuleReport, String> {
    let wide: Vec<u16> = dll.as_os_str().to_string_lossy().encode_utf16().chain(Some(0)).collect();
    unsafe {
        let module = LoadLibraryW(wide.as_ptr());
        if module.is_null() {
            return Err(format!("could not load {}", dll.display()));
        }
        let result = (|| {
            let sym = GetProcAddress(module, b"GetPluginFactory\0".as_ptr());
            if sym.is_null() {
                return Err("GetPluginFactory is not exported".to_string());
            }
            let get: unsafe extern "system" fn() -> Obj = std::mem::transmute(sym);
            let factory = get();
            if factory.is_null() {
                return Err("GetPluginFactory returned nothing".into());
            }
            let vt = &**(factory as *mut *const FactoryVt);
            let mut fi: PFactoryInfo = std::mem::zeroed();
            if (vt.get_factory_info)(factory, &mut fi) != 0 {
                return Err("getFactoryInfo failed".into());
            }
            // IPluginFactory2
            let iid2 = com_uid(0x0007B650, 0xF24B4C0B, 0xA464EDB9, 0xF00B2ABB);
            let mut f2: Obj = std::ptr::null_mut();
            if (vt.query_interface)(factory, &iid2, &mut f2) != 0 || f2.is_null() {
                return Err("factory does not offer IPluginFactory2".into());
            }
            let vt2 = &**(f2 as *mut *const FactoryVt);
            let n = (vt2.count_classes)(f2);
            let mut classes = Vec::new();
            let mut ins = -1;
            let mut outs = -1;
            for i in 0..n {
                let mut ci: PClassInfo2 = std::mem::zeroed();
                if (vt2.get_class_info2)(f2, i, &mut ci) != 0 {
                    return Err(format!("getClassInfo2({i}) failed"));
                }
                let info = ClassInfo {
                    cid: ci.cid,
                    category: cstr(&ci.category),
                    name: cstr(&ci.name),
                    flags: ci.class_flags,
                    subcategories: cstr(&ci.subcategories),
                    vendor: cstr(&ci.vendor),
                    version: cstr(&ci.version),
                    sdk_version: cstr(&ci.sdk_version),
                };
                if info.category == "Audio Module Class" {
                    // IComponent
                    let iid_comp = com_uid(0xE831FF31, 0xF2D54301, 0x928EBBEE, 0x25697802);
                    let mut comp: Obj = std::ptr::null_mut();
                    if (vt2.create_instance)(f2, &ci.cid, &iid_comp, &mut comp) != 0 || comp.is_null() {
                        return Err("could not create the audio component".into());
                    }
                    let cvt = &**(comp as *mut *const ComponentVt);
                    if (cvt.initialize)(comp, std::ptr::null_mut()) != 0 {
                        return Err("component initialize failed".into());
                    }
                    ins = (cvt.get_bus_count)(comp, 0, 0);
                    outs = (cvt.get_bus_count)(comp, 0, 1);
                    (cvt.terminate)(comp);
                    (cvt.release)(comp);
                }
                classes.push(info);
            }
            (vt2.release)(f2);
            (vt.release)(factory);
            Ok(ModuleReport {
                vendor: cstr(&fi.vendor),
                url: cstr(&fi.url),
                email: cstr(&fi.email),
                factory_flags: fi.flags,
                classes,
                audio_inputs: ins,
                audio_outputs: outs,
            })
        })();
        FreeLibrary(module);
        result
    }
}

/// moduleinfo.json written from what the plugin itself reports, laid out like the
/// file the VST3 SDK tools generate.
pub fn module_info_json(r: &ModuleReport, name: &str, version: &str) -> String {
    let mut o = String::new();
    o.push_str("{\n");
    o.push_str(&format!("  \"Name\": {},\n  \"Version\": {},\n", json_str(name), json_str(version)));
    o.push_str("  \"Factory Info\": {\n");
    o.push_str(&format!(
        "    \"Vendor\": {},\n    \"URL\": {},\n    \"E-Mail\": {},\n",
        json_str(&r.vendor),
        json_str(&r.url),
        json_str(&r.email)
    ));
    o.push_str(&format!(
        "    \"Flags\": {{\n      \"Unicode\": {},\n      \"Classes Discardable\": {},\n      \"Component Non Discardable\": {}\n    }}\n  }},\n",
        r.factory_flags & 0x10 != 0,
        r.factory_flags & 0x01 != 0,
        r.factory_flags & 0x08 != 0
    ));
    o.push_str("  \"Classes\": [\n");
    for (i, c) in r.classes.iter().enumerate() {
        let subs: Vec<String> = c.subcategories.split('|').filter(|s| !s.is_empty()).map(json_str).collect();
        o.push_str("    {\n");
        o.push_str(&format!("      \"CID\": {},\n", json_str(&cid_string(&c.cid))));
        o.push_str(&format!("      \"Category\": {},\n", json_str(&c.category)));
        o.push_str(&format!("      \"Name\": {},\n", json_str(&c.name)));
        o.push_str(&format!("      \"Vendor\": {},\n", json_str(&c.vendor)));
        o.push_str(&format!("      \"Version\": {},\n", json_str(&c.version)));
        o.push_str(&format!("      \"SDKVersion\": {},\n", json_str(&c.sdk_version)));
        o.push_str(&format!("      \"Sub Categories\": [{}],\n", subs.join(", ")));
        o.push_str(&format!("      \"Class Flags\": {},\n", c.flags));
        o.push_str("      \"Cardinality\": 2147483647,\n      \"Snapshots\": []\n");
        o.push_str(if i + 1 < r.classes.len() { "    },\n" } else { "    }\n" });
    }
    o.push_str("  ]\n}\n");
    o
}

pub fn binary_in(bundle: &Path) -> PathBuf {
    let name = bundle.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();
    bundle.join("Contents").join("x86_64-win").join(name)
}

/// Create `<out_dir>/<name>.vst3` from the built plugin library.
pub fn make_bundle(dll: &Path, out_dir: &Path, name: &str, version: &str) -> Result<PathBuf, String> {
    let bundle = out_dir.join(format!("{name}.vst3"));
    let bin = binary_in(&bundle);
    let res = bundle.join("Contents").join("Resources");
    std::fs::create_dir_all(bin.parent().unwrap()).map_err(|e| e.to_string())?;
    std::fs::create_dir_all(&res).map_err(|e| e.to_string())?;
    std::fs::copy(dll, &bin).map_err(|e| format!("cannot copy {}: {e}", dll.display()))?;
    let report = inspect(&bin)?;
    std::fs::write(res.join("moduleinfo.json"), module_info_json(&report, name, version)).map_err(|e| e.to_string())?;
    Ok(bundle)
}

/// Check the bundle layout and that moduleinfo.json agrees with the plugin. Returns lines to print.
pub fn check_bundle(bundle: &Path) -> Result<Vec<String>, String> {
    let mut out = Vec::new();
    let bin = binary_in(bundle);
    if !bin.is_file() {
        return Err(format!("missing {}", bin.display()));
    }
    out.push(format!("ok  binary            {}", bin.display()));
    let info_path = bundle.join("Contents").join("Resources").join("moduleinfo.json");
    let info = std::fs::read_to_string(&info_path).map_err(|_| format!("missing {}", info_path.display()))?;
    out.push(format!("ok  moduleinfo.json   {}", info_path.display()));
    let r = inspect(&bin)?;
    out.push(format!("ok  factory           vendor \"{}\", {} class(es)", r.vendor, r.classes.len()));
    for c in &r.classes {
        let cid = cid_string(&c.cid);
        if !info.contains(&cid) {
            return Err(format!("moduleinfo.json does not list class {cid}"));
        }
        out.push(format!(
            "ok  class             {} \"{}\" [{}] {} {}  CID {}",
            c.category, c.name, c.subcategories, c.version, c.sdk_version, cid
        ));
    }
    if r.audio_inputs < 1 || r.audio_outputs < 1 {
        return Err(format!("audio busses: {} in, {} out", r.audio_inputs, r.audio_outputs));
    }
    out.push(format!("ok  audio busses      {} in (main + sidechain), {} out", r.audio_inputs, r.audio_outputs));
    Ok(out)
}
