import difflib

a = open(r"C:\Users\tromb\AppData\Local\Temp\opencode\i5_params_expected.h", encoding="utf-8").read().splitlines()
b = open(r"D:\PROJETOS\shadowFILES\soultea3_plugin\Source\Soultea3Parameters.h", encoding="utf-8").read().splitlines()
print("lines expected=%d i1=%d" % (len(a), len(b)))
diff = list(difflib.unified_diff(a, b, fromfile="EXPECTED", tofile="I1", lineterm="", n=1))
print("diff lines:", len(diff))
for line in diff[:200]:
    print(line)
