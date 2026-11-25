import pathlib

p = pathlib.Path('checks/fft_stage_probe.rs')
t = p.read_text(encoding='utf-8')
t = t.replace('''const RVA_KERNEL6: usize = 0x8BFE0;''', '''const RVA_KERNEL6: usize = 0x8BFE0;
const RVA_KERNEL7: usize = 0x8C280;''')
t = t.replace('''    let order: i32 = std::env::args()
        .nth(1)
        .map(|s| s.parse().unwrap())
        .unwrap_or(6);
    assert_eq!(order, 6, "por enquanto só ordem 6 (kernel 0x8BFE0)");''', '''    let order: i32 = std::env::args()
        .nth(1)
        .map(|s| s.parse().unwrap())
        .unwrap_or(6);
    // 0007258C: ordem <= 7 usa a tabela 0x1DFA358; 6 -> 0x8BFE0, 7 -> 0x8C280.
    let rva_kernel = match order {
        6 => RVA_KERNEL6,
        7 => RVA_KERNEL7,
        _ => panic!("kernel de ordem {order} ainda NAO EXTRAIDO"),
    };''')
t = t.replace('''    let kernel: FnKernel = unsafe { std::mem::transmute(base + RVA_KERNEL6) };''', '''    let kernel: FnKernel = unsafe { std::mem::transmute(base + rva_kernel) };''')
t = t.replace('''    let mut tw = Vec::new();
    for i in 0..64usize {''', '''    let mut tw = Vec::new();
    for i in 0..(2 * n) {''')
t = t.replace('''    println!("escrito {path} (TW = 64 u32 de ctx+0x50)");''', '''    println!("escrito {path} (TW = {} u32 de ctx+0x50, 2*n)", tw.len());''')
p.write_text(t, encoding='utf-8')
print('ok')
