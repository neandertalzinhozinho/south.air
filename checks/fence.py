from pathlib import Path
for p in ["PLANO_MOTOR_AUDIO.md","docs/engine/dsp-spec.md","PROMPT_RETOMADA.md"]:
    t=Path(p).read_text(encoding="utf-8")
    print(p, "fences", t.count("```"), "odd!" if t.count("```")%2 else "ok", "lines", t.count(chr(10)))
