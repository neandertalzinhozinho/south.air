"""Gera app/src/param_table.rs a partir de parameter_table_143_params.json (dado nao confiavel: so leitura).

Uso: py -I gerar_param_table.py <json> <saida.rs>
Nao inventa nada: cada campo vem do JSON; o que o JSON nao prova fica marcado NAO PROVADO.
"""
import hashlib
import json
import sys

src, out = sys.argv[1], sys.argv[2]
raw = open(src, "rb").read()
d = json.loads(raw.decode("utf-8"))
P = d["parameters"]
assert len(P) == 143 and [p["id"] for p in P] == list(range(143))
E = d["validated_enum_tables"]

# formatadores (campo +88) que identificam enums/bools; vem do proprio JSON
FMT_BOOL = 0x335F40
FMT_ENUM = {0x3366A0: "BandShape", 0x3367D0: "StereoMode", 0x3369A0: "Quality", 0x336610: "BandChannels"}


def rva(p, off):
    for x in p["pointers"]:
        if x["field_offset"] == off:
            return int(x["rva"], 16)
    return 0


def f(x):
    r = repr(float(x))
    return r


lines = []
w = lines.append
w("//! GERADO por `resonia/_ferramentas/gerar_param_table.py`. NAO EDITAR A MAO.")
w("//!")
w("//! Fonte: `RECURSOS_VALIDADOS_recuperados/parameter_table_143_params.json`")
w("//! (SHA-256 do arquivo: %s)." % hashlib.sha256(raw).hexdigest())
w("//! Tabela de 143 descritores em `0x238E9C0` (registros de 0x68 B), lida do dump 1.0.6")
w("//! em 2026-11-25 (docs/engine/recursos-recuperados.md 2.4).")
w("//!")
w("//! Provado (2.4): ids 0..142, nomes, minimo, maximo, flags, ponteiros de callback.")
w("//! `NAO PROVADO`: (a) que `default` seja o estado inicial gravado pelo motor (o JSON o chama")
w("//! `initial_or_default_candidate`); (b) a curva normalizado<->valor de todo parametro cujo")
w("//! callback `+72` nao e `0x3351A0` (ver `Curve`); (c) o significado das flags; (d) rotulos de")
w("//! `Mode` (id 2) e `Band solo` (id 91): o formatador nao foi resolvido; (e) a classe `Kind`,")
w("//! que e so a escolha de controle para o host/GUI (pelo formatador `+88`).")
w("")
w("/// Controle exposto ao host/GUI. Derivado do formatador `+88` e dos limites; nao e prova de semantica.")
w("#[derive(Clone, Copy, Debug, PartialEq, Eq)]")
w("pub enum Kind {")
w("    /// Contínuo.")
w("    Float,")
w("    /// 0/1 (formatador `0x335F40`).")
w("    Bool,")
w("    /// Inteiro discreto sem tabela de rótulos provada.")
w("    Int,")
w("    /// Inteiro com tabela de rótulos lida do dump.")
w("    Enum(EnumTable),")
w("}")
w("")
w("#[derive(Clone, Copy, Debug, PartialEq, Eq)]")
w("pub enum EnumTable {")
for n in ("BandShape", "StereoMode", "Quality", "BandChannels"):
    w("    %s," % n)
w("}")
w("")
w("/// Curva normalizado<->valor.")
w("#[derive(Clone, Copy, Debug, PartialEq, Eq)]")
w("pub enum Curve {")
w("    /// `cb+72 = 0x3351A0`, `cb+80 = 0x3351E0`: (x-min)/(max-min) e inversa, PROVADO (2.4).")
w("    Linear,")
w("    /// Outro callback: curva NAO PROVADA. O host usa mapeamento linear provisório.")
w("    NaoProvado,")
w("}")
w("")
w("#[derive(Clone, Copy, Debug)]")
w("pub struct ParamSpec {")
w("    pub id: u32,")
w("    pub name: &'static str,")
w("    pub min: f64,")
w("    pub max: f64,")
w("    /// `initial_or_default_candidate`: NAO PROVADO como estado inicial do motor.")
w("    pub default: f64,")
w("    pub flags: u64,")
w("    pub kind: Kind,")
w("    pub curve: Curve,")
w("    /// RVAs (dump 1.0.6) dos 4 callbacks: valor->normalizado, normalizado->valor, formatador, parser.")
w("    pub callbacks: [u32; 4],")
w("}")
w("")
for key, ty, nm in (("band_shape", "BAND_SHAPE_LABELS", "BandShape"), ("stereo_mode", "STEREO_MODE_LABELS", "StereoMode"),
                    ("quality", "QUALITY_LABELS", "Quality"), ("band_channels", "BAND_CHANNELS_LABELS", "BandChannels")):
    vals = E[key]["values"]
    assert [v["value"] for v in vals] == list(range(len(vals)))
    w("/// Rótulos lidos do dump (tabela `%s`)." % key + (" Rótulos de quality/band_channels: NAO reconferidos no 1.0.6 (INCERTO)." if key in ("quality", "band_channels") else ""))
    w("pub const %s: [&str; %d] = [%s];" % (ty, len(vals), ", ".join(json.dumps(v["label"]) for v in vals)))
    w("")
w("pub const PARAM_COUNT: usize = 143;")
w("")
w("pub static PARAMS: [ParamSpec; PARAM_COUNT] = [")
for p in P:
    cb = [rva(p, o) for o in (72, 80, 88, 96)]
    mn, mx, df = p["minimum"], p["maximum"], p["initial_or_default_candidate"]
    flags = int(p["flags_raw_u64"], 16)
    if cb[2] in FMT_ENUM:
        kind = "Kind::Enum(EnumTable::%s)" % FMT_ENUM[cb[2]]
    elif cb[2] == FMT_BOOL and mn == 0 and mx == 1:
        kind = "Kind::Bool"
    elif cb[0] == 0x335240 and float(mn).is_integer() and float(mx).is_integer():
        kind = "Kind::Int"
    else:
        kind = "Kind::Float"
    curve = "Curve::Linear" if (cb[0] == 0x3351A0 and cb[1] == 0x3351E0) else "Curve::NaoProvado"
    w("    ParamSpec { id: %d, name: %s, min: %s, max: %s, default: %s, flags: 0x%X, kind: %s, curve: %s, callbacks: [0x%X, 0x%X, 0x%X, 0x%X] }," % (
        p["id"], json.dumps(p["name"]), f(mn), f(mx), f(df), flags, kind, curve, *cb))
w("];")
w("")
open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("ok", len(P), "parametros ->", out)
