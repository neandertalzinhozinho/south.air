from pathlib import Path

p = Path(r'D:\PROJETOS\shadowFILES\REGISTRO_COORDENACAO.md')
t = p.read_text(encoding='utf-8')

add = """

## Reconciliacao da base da captura - 16/11/2026

Medicao somente leitura sobre os artefatos parados. Tres campos independentes do diretorio TLS
(RVA `0x79CC428`) foram lidos no original e na captura de memoria:

- `AddressOfCallBacks` (RVA `0x79CC440`): original `0x1879CC158`, captura `0x2068C158`, diferenca `0xCC0000`.
- `StartAddressOfRawData` (RVA `0x79CC430`): original `0x1820D7E70`, captura `0x1AD97E70`, diferenca `0xCC0000`.
- `AddressOfIndex` (RVA `0x79CC438`): original `0x1826AE7E0`, captura `0x1B36E7E0`, diferenca `0xCC0000`.

As tres diferencas coincidem byte a byte em `0xCC0000`, o que fixa a base de carga da captura em
`0x18CC0000` e a base preferida em `0x180000000`. O alvo de `AddressOfCallBacks` e o RVA
`0x79CC158` (array de callbacks), nao o RVA do campo `0x79CC440`; a leitura anterior desse campo
como "ponteiro orfao" foi erro de interpretacao, nao evidencia de base inconsistente.

**Correcao aritmetica.** A identidade registrada nas secoes anteriores tem um zero a menos. O
correto e `0x18CC0000 - 0xCC0000 = 0x180000000`. A premissa da suspensao deixa de existir.

**Estado da receita.** A conversao de ponteiros por `-0xCC0000` e aritmeticamente consistente, mas
nao e a rota em uso: a captura no estagio de carga difere do oraculo em 1 byte
(`s3_wrapperstub_gate.json`, `comparison.load_delta_lower` = 1 nas nove combinacoes). A
materializacao do `.data` e reproduzida por replay da cadeia de inicializacao (306 entradas em
`init_order_plus_tables.json`), nao por gravar a cauda da captura no arquivo. R.3 fica
**superseded**, nao "validada". Nenhum binario foi criado, alterado ou executado nesta rodada.

**Residuo que permanece, e que nao e aritmetico.** No artefato `wrapperstub`, o `.data` pos-create
difere do oraculo em limite inferior de 90.295 bytes (estavel 9/9), e a janela `.data+0x530000` a
`.data+0x538000` tem seis strings presentes no oraculo e zeros no candidato. Esse residuo e estado
populado pela camada de licenca, nao geometria do PE. S3 continua NAO APROVADO.
"""

if 'Reconciliacao da base da captura' in t:
    print('ja existe; nada alterado')
else:
    p.write_text(t.rstrip() + add, encoding='utf-8')
    print('apendado. linhas agora:', len(p.read_text(encoding='utf-8').splitlines()))
