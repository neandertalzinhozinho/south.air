import pathlib
for p in ["PLANO_MOTOR_AUDIO.md","docs/engine/dsp-spec.md","PROMPT_RETOMADA.md"]:
    b=pathlib.Path(p).read_bytes()
    print(p, len(b), "BOM" if b[:3]==b"\xef\xbb\xbf" else "noBOM")
    try:
        b.decode("utf-8"); print("   utf-8 OK")
    except Exception as e:
        print("   utf-8 FAIL", e)
    # sample non-ascii
    na=[i for i,c in enumerate(b) if c>127][:5]
    print("   first non-ascii bytes", [(i,hex(b[i])) for i in na])
