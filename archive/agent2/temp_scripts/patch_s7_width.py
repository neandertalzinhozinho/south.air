p = r'D:\PROJETOS\shadowFILES\analysis\tools\s7_gui_probe\src\main.rs'
s = open(p, encoding='utf-8').read()

old1 = "    let width = rect.right - rect.left;\n    let height = rect.bottom - rect.top;\n"
new1 = (
    "    let mut width = rect.right - rect.left;\n"
    "    let height = rect.bottom - rect.top;\n"
    "    // Optional S7_WIDTH reproduces the exact editor width the reference was\n"
    "    // captured at; the layout is width-sensitive.\n"
    "    let force_w: Option<i32> = std::env::var(\"S7_WIDTH\").ok().and_then(|v| v.trim().parse().ok());\n"
)
assert old1 in s
s = s.replace(old1, new1, 1)

old2 = '    assert_eq!(attach_res, 0, "attached failed");\n'
new2 = (
    '    assert_eq!(attach_res, 0, "attached failed");\n'
    "\n"
    "    if let Some(w) = force_w {\n"
    "        if w != width {\n"
    "            SetWindowPos(hwnd, null_mut(), 50, 50, w, height, 0x0004);\n"
    "            let mut vr = ViewRect { left: 0, top: 0, right: w, bottom: height };\n"
    "            let on_size: unsafe extern \"C\" fn(P, *mut ViewRect) -> i32 = std::mem::transmute(slot(p, 10));\n"
    "            let rs = on_size(p, &mut vr);\n"
    "            emit(json!({\"event\":\"onSize\",\"status\":rs,\"width\":w,\"height\":height}));\n"
    "            pump_messages(80, 10);\n"
    "            width = w;\n"
    "            emit(json!({\"event\":\"resized\",\"width\":width}));\n"
    "        }\n"
    "    }\n"
)
assert old2 in s
s = s.replace(old2, new2, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched ok')
