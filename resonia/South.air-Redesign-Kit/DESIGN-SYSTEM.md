# South.air — Design System e decomposição visual

## Direção criativa

**Conceito:** Japanese-inspired audio engineering, premium dark interface, minimalismo tecnológico.

A interface deve transmitir precisão técnica, sofisticação e profissionalismo. A inspiração japonesa deve aparecer principalmente no símbolo do Monte Fuji e no sol nascente, sem transformar a interface em um tema decorativo ou caricatural.

## 1. Identidade e logotipo

### Símbolo

O logotipo deve funcionar como um vetor independente:

- Sol nascente circular em laranja.
- Monte Fuji em silhueta grafite, com neve clara no topo.
- Pequenos traços horizontais sugerindo nuvens ou movimento.
- Geometria simples, poucos nós vetoriais e leitura clara em tamanhos pequenos.
- Fundo transparente.

Arquivos incluídos:

- `assets/brand/southair-mark.svg`: símbolo isolado.
- `assets/brand/southair-lockup.svg`: símbolo com wordmark.

Os SVGs são assets iniciais editáveis, não uma imagem achatada. A tipografia do wordmark usa fontes de sistema como fallback; carregar Oxanium ou Rajdhani no projeto para maior fidelidade.

### Wordmark

Texto: `South.air`

- `South.` em branco gelo.
- `air` em laranja.
- Estilo semibold/bold, levemente inclinado.
- Sugestões: Oxanium, Rajdhani ou alternativa geométrica semelhante.
- Preferir texto real em HTML/CSS na interface, mantendo SVG apenas para lockups estáticos quando necessário.

## 2. Tipografia da interface

- Interface: Inter ou equivalente, pesos 400, 500 e 600.
- Marca: Oxanium ou Rajdhani, peso 600–700, itálico.
- Valores numéricos alinhados e fáceis de comparar.
- Priorizar legibilidade sobre estética futurista.

## 3. Decomposição em componentes

### Sidebar principal

Contém símbolo, wordmark, versão, seletor Soft/Hard, Depth, Detail, Attack e Release. Usar painel grafite e separadores discretos.

### Control Rail

Contém L/R e M/S, Link, Focus, Even, Detail, Attack, Release, Max Cut e Wet Trim. Usar campos compactos, rótulos alinhados e agrupamento consistente.

### Área principal de processamento

- Gráfico com escala de frequência logarítmica.
- Marcas de frequência: 100, 250, 500, 1k, 2k, 4k, 8k e 16k.
- Grade sutil em grafite.
- Curva de processamento laranja e região preenchida com transparência.
- Pontos de controle editáveis e marcadores com contraste suficiente.
- Escala vertical preservada.

O gráfico deve permanecer vetorial/interativo. Não rasterizar.

### Header superior

Indicador de atividade do engine, nome/estado do engine, latência e configurações. Fundo de superfície escura, bordas sutis.

### Footer

Contém Bypass, Delta, Mix, Out, Quality e Low Latency. Manter cada controle como componente independente e funcional.

## 4. Controles e estados

### Knobs

- Trilha restante grafite.
- Arco de valor laranja.
- Indicador laranja.
- Valor numérico em branco gelo.
- Sombra discreta.
- Preferir SVG dinâmico ou CSS/SVG controlado por estado real.

### Sliders

- Trilha grafite.
- Progresso laranja.
- Thumb laranja.

### Botões ativos

- Fundo laranja.
- Texto escuro.
- Contorno sutil.

### Botões inativos

- Fundo `#202123`.
- Texto `#A1A1A2`.
- Borda `#2B2B2D`.

### Inputs numéricos

- Fundo grafite.
- Texto claro.
- Borda discreta.
- Foco com contorno laranja sutil.

### Hover e focus

Transições leves, sem brilho excessivo ou animações que prejudiquem responsividade e desempenho.

## 5. Recomendações técnicas para SVG

Usar SVG para:

- Símbolo do Monte Fuji.
- Lockup estático do logotipo.
- Ícones simples.
- Curva e pontos do gráfico, caso compatíveis com a arquitetura atual.
- Arcos dos knobs, se isso facilitar a atualização dinâmica.

Características:

- `viewBox` proporcional e escalável.
- Fundo transparente.
- `stroke-linecap="round"` e `stroke-linejoin="round"` quando aplicável.
- Evitar SVG monolítico que contenha a interface inteira.
- Não substituir elementos interativos por imagens estáticas.

Cores de ícones: padrão `#A1A1A2`, ativo `#F36D03`.

## 6. Regras de preservação

Não modificar:

- Algoritmos e parâmetros DSP.
- Valores padrão dos controles.
- Conexões entre interface e engine.
- Bypass e Delta.
- Cálculo e comportamento da curva.
- Integração com Soothe3.
- Sistema de áudio e Low Latency.

A tarefa é exclusivamente visual. Antes de mexer, inspecionar framework, componentes, biblioteca de ícones, renderização do gráfico, estilos e mapeamento dos parâmetros.

## 7. Critérios de qualidade

- Preservar a hierarquia de três áreas: sidebar, control rail e gráfico.
- Manter alinhamento, espaçamento e proporções consistentes.
- Evitar texto cortado e controles sobrepostos.
- Garantir legibilidade em diferentes resoluções e densidades de tela.
- Não introduzir rasterizações desnecessárias.
- Validar visualmente o resultado final com screenshot.
