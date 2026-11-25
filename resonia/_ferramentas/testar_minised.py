"""Testa minised.py contra saidas conhecidas dos registros (somente leitura/dados).

Uso: py -I testar_minised.py
Casos: (a) sed 01:54:26 em curve.rs final; (b) sed 01:54:41 sobre stft (montado) = grep conhecido;
(c) sed 01:55:08 'c/i' em texto sintetico; (d) sed 10:02:15 '93,94c\' em texto sintetico.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import minised as ms  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok_all = True


def check(nome, cond, det=""):
    global ok_all
    ok_all &= bool(cond)
    print(("OK    " if cond else "FALHA ") + nome + (" " + det if det else ""))


# (a) curve.rs final contem o resultado; reaplicar o sed deve ser idempotente e dar o sed -n 114,122p
cur = open(os.path.join(ROOT, "app", "src", "dsp", "curve.rs"), encoding="utf-8", newline="").read()
r, n = ms.run(cur, ["120s|.*|    lo.max(0.01).powf(wl) * hi.max(0.01).powf(wh)|"])
r, n2 = ms.run(r, ["s|^/// Tilt scaling: 0 below/above nothing.*|/// Tilt scaling: a multiplier (1.0x = none) that acts gradually under 500 Hz and above 2 kHz.|"])
NL = chr(10)
trecho = NL.join(r.split(NL)[113:122]).rstrip(NL)
esperado = """}

/// Tilt scaling: a multiplier (1.0x = none) that acts gradually under 500 Hz and above 2 kHz.
pub(crate) fn tilt_factor(f: f32, lo: f32, hi: f32) -> f32 {
    let wl = ((TILT_LOW_HZ / f.max(1.0)).log2() / (TILT_LOW_HZ / 20.0).log2()).clamp(0.0, 1.0);
    let wh = ((f / TILT_HIGH_HZ).log2() / (20000.0 / TILT_HIGH_HZ).log2()).clamp(0.0, 1.0);
    lo.max(0.01).powf(wl) * hi.max(0.01).powf(wh)
}"""
check("a) curve.rs linhas 114-122 (sed 01:54:26)", trecho == esperado)

# (b) idem do sed 01:54:41: o stft final tem as 3 substituicoes; reaplicar nao deve achar ancora nova
st = open(os.path.join(ROOT, "app", "src", "dsp", "stft.rs"), encoding="utf-8", newline="").read()
base = st.replace("use super::curve::{self, Tuning};", "use super::curve::{self, DETAIL_WIDTH_AT_0, DETAIL_WIDTH_AT_100, REFERENCE_WIDTH_OCT};", 1)
exprs = [
    "s|^use super::curve::{self, DETAIL_WIDTH_AT_0, DETAIL_WIDTH_AT_100, REFERENCE_WIDTH_OCT};|use super::curve::{self, Tuning};|",
]
r, n = ms.run(base, exprs)
check("b) stft: troca de use (sed 01:54:41)", r == st and n == 1, "n=%d" % n)

# (c) sed -E '257,262s/: 0\.0,/: 1.0,/' + '132i\' com \n e \&
pre = "\n".join("l%d" % i for i in range(1, 140)) + "\n"
r, n = ms.run(pre, [r'132i\        if self.name == "Max cut" \&\& v >= self.max {\n            return "off".to_string();\n        }'])
L = r.split("\n")
check("c) 132i\ insere 3 linhas antes da 132", L[131].strip().startswith("if self.name") and "&&" in L[131] and L[133].strip() == "}" and L[134] == "l132", repr(L[131:135]))
t2 = "\n".join(["x"] * 256 + ["  detail_lo: 0.0,", "  mix: 0.0,"] + ["y"] * 5 + ["  z: 0.0,"]) + "\n"
r, n = ms.run(t2, [r"257,262s/: 0\.0,/: 1.0,/"], ere=True)
R = r.split("\n")
check("c2) faixa 257,262s (ERE)", R[256] == "  detail_lo: 1.0," and R[257] == "  mix: 1.0," and R[-2] == "  z: 0.0,", repr(R[256:258]))

# (d) 93,94c\ (duas linhas viram duas linhas novas)
pre = "\n".join("l%d" % i for i in range(1, 100)) + "\n"
r, n = ms.run(pre, [r"93,94c\            let h = ui.available_height().max(160.0);\n            ui.horizontal(|ui| {"])
L = r.split("\n")
check("d) 93,94c\ troca o intervalo por 2 linhas", L[91] == "l92" and L[92].strip().startswith("let h") and L[93].strip().startswith("ui.horizontal") and L[94] == "l95", repr(L[91:95]))
print("RESULTADO:", "TUDO OK" if ok_all else "HA FALHAS")
