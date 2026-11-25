import sqlite3, os, binascii

p = r"C:\ProgramData\PACE\Eden\com.paceap.eden.clientdb.v1.01.sdb"
head = open(p, "rb").read(512)
print("magic:", head[:16])
print("hex:", head[:64].hex())
print("sqlite?", head.startswith(b"SQLite format 3\x00"))

for f in range(1, 6):
    fp = rf"C:\ProgramData\PACE\Eden\LdLogs\LdLog_00000{f}.txt"
    print(f"=== {os.path.basename(fp)} ===")
    print(open(fp, encoding="utf-8", errors="replace").read())
