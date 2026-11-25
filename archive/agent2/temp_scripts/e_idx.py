import json
from pathlib import Path

D = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2\dumps")


def load(data):
    text = data.decode("utf-8", errors="replace")
    end = text.rfind("}")
    return json.loads(text[: end + 1])


rows = []
for k in range(69):
    ja = load((D / f"cand.program_{k}.bin").read_bytes())
    jb = load((D / f"oracle.program_{k}.bin").read_bytes())
    rows.append((k, ja.get("current_program_index"), jb.get("current_program_index"),
                 ja.get("current_snapshot"), jb.get("current_snapshot"),
                 len(ja.get("snapshots", [])), len(jb.get("snapshots", []))))
print("k  cand_idx orc_idx  cand_snap orc_snap  cand_list orc_list  match")
for r in rows:
    print(f"{r[0]:3d} {str(r[1]):>8s} {str(r[2]):>7s}  {str(r[3]):>9s} {str(r[4]):>8s}  "
          f"{r[5]:9d} {r[6]:8d}  {r[1] == r[2]}")
