# SOUTH.AIR — REDESIGN VISUAL E DESIGN SYSTEM

## OBJETIVO

Reconstruir visualmente a interface atual do plugin de áudio, substituindo a identidade visual antiga pela nova identidade South.air.

Utilize `assets/reference/southair-ui-reference.png` como guia visual principal e `DESIGN-SYSTEM.md` como especificação complementar.

**IMPORTANTE:** esta tarefa é exclusivamente de redesign visual. Preserve integralmente a lógica de processamento de áudio, parâmetros DSP, funcionalidades, arquitetura e comportamento dos controles existentes.

Não recrie o plugin do zero ignorando sua implementação atual. Primeiro analise a estrutura existente e identifique os componentes que podem ser estilizados ou substituídos visualmente.

## 1. NOVA IDENTIDADE VISUAL

Nome oficial: **South.air**

Conceito: Japanese-inspired audio engineering, premium dark interface, minimalismo tecnológico.

A identidade deve transmitir precisão técnica, sofisticação, minimalismo e tecnologia de áudio profissional. A inspiração japonesa deve aparecer principalmente no símbolo do Monte Fuji e no sol nascente, sem transformar a interface em um tema decorativo.

### Logotipo

Criar um logotipo vetorial original inspirado no Monte Fuji:
- Sol nascente circular em laranja.
- Montanha Fuji em silhueta grafite com neve branca no topo.
- Pequenos traços horizontais representando nuvens ou movimento.
- Composição geométrica limpa e equilibrada.
- Fundo transparente.

Arquivos iniciais incluídos:
- `assets/brand/southair-mark.svg` — símbolo isolado.
- `assets/brand/southair-lockup.svg` — símbolo com wordmark.

Os SVGs são pontos de partida editáveis. Ajustar proporções, paths e tipografia se necessário. Carregar Oxanium ou Rajdhani no projeto para maior fidelidade.

### Wordmark

Texto: `South.air`
- `South.` em branco gelo.
- `air` em laranja.
- Fonte sugerida: Oxanium ou Rajdhani, peso 600–700, estilo itálico.
- Preferir texto real em HTML/CSS na interface em vez de texto rasterizado.

## 2. PALETA OFICIAL

Usar os tokens definidos em `design-system/tokens.css` e `design-system/tokens.json`.

### Backgrounds
- Background principal: `#100E0E`
- Panel: `#141414`
- Surface: `#1A1A1B`
- Control Background: `#202123`
- Border: `#2B2B2D`
- Graph Grid: `#292727`

### Orange
- Orange Primary: `#F36D03`
- Orange Active: `#FA8603`
- Orange Deep: `#A54D05`
- Orange Glow: `#522304`
- Orange Soft: `#FBA45A`

### Typography
- Text Primary: `#E3E3E2`
- Text Secondary: `#A1A1A2`
- Text Muted: `#68686B`

O laranja deve ser utilizado com moderação. Não transformar toda a interface em uma superfície laranja. Reservar o laranja para elementos selecionados, indicadores ativos, curvas de processamento, pontos de controle, detalhes do logotipo e estados de interação.

## 3. TIPOGRAFIA

Interface:
- Inter ou alternativa equivalente.
- Preferência por pesos 400, 500 e 600.
- Valores numéricos com alinhamento consistente.
- Hierarquia visual clara entre títulos, rótulos e valores.

Marca:
- Oxanium ou Rajdhani.
- Peso 600 ou 700.
- Estilo itálico.
- Aparência tecnológica, sem exageros.

Evitar fontes excessivamente futuristas nos controles. A legibilidade é prioritária.

## 4. DECOMPOSIÇÃO DA INTERFACE

### A. Sidebar principal

Contém:
- Símbolo South.air.
- Wordmark South.air.
- Versão 0.1.0.
- Seletores Soft e Hard.
- Knob Depth.
- Knob Detail.
- Knob Attack.
- Knob Release.

Utilizar fundo grafite, divisórias discretas e espaçamento consistente.

### B. Control Rail

Contém:
- Seleção L/R e M/S.
- Link.
- Focus.
- Even.
- Detail.
- Attack.
- Release.
- Max Cut.
- Wet Trim.

Agrupar controles de maneira organizada, com campos numéricos compactos.

### C. Área principal de processamento

Preservar o gráfico de frequência.
- Grade escura e discreta.
- Frequências de referência: 100, 250, 500, 1k, 2k, 4k, 8k e 16k.
- Escala logarítmica.
- Marcadores circulares editáveis.
- Curva de processamento laranja.
- Região de processamento com preenchimento laranja translúcido.
- Indicadores de nível no eixo vertical.

A curva e os pontos devem ser vetoriais, preferencialmente usando SVG. Não rasterizar o gráfico.

