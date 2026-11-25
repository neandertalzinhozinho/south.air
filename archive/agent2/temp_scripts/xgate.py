import json
import os

os.chdir(r'D:\PROJETOS\shadowFILES')
A = 'analysis/startup_audit/'
REGIONS = [("data", 0x217F000), ("data001", 0x79CD000), ("rdata01", 0x79CC000), ("text001", 0x79CA000)]
rd = lambda p: open(p, 'rb').read()

o = [rd(f'{A}xA_create_r{i}_{r}.bin') for r in (n for n, _ in REGIONS) for i in (1, 2, 3)]
c = [rd(f'{A}xC273_create_r{i}_{r}.bin') for r in (n for n, _ in REGIONS) for i in (1, 2, 3)]

out = {}
tot_res = tot_floor_o = tot_floor_c = 0
for k, (name, rva) in enumerate(REGIONS):
    orun = o[k * 3:k * 3 + 3]
    crun = c[k * 3:k * 3 + 3]
    n = len(orun[0])
    assert all(len(x) == n for x in orun + crun), name
    fo = {i for i in range(n) if not (orun[0][i] == orun[1][i] == orun[2][i])}
    fc = {i for i in range(n) if not (crun[0][i] == crun[1][i] == crun[2][i])}
    mask = fo | fc
    res = {i for i in range(n) if crun[0][i] != orun[0][i]} - mask
    # cross-check 9/9
    cross = set()
    for a in crun:
        for b in orun:
            cross.add(len({i for i in range(n) if a[i] != b[i]} - mask))
    out[name] = {
        "rva": hex(rva), "bytes": n,
        "floor_oracle": len(fo), "floor_candidate": len(fc), "union": len(mask),
        "residual": len(res),
        "class": {"cand_zero_orac_nz": sum(1 for i in res if crun[0][i] == 0 and orun[0][i]),
                  "both_nz": sum(1 for i in res if crun[0][i] and orun[0][i]),
                  "extra": sum(1 for i in res if crun[0][i] and not orun[0][i])},
        "cross_check_residuals": sorted(cross),
    }
    tot_res += len(res)
    tot_floor_o += len(fo)
    tot_floor_c += len(fc)

out["total"] = {"floor_oracle": tot_floor_o, "floor_candidate": tot_floor_c,
                "residual_outside_union": tot_res,
                "verdict": "S3 NAO APROVADO" if tot_res else "S3 APROVADO (byte equality fora do piso)"}
out["method"] = ("3 capturas do build A e 3 execucoes do candidato (receita 273) no mesmo ponto "
                 "load->inits->InitDll->factory->createInstance classe 0; piso = bytes que variam entre as 3; "
                 "mascara = uniao dos dois pisos; residual = divergencia fora da mascara")
out["data001_finding"] = {"oracle_nonzero": 400, "candidate_nonzero": 27,
                          "note": "o candidato nao escreve o bloco PACE/iLok; ver s3_tls_builder_gap.json"}
open(f'{A}xgate_12h55.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
for k, v in out.items():
    if isinstance(v, dict):
        print(k, json.dumps({x: v[x] for x in v if x in ("floor_oracle", "floor_candidate", "union", "residual", "class", "cross_check_residuals", "residual_outside_union", "verdict")}, ensure_ascii=False))
