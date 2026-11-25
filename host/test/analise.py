# analise.py — compara o WAV de entrada com o WAV gerado pelo host.
#
# Uso:
#   py analise.py <entrada.wav> <saida.wav>
#
# Não faz parte do host; é só uma lupa para o null-test da etapa I. Lê os dois
# arquivos, confere formato/contagem e procura o atraso que melhor alinha a
# saída à entrada (correlação cruzada), para separar "atraso" de "processamento".

import math
import struct
import sys


def ler_wav(caminho):
    dados = open(caminho, "rb").read()
    if dados[0:4] != b"RIFF" or dados[8:12] != b"WAVE":
        raise SystemExit(f"{caminho}: não é RIFF/WAVE")
    pos = 12
    fmt = None
    audio = None
    while pos + 8 <= len(dados):
        cid = dados[pos:pos + 4]
        tam = struct.unpack_from("<I", dados, pos + 4)[0]
        corpo = pos + 8
        if cid == b"fmt ":
            tag, canais, taxa = struct.unpack_from("<HHI", dados, corpo)
            bits = struct.unpack_from("<H", dados, corpo + 14)[0]
            if tag == 0xFFFE:
                tag = struct.unpack_from("<H", dados, corpo + 24)[0]
            fmt = (tag, canais, taxa, bits)
        elif cid == b"data":
            audio = dados[corpo:corpo + tam]
        pos = corpo + tam + (tam & 1)
    if fmt is None or audio is None:
        raise SystemExit(f"{caminho}: falta 'fmt ' ou 'data'")
    tag, canais, taxa, bits = fmt
    n = len(audio) // (bits // 8 * canais)
    amostras = []
    for i in range(n):
        quadro = []
        for c in range(canais):
            off = (i * canais + c) * (bits // 8)
            if tag == 3 and bits == 32:
                v = struct.unpack_from("<f", audio, off)[0]
            elif tag == 3 and bits == 64:
                v = struct.unpack_from("<d", audio, off)[0]
            elif tag == 1 and bits == 16:
                v = struct.unpack_from("<h", audio, off)[0] / 32768.0
            elif tag == 1 and bits == 24:
                b = audio[off:off + 3]
                x = (b[2] << 24 | b[1] << 16 | b[0] << 8) >> 8
                v = x / 8388608.0
            elif tag == 1 and bits == 32:
                v = struct.unpack_from("<i", audio, off)[0] / 2147483648.0
            else:
                raise SystemExit(f"{caminho}: formato tag={tag} bits={bits} não tratado")
            quadro.append(v)
        amostras.append(quadro)
    return {"tag": tag, "canais": canais, "taxa": taxa, "bits": bits,
            "quadros": n, "amostras": amostras}


def pico_rms(canal):
    pico = max((abs(v) for v in canal), default=0.0)
    rms = math.sqrt(sum(v * v for v in canal) / len(canal)) if canal else 0.0
    return pico, rms


def db(x):
    return 20.0 * math.log10(x) if x > 0 else float("-inf")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("uso: py analise.py <entrada.wav> <saida.wav>")
    ent = ler_wav(sys.argv[1])
    sai = ler_wav(sys.argv[2])

    print(f"entrada: {ent['quadros']} quadros, {ent['canais']} ch, {ent['taxa']} Hz, "
          f"tag={ent['tag']} bits={ent['bits']}")
    print(f"saída  : {sai['quadros']} quadros, {sai['canais']} ch, {sai['taxa']} Hz, "
          f"tag={sai['tag']} bits={sai['bits']}")
    if ent["quadros"] != sai["quadros"]:
        print("ATENÇÃO: contagem de quadros diferente!")

    n = min(ent["quadros"], sai["quadros"])
    for rotulo, w in (("entrada", ent), ("saída", sai)):
        for c in range(min(2, w["canais"])):
            canal = [w["amostras"][i][c] for i in range(n)]
            pico, rms = pico_rms(canal)
            ruim = sum(1 for v in canal if not math.isfinite(v))
            print(f"  {rotulo} ch{c}: pico {pico:.6f} ({db(pico):.1f} dBFS), "
                  f"RMS {rms:.6f} ({db(rms):.1f} dBFS), não-finitos={ruim}")

    a = [ent["amostras"][i][0] for i in range(n)]
    b = [sai["amostras"][i][0] for i in range(n)]

    identico = all(x == y for x, y in zip(a, b))
    print(f"L idêntico bit-a-bit: {identico}")

    # Correlação cruzada: acha o atraso 'd' (saída atrasada em relação à entrada).
    max_lag = min(6000, n - 1)
    melhor_lag, melhor_corr = 0, float("-inf")
    for d in range(max_lag + 1):
        m = n - d
        if m <= 0:
            break
        num = sum(a[i] * b[i + d] for i in range(m))
        den = math.sqrt(sum(a[i] * a[i] for i in range(m)) *
                        sum(b[i + d] * b[i + d] for i in range(m)))
        corr = num / den if den > 0 else 0.0
        if corr > melhor_corr:
            melhor_corr, melhor_lag = corr, d
    print(f"melhor atraso saída-entrada: {melhor_lag} amostras "
          f"(correlação normalizada {melhor_corr:.6f})")

    # Ganho escalar ótimo e resíduo no alinhamento escolhido.
    d = melhor_lag
    m = n - d
    num = sum(a[i] * b[i + d] for i in range(m))
    den = sum(a[i] * a[i] for i in range(m))
    g = num / den if den > 0 else 0.0
    res = [b[i + d] - g * a[i] for i in range(m)]
    rms_res = math.sqrt(sum(v * v for v in res) / m)
    rms_out = math.sqrt(sum(b[i + d] ** 2 for i in range(m)) / m)
    print(f"ganho escalar ótimo no alinhamento: {g:.6f} "
          f"({db(abs(g)):.1f} dB); resíduo RMS {db(rms_res):.1f} dBFS "
          f"({db(rms_res) - db(rms_out):+.1f} dB relativo à saída)")

    # Diferença crua, sem alinhar.
    dif = max(abs(b[i] - a[i]) for i in range(n))
    print(f"diferença crua saída-entrada (L): pico {dif:.6f} ({db(dif):.1f} dBFS)")


if __name__ == "__main__":
    main()
