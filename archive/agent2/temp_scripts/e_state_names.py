import json
from pathlib import Path

D = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2\dumps")


def load(data):
    text = data.decode("utf-8", errors="replace")
    return json.loads(text[: text.rfind("}") + 1])


for k in (0, 1, 39, 45, 68):
    for tag in ("cand", "oracle"):
        j = load((D / f"{tag}.program_{k}.bin").read_bytes())
        names = [s.get("name") for s in j.get("snapshots", [])]
        print(f"k={k:2d} {tag:6s} idx={j.get('current_program_index')} snap_names={names} "
              f"descriptions={[s.get('description') for s in j.get('snapshots', [])][:2]} "
              f"keys={sorted(j.keys())}")
    print()
