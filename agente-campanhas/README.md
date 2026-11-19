# 🎯 Agente de Campanhas e Engajamento

Agente de marketing digital que **cria campanhas**, **analisa engajamento** de redes sociais e **recomenda estratégias** com base em dados.

São duas partes:

| Parte | O que faz |
|---|---|
| `.claude/agents/estrategista-campanhas.md` | Agente do Claude Code: conduz o briefing, escreve conceito criativo, copys, roteiros e interpreta os números. |
| `agente-campanhas/campanhas/` | Motor em Python (só biblioteca padrão) que calcula métricas e gera o esqueleto do plano. |

## Como usar o agente

No Claude Code, dentro deste repositório, peça por exemplo:

- "Usa o estrategista-campanhas para criar a campanha de Natal com R$ 3.000 em 20 dias"
- "Analisa o engajamento desse CSV do Instagram e me diz o que fazer"
- "Qual o melhor formato e horário para postar?"

## Motor em Python

```bash
cd agente-campanhas

# Análise de engajamento
python -m campanhas analisar dados/exemplo_posts.csv --saida relatorio.md
python -m campanhas analisar dados/exemplo_posts.csv --canal instagram

# Plano de campanha
python -m campanhas planejar --nome "Black Friday" --objetivo conversao \
  --orcamento 5000 --dias 21 --canais instagram,facebook,whatsapp \
  --inicio 2026-11-10 --publico "Pintores, 25-55 anos" --saida plano.md

# Testes
python -m unittest discover -s tests
```

### Formato do CSV

```
data,canal,formato,tema,alcance,impressoes,curtidas,comentarios,compartilhamentos,salvamentos,cliques,conversoes,investimento
2026-09-01 19:30,instagram,reels,Antes e depois,2400,3100,90,12,20,8,25,1,0
```

- Separador `,` ou `;`; números no formato `1.234,56` ou `1234.56`.
- Só `data` é obrigatória; colunas ausentes contam como zero; colunas extras (ex.: `tema`) aparecem no relatório.

### O que a análise entrega

- Taxa de engajamento, salvamento, compartilhamento, CTR, conversão, CPC e custo por conversão, comparados a benchmarks de mercado.
- Desempenho por canal, formato, dia da semana e faixa horária.
- Tendência (1ª vs. 2ª metade do período), melhores/piores posts e outliers (z-score ≥ 1,5).
- **Ações priorizadas**: ação → motivo → impacto → como medir.

### O que o plano entrega

- Fases do funil (topo/meio/fundo) com duração e verba proporcionais ao objetivo
  (`reconhecimento`, `engajamento`, `trafego`, `leads`, `conversao`, `retencao`).
- Divisão de verba por canal + 15% de reserva para testes A/B.
- KPIs do objetivo, calendário de conteúdo, datas sazonais do varejo no período
  (Dia das Mães, Black Friday, Natal…), rotina de acompanhamento e plano B.

> Os dados de `dados/exemplo_posts.csv` são fictícios, gerados só para demonstração.
