from pathlib import Path
for p in ["PLANO_MOTOR_AUDIO.md","docs/engine/dsp-spec.md"]:
    t=Path(p).read_text(encoding="utf-8")
    n1=t.count("0.60159128006704898"); n2=t.count("0.70710678118654746")
    t=t.replace("0.60159128006704898","0.601591280067049").replace("0.70710678118654746","0.7071067811865475")
    Path(p).write_text(t,encoding="utf-8")
    print(p,"replaced",n1,n2)
