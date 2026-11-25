p = r'D:\PROJETOS\shadowFILES\RELATORIO_CONTINUIDADE.md'
s = open(p, encoding='utf-8').read()

note = ("> **Revisão 13/11 13h35 (-03):** os números 3.290 / 3.191 foram **revogados como gate**.\n"
        "> O piso depende do harness (o mesmo build A deu 514.595 num e 315.923 noutro; comparar\n"
        "> capturas de harnesses diferentes sub-mascara) e o candidato não é determinístico no ponto\n"
        "> de amostragem (339.655 bytes voláteis só nele). Com a receita de **306 inits** e piso do\n"
        "> mesmo harness, o gate fica **768 (limite inferior) / 9.291 (limite superior)**, dos quais\n"
        "> 404 em `.data`, 359 em `.data001` (PACE/iLok) e 5 no campo TLS. Ver `ROADMAP.md` § S3 e\n"
        "> `startup_audit/xgate_306.json`.\n\n")

s = s.replace("### 2. Estado pós-create — piso do oráculo medido, distância real 3.290",
              note + "### 2. Estado pós-create — piso do oráculo medido, distância real 3.290")
s = s.replace("| Distância pós-create fora do piso | **3.290 bytes** (3.227 ausentes) | idem |",
              "| Distância pós-create fora do piso | **768 / 9.291** com 306 inits (revogados 3.290 / 3.191) | `startup_audit/xgate_306.json` |")
s = s.replace("❌ Estado pós-create       → 3.290 bytes fora do piso (3.227 ausentes)",
              "❌ Estado pós-create       → 768 inferior / 9.291 superior (306 inits)")
open(p, 'w', encoding='utf-8').write(s)
print('3.290 restante:', s.count('3.290'))
