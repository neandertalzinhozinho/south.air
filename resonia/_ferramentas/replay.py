"""Replay das edicoes Claude (Write/Edit e os poucos sed/heredoc relevantes) para os
arquivos cujo estado final sera reconstruido. So le JSON; nao executa comandos dos registros.

Uso: py -I replay.py <saida_dir>
Grava <saida_dir>/<arquivo>@<HH-MM-SS>.txt apos cada mudanca e um log de conferencias.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import events  # noqa: E402

APP = "D:\\PROJETOS\\soultree\\app\\"
TRACK = {
    "src\\main.rs", "src\\lib.rs", "src\\vst3tool.rs", "src\\vst3host.rs", "src\\equivalence.rs",
    "src\\calibrate.rs", "make_vst3.cmd", "Cargo.toml", "src\\dsp\\curve.rs", "src\\dsp\\detect.rs",
}

files = {}
log = []


def rel(p):
    return p.replace(APP, "") if p.startswith(APP) else None


def check_patch(name, before, sp, ts):
    """Confere as linhas de contexto/removidas de cada hunk contra o arquivo antes da edicao."""
    if not sp:
        return
    lines = before.split("\n")
    for h in sp:
        start = h["oldStart"]
        k = start - 1
        bad = 0
        for ln in h["lines"]:
            if ln.startswith("+"):
                continue
            body = ln[1:]
            if k >= len(lines) or lines[k] != body:
                bad += 1
            k += 1
        log.append("%s %s hunk@%d %s" % (ts, name, start, "OK" if bad == 0 else "DIVERGE(%d)" % bad))


def snap(outdir, name, ts):
    fn = os.path.join(outdir, name.replace("\\", "_") + "@" + ts[11:19].replace(":", "-") + ".txt")
    with open(fn, "w", encoding="utf-8", newline="") as w:
        w.write(files[name])


def heredoc(cmd):
    m = re.search(r"<<'EOF'\n(.*?)\nEOF", cmd, re.S)
    return m.group(1) + "\n"


def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    evs = sorted(events.claude_events(), key=lambda e: e["ts"])
    for e in evs:
        ts, nm, inp = e["ts"], e["name"], e["input"]
        if nm == "Write":
            r = rel(inp["file_path"])
            if r in TRACK:
                if r in files and isinstance(e["tur"], dict) and e["tur"].get("originalFile") is not None:
                    of = e["tur"]["originalFile"]
                    log.append("%s Write %s originalFile %s" % (ts, r, "IGUAL" if of == files[r] else "DIFERENTE"))
                files[r] = inp["content"]
                log.append("%s Write %s len=%d" % (ts, r, len(inp["content"])))
                snap(outdir, r, ts)
        elif nm == "Edit":
            r = rel(inp["file_path"])
            if r in TRACK:
                if r not in files:
                    log.append("%s Edit %s SEM BASE (arquivo da lacuna) - ignorado" % (ts, r))
                    continue
                old, new = inp["old_string"], inp["new_string"]
                cur = files[r]
                if "\r\n" in cur:
                    # a ferramenta Edit preserva o CRLF do arquivo
                    old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
                n = cur.count(old)
                tur = e["tur"] if isinstance(e["tur"], dict) else {}
                check_patch(r, cur.replace("\r\n", "\n"), tur.get("structuredPatch"), ts)
                if n == 0:
                    log.append("%s Edit %s FALHOU: old_string nao encontrado" % (ts, r))
                    continue
                if inp.get("replace_all"):
                    files[r] = cur.replace(old, new)
                else:
                    if n > 1:
                        log.append("%s Edit %s AVISO: old_string aparece %d vezes" % (ts, r, n))
                    files[r] = cur.replace(old, new, 1)
                log.append("%s Edit %s ok" % (ts, r))
                snap(outdir, r, ts)
        elif nm == "Read":
            r = rel(inp.get("file_path", ""))
            tur = e["tur"] if isinstance(e["tur"], dict) else {}
            f = tur.get("file") or {}
            if r in files and "content" in f:
                lines = files[r].replace("\r\n", "\n").split("\n")
                s = f["startLine"]
                got = "\n".join(lines[s - 1:s - 1 + f["numLines"]])
                ok = got == f["content"].replace("\r\n", "\n")
                tot = f.get("totalLines")
                log.append("%s Read %s %d+%d total=%s/%d conteudo %s, total %s" % (
                    ts, r, s, f["numLines"], tot, len(lines), "IGUAL" if ok else "DIFERENTE",
                    "IGUAL" if tot == len(lines) else "DIFERENTE"))
        elif nm in ("Bash", "PowerShell"):
            cmd = inp.get("command", "")
            t = ts[11:19]
            if t == "10:01:01" and ts.startswith("2026-11-21"):
                r = "src\\lib.rs"
                a = "ui::draw(ctx, &mut new, &snapshot, state, &mut |_| {});"
                b = "ui::draw(ctx, &mut new, &snapshot, state, None, &mut |_| {});"
                log.append("%s sed %s casos=%d" % (ts, r, files[r].count(a)))
                files[r] = files[r].replace(a, b)
                snap(outdir, r, ts)
            elif t == "10:01:37" and ts.startswith("2026-11-21"):
                r = "src\\main.rs"
                lines = files[r].split("\n")
                log.append("%s sed main.rs linha231 antes=%r" % (ts, lines[230]))
                lines[230] = ("        // the desktop app opens on a preset so the band nodes are visible with the test sound\n"
                              "        let settings = resonia::settings::factory_presets()[1].1.clone();")
                txt = "\n".join(lines)
                a = "            ui_state: ui::UiState::default(),"
                b = "            ui_state: ui::UiState { preset: 1, ..Default::default() },"
                log.append("%s sed main.rs ui_state casos=%d" % (ts, txt.count(a)))
                files[r] = txt.replace(a, b)
                snap(outdir, r, ts)
            elif t == "01:38:31":
                r = "src\\vst3tool.rs"
                out = []
                for ln in files[r].split("\n"):
                    ln = re.sub(r"^fn com_uid\(", "pub fn com_uid(", ln)
                    ln = re.sub(r"^fn cid_string\(", "pub fn cid_string(", ln)
                    if ln.startswith('extern "system" {'):
                        ln = 'extern "system" {' + ln[len('extern "system" {'):] + \
                            "\n    pub fn LoadLibraryExW(name: *const u16, file: Obj, flags: u32) -> Obj;"
                    out.append(ln)
                out2 = []
                for ln in "\n".join(out).split("\n"):
                    ln = re.sub(r"^    fn LoadLibraryW", "    pub fn LoadLibraryW", ln)
                    ln = re.sub(r"^    fn GetProcAddress", "    pub fn GetProcAddress", ln)
                    ln = re.sub(r"^    fn FreeLibrary", "    pub fn FreeLibrary", ln)
                    out2.append(ln)
                files[r] = "\n".join(out2)
                log.append("%s sed vst3tool.rs aplicado" % ts)
                snap(outdir, r, ts)
            elif t == "01:44:18":
                r = "src\\equivalence.rs"
                # Get-Content (sem EOL final) -> remove indice 330 -> WriteAllLines (CRLF + CRLF final)
                lines = files[r].split("\n")
                if files[r].endswith("\n"):
                    lines = lines[:-1]
                log.append("%s PS remove linha 331 de equivalence.rs: %r" % (ts, lines[330]))
                lines = lines[:330] + lines[331:]
                files[r] = "\r\n".join(lines) + "\r\n"
                snap(outdir, r, ts)
            elif t == "01:50:57":
                r = "src\\calibrate.rs"
                out = []
                for ln in files[r].split("\n"):
                    ln = re.sub(r"^    let mut total = 0\.0;\r?$", "    let mut total = 0.0f64;", ln)
                    ln = re.sub(r"^    let mut count = 0\.0;$", "    let mut count = 0.0f64;", ln)
                    out.append(ln)
                files[r] = "\n".join(out)
                log.append("%s sed calibrate.rs aplicado" % ts)
                snap(outdir, r, ts)
            elif t == "01:56:26":
                r = "src\\calibrate.rs"
                files[r] += heredoc(cmd)
                log.append("%s cat >> calibrate.rs (%d bytes)" % (ts, len(heredoc(cmd))))
                snap(outdir, r, ts)
    with open(os.path.join(outdir, "_log.txt"), "w", encoding="utf-8") as w:
        w.write("\n".join(log) + "\n")
    for k, v in sorted(files.items()):
        b = v.encode("utf-8")
        print(k, "bytes=%d crlf=%d" % (len(b), v.count("\r\n")))
    print("\n".join(log))


if __name__ == "__main__":
    main()
