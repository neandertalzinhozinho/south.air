# RETOMADA — DSP do soothe3

Continuar a extração estática do DSP do soothe3 de onde parou. Prova = instrução com RVA; decompilado é leitura. Proibido estimar, inventar nome, "algoritmo equivalente", ajustar até o null-test bater, inferir por nome de parâmetro, hook/Frida/patch. Não lido = `NÃO EXTRAÍDO`.

Entrega só conta com 5 itens por função: (a) RVA, (b) desmontagem/pseudocódigo comentado, (c) constantes com RVA, (d) structs com offsets provados, (e) código com a mesma aritmética, ordem e coeficientes. Detalhe de cada etapa: `PLANO_MOTOR_AUDIO.md` §23.

Fonte: `dumpsooth\nyx_soothe3_dump.bin` (SHA-256 68D30368…) → `soothe3_unpacked.dll` (ImageBase 0x180000000, 30.859 funções). IDA: `C:\Users\tromb\AppData\Local\Temp\opencode\ida_pe\soothe3_pe.dll.i64`. `original\soothe3.vst3` não é fonte (.text cifrado). `LEMBRAR DISSO.md` é congelado (hash D10EB33…); divergência → registre em §23.14, não edite.

## Estado

Fechados: 0x8C1440 (buffer); 0x8C02F0 e 0x8C0BD0 (plumbing — descritores de 24 B, +8 ptr, +16 tipo, cadeia 0x1190→0x10D0/0x1370→0x1100→0x1550→0x1220→0x11F0). Varredura chain-aware 0x8A0000–0x8E0000: 0 FMA, 90 mulss/57 addss/50 subss/19 divss.

Achado, não lido: **0x8B2C30** — 1.163 B, 300 insns, 27 mulss + 27 addss, 0 call, `[rcx+0x80]`, `ebx=0x1f`, `and r8,~3`.

## Agora (D0)

```
py -3 tools\show_func.py 0x8B2C30 > checks\8b2c30.dis
py -3 -c "open(r'tools\ida\batch_list.txt','w').write('0x8B2C30\n')"
powershell -File tools\ida\run_batch.ps1
```

Responda com instrução e RVA: a entrada é 0x8B2C30 (prólogo `mov [rsp+0x18],rbx` / `sub rsp,0x10`; .pdata parte em 0x8B2BCE/0x8B2BD6/0x8B2C30/0x8B2C55)? O que é `[rcx+0x80]`? `0x1f` é máscara? 27 taps de quê? É filtro por banda? Se não for, prove e siga.

## Depois

A 0x8CAE90 (245 B) · B ordem dos args de 0x63640, 0x5BC0, 0x4BC0, 0x2F60, 0xA120, 0x3480, 0x6160, 0x11C0, 0x1250 → §17.6 · C struct de 24 B (quem preenche) · F tipo de filtro: 0x87BB60→0x882FC0, 0x87E220 · D1 0x8BF650/0x8BFD30 · E 0x8C33D0 · G estado ctx+0x2C38/+0xBFF8/+0x5F8/+0x5ED0 + 143 params · H dsp-spec · I oráculo (bloqueado: LoadLibrary morre 0xC0000005 no DllMain) · J port.

## Armadilhas

- `functions.csv` mente: 0x8B3ED0 = 49 B no CSV, 20.209 B real. Use `show_func.py` / `scan_region.py`.
- 0x8B660 (570 KB, IPP) ≠ 0x8B3ED0 (9 MB, DSP). Conte os dígitos.
- Gêmeo começa em 0x8C5C40; 0x8C5FD8 é fragmento.
- `xrefs.csv` é latin1.
- `reach_kernels.py` descartado; `find_kernels.py` subconta.
- `auto_wait()` trava; use `plan_and_wait`. `decompile_batch.py` grava `ida_%08X.c` (não mude).
- Latência 2.304 @48 kHz é do 1.0.5, não do dump.
- `archive/agent2/oracle_bundle_1.0.5/` é v1.0.5 — não meça nada nele; o dump é 1.0.6.
- N=256/278/557 = round(256×fs/44100); a instrução ainda não foi lida.

## Registro

Cada etapa: atualize §23.x do `PLANO_MOTOR_AUDIO.md` e a `dsp-spec.md` (só o que tem RVA). Toda afirmação técnica leva RVA. Pronto = D0 fechada com prova e o plano atualizado, com a etapa A marcada como próxima.
