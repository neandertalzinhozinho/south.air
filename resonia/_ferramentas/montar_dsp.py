"""Monta dsp/stft.rs (Read 01:53:47 + grep 01:48:36 + edicoes 01:54:37..44) e dsp/envelope.rs (cat 01:48:36).

Uso: py -I montar_dsp.py <saida_dir>
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import events  # noqa: E402

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
ev = {e["ts"][11:19]: e for e in events.claude_events() if e["ts"].startswith("2026-11-22")}

# --- stft.rs base
rd = ev["01:53:47"]["tur"]["file"]
assert rd["startLine"] == 1 and rd["numLines"] == 198 and rd["totalLines"] == 312
head = rd["content"].split("\n")
cat = ev["01:48:36"]["tur"]["stdout"]
i0 = cat.index("199:    pub(crate) fn process_frame")
tail = []
for ln in cat[i0:].split("\n"):
    m = re.match(r"^(\d+)[:-](.*)$", ln)
    assert m, ln
    tail.append((int(m.group(1)), m.group(2)))
assert [n for n, _ in tail] == list(range(199, 312)), (tail[0][0], tail[-1][0])
lines = head + [t for _, t in tail]
base = "\n".join(lines) + "\n"
print("stft base: linhas=%d bytes=%d (ls 01:41: 11298)" % (len(lines), len(base.encode())))

# Edit 01:54:37
e = ev["01:54:37"]["input"]
assert base.count(e["old_string"]) == 1
t = base.replace(e["old_string"], e["new_string"], 1)
# sed 01:54:41 (tres substituicoes de linha inteira ancoradas em ^)
L = t.split("\n")
o = []
for ln in L:
    if ln == "use super::curve::{self, DETAIL_WIDTH_AT_0, DETAIL_WIDTH_AT_100, REFERENCE_WIDTH_OCT};" or \
            ln.startswith("use super::curve::{self, DETAIL_WIDTH_AT_0, DETAIL_WIDTH_AT_100, REFERENCE_WIDTH_OCT};"):
        ln = "use super::curve::{self, Tuning};" + ln[len("use super::curve::{self, DETAIL_WIDTH_AT_0, DETAIL_WIDTH_AT_100, REFERENCE_WIDTH_OCT};"):]
    o.append(ln)
L = o
o = []
for ln in L:
    if ln.startswith("    cached: Option<Settings>,"):
        ln = ("    cached: Option<Settings>,\n    /// Detection power averaged over time, per channel.\n"
              "    pub(crate) det_state: Vec<Vec<f32>>,\n    pub(crate) det_coef: f32,\n"
              "    /// Detection power and its wide average, linear.\n    pub(crate) det_lin: Vec<f32>,\n"
              "    pub(crate) ref_lin: Vec<f32>,\n    pub(crate) tuning: Tuning,") + ln[len("    cached: Option<Settings>,"):]
    elif ln.startswith("            cached: None,"):
        ln = ("            cached: None,\n            det_state: ch(bins),\n            det_coef: 0.0,\n"
              "            det_lin: vec![0.0; bins],\n            ref_lin: vec![0.0; bins],\n"
              "            tuning: Tuning::CALIBRATED,") + ln[len("            cached: None,"):]
    elif ln.startswith("            .chain(self.reduction.iter_mut())"):
        ln = "            .chain(self.reduction.iter_mut())\n            .chain(self.det_state.iter_mut())" + \
            ln[len("            .chain(self.reduction.iter_mut())"):]
    o.append(ln)
t = "\n".join(o)
L = t.split("\n")
# conferencia com o grep de 01:54:41
for n, want in [(68, "    pub(crate) det_state: Vec<Vec<f32>>,"), (73, "    pub(crate) tuning: Tuning,"),
                (121, "            det_state: ch(bins),"), (125, "            tuning: Tuning::CALIBRATED,"),
                (143, "            .chain(self.det_state.iter_mut())"), (159, "        let t = curve::tuning();"),
                (175, "        self.tuning = t;"), (279, "                s.max_reduction,")]:
    print("  linha %d %s" % (n, "OK" if L[n - 1] == want else "DIFERE: %r" % L[n - 1]))
# sed 01:54:44
assert L[278] == "                s.max_reduction,"
L[278] = "                if s.max_reduction >= MAX_RED.max { f32::INFINITY } else { s.max_reduction },"
t = "\n".join(L)
print("stft final: bytes=%d (esperado 12007)" % len(t.encode()))
open(os.path.join(out, "stft.rs"), "w", encoding="utf-8", newline="").write(t)

# --- envelope.rs
j0 = cat.index("//! Attack/release smoothing")
j1 = cat.index("//! The depth curve")
env = cat[j0:j1]
print("envelope: bytes=%d (esperado 998)" % len(env.encode()))
open(os.path.join(out, "envelope.rs"), "w", encoding="utf-8", newline="").write(env)
