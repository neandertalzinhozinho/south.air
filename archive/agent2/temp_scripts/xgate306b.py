import collections
import json
import os

os.chdir(r'D:\PROJETOS\shadowFILES')
A = 'analysis/startup_audit/'
rd = lambda p: open(p, 'rb').read()
o = [rd(f'{A}xA_create_r{i}_data.bin') for i in (1, 2, 3)]
c = [rd(f'{A}xC306_create_r{i}_data.bin') for i in (1, 2, 3)]
n = len(o[0])
fo = {i for i in range(n) if not (o[0][i] == o[1][i] == o[2][i])}
fc = {i for i in range(n) if not (c[0][i] == c[1][i] == c[2][i])}
res = sorted({i for i in range(n) if c[0][i] != o[0][i]} - (fo | fc))
m = json.load(open(A + 's3_residual_mass_audit.json', encoding='utf-8'))
ua = {int(u['offset'], 16) if isinstance(u, dict) and isinstance(u['offset'], str) else int(u) for u in m['unattributed_offsets']}
rng = []
st = pr = res[0]
for x in res[1:]:
    if x == pr + 1:
        pr = x
    else:
        rng.append((st, pr))
        st = pr = x
rng.append((st, pr))
rng.sort(key=lambda t: t[1] - t[0], reverse=True)

doc = json.load(open(f'{A}xgate_306.json', encoding='utf-8'))
doc['residual_detail'] = {
    "total": len(res),
    "class": {"candidato_zero": sum(1 for i in res if c[0][i] == 0 and o[0][i]),
              "ambos_nao_zero": sum(1 for i in res if c[0][i] and o[0][i]),
              "extra": sum(1 for i in res if c[0][i] and not o[0][i])},
    "pages": [{"rva": hex(0x217F000 + (k << 12)), "bytes": v} for k, v in collections.Counter(i >> 12 for i in res).most_common(10)],
    "faixas_maiores": [{"inicio_off": hex(s), "rva": hex(0x217F000 + s), "bytes": e - s + 1,
                        "oraculo": o[0][s:e + 1].hex()[:40], "candidato": c[0][s:e + 1].hex()[:40]}
                       for s, e in rng[:10]],
    "atribuicao": {"coincide_com_unattributed_do_S3_MASS": len(ua & set(res)),
                   "unattributed_no_relatorio": len(ua),
                   "fora_do_relatorio": len(res) - len(ua & set(res))},
    "leitura": ("as maiores faixas restantes sao as strings de licenciamento/PACE "
                "(LicenseDbRemote, IlokCloudRemote, iLok2Remote, iLok3Remote, LicenseDb, ImlIasm_) - "
                "o mesmo subsistema cujo estado o builder descartou em .data001 e cuja cadeia de init "
                "(__dyn_tls_init) ele desligou")
}
json.dump(doc, open(f'{A}xgate_306.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(doc['residual_detail'], ensure_ascii=False, indent=1)[:1500])