### D. Header superior

Contém indicador de atividade do engine, nome e estado do engine, latência e botão de configurações. Manter o cabeçalho discreto, com superfícies grafite e bordas sutis.

### E. Footer

Contém Bypass, Delta, Mix, Out, Quality e Low Latency. Utilizar botões e campos independentes. Manter valores e comportamentos existentes.

## 5. DIRETRIZES PARA SVG

Criar ou adaptar SVGs independentes para:
1. Símbolo do Monte Fuji.
2. Composição completa do logotipo.
3. Ícones de controles e ações.
4. Curva e marcadores do gráfico, se compatíveis com a arquitetura.
5. Arcos dos knobs, caso seja adequado à implementação atual.

Características:
- `viewBox` adequado e escalável.
- Fundo transparente.
- `stroke-linecap="round"` e `stroke-linejoin="round"` quando aplicável.
- Não criar SVG gigante contendo toda a interface.
- Não substituir componentes interativos por imagens estáticas.

Ícones: cor padrão `#A1A1A2`, cor ativa `#F36D03`, tamanho-base sugerido 24 × 24 px.

## 6. CONTROLES E ESTADOS VISUAIS

### Botões selecionados
- Fundo laranja.
- Texto escuro.
- Bordas discretas.

### Botões inativos
- Fundo `#202123`.
- Texto `#A1A1A2`.
- Borda `#2B2B2D`.

### Sliders
- Trilha grafite.
- Progresso laranja.
- Thumb laranja.

### Knobs
- Arco de progresso laranja.
- Trilha restante grafite.
- Indicador central laranja.
- Valor numérico em branco.
- Sombras discretas.

### Inputs numéricos
- Fundo grafite.
- Bordas sutis.
- Texto branco.
- Estados de foco com contorno laranja discreto.

### Hover e Focus
- Transições leves.
- Sem brilho excessivo.
- Sem animações exageradas.
- Não comprometer a latência ou a resposta dos controles.

## 7. ESTRUTURA E IMPLEMENTAÇÃO

Antes de implementar, identificar:
- Framework e linguagem utilizados.
- Sistema atual de componentes.
- Biblioteca de ícones.
- Sistema de renderização do gráfico.
- Estrutura de estilos.
- Mapeamento dos parâmetros dos controles.

Criar tokens reutilizáveis para cores, tipografia, bordas, espaçamentos, raios e sombras.

Separar os estilos da identidade visual da lógica DSP.

Preferir componentes reutilizáveis para:
- Knob.
- Slider.
- Button.
- NumericInput.
- Toggle.
- Dropdown.
- Graph.
- Header.
- Sidebar.
- ControlRail.
- Footer.

Se a arquitetura atual exigir outra organização, adaptar sem forçar uma reestruturação desnecessária.

## 8. RESPONSIVIDADE E QUALIDADE

- Manter a proporção visual da referência.
- Preservar a hierarquia dos três painéis.
- Garantir alinhamento consistente.
- Evitar textos cortados.
- Evitar controles sobrepostos.
- Manter legibilidade em diferentes resoluções.
- Garantir renderização nítida em telas de alta densidade.
- Não utilizar rasterizações desnecessárias.

## 9. REGRAS IMPORTANTES

NÃO modificar:
- Algoritmos de processamento.
- Parâmetros DSP.
- Valores padrão.
- Conexões entre controles e engine.
- Funcionamento de Bypass e Delta.
- Cálculo da curva.
- Sistema de áudio.
- Integração com Soothe3.
- Comportamento de Low Latency.

NÃO fazer:
- Recriar uma interface estática.
- Transformar o gráfico em imagem.
- Usar emojis como ícones.
- Utilizar gradientes laranja em grandes superfícies.
- Exagerar nos efeitos de glow.
- Alterar nomes ou valores dos parâmetros existentes.
- Remover funcionalidades para facilitar o redesign.

## 10. RESULTADO ESPERADO

Entregar uma implementação funcional do redesign South.air, visualmente próxima da imagem de referência, mantendo a estrutura original e todos os comportamentos existentes.

Entregar:
- Logotipo vetorial em SVG.
- Ícones vetoriais.
- Design tokens de cores.
- Tipografia configurada.
- Componentes visuais reutilizáveis.
- Gráfico vetorial interativo.
- Estilos organizados.
- Interface final integrada ao plugin.

Ao concluir, apresentar:
1. Arquivos criados e modificados.
2. Componentes reaproveitados.
3. Componentes substituídos.
4. Confirmação de que a lógica DSP não foi alterada.
5. Captura de tela do resultado final.

O objetivo é que South.air tenha aparência de um produto comercial de áudio profissional, com identidade visual própria, consistente e preparada para evoluir.
