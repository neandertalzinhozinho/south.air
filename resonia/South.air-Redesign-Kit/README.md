# South.air — Redesign Kit

Pacote de handoff visual para orientar o redesign da interface do plugin de áudio South.air.

## Conteúdo

- `PROMPT-PARA-AGENTE.md`: briefing completo para enviar ao agente de desenvolvimento.
- `DESIGN-SYSTEM.md`: decomposição dos elementos, regras visuais e recomendações de implementação.
- `PALETA.md`: paleta oficial com códigos HEX e usos.
- `design-system/tokens.css`: variáveis CSS reutilizáveis.
- `design-system/tokens.json`: tokens em JSON para integração com outras ferramentas.
- `assets/brand/southair-mark.svg`: símbolo vetorial isolado do Monte Fuji.
- `assets/brand/southair-lockup.svg`: símbolo e wordmark em uma composição vetorial.
- `assets/reference/southair-ui-reference.png`: imagem de referência visual aprovada.

## Como usar

1. Envie `assets/reference/southair-ui-reference.png` ao agente como referência visual.
2. Envie o conteúdo de `PROMPT-PARA-AGENTE.md` como instrução principal.
3. Quando possível, peça ao agente para ler também `DESIGN-SYSTEM.md` e importar `design-system/tokens.css`.
4. Os SVGs incluídos são pontos de partida editáveis. Ajuste dimensões e tipografia conforme a arquitetura real do projeto.

## Observação importante

Este pacote contém especificação visual e assets de referência. Não contém o código-fonte do plugin nem altera sua implementação. A lógica DSP, os parâmetros e as conexões de áudio devem permanecer intactos durante o redesign.

A fonte da marca é declarada no SVG com fallbacks. Para manter a aparência exata em todas as máquinas, instale/carregue a fonte escolhida no próprio projeto (por exemplo, Oxanium) ou converta o lettering para curvas somente na versão final de distribuição.
