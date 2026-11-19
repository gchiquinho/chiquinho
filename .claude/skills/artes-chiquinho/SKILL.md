---
name: artes-chiquinho
description: Cria as artes (imagens PNG) das campanhas e posts da Chiquinho Tintas com a identidade visual da loja — capa e passos de carrossel, oferta com preço/selo/cupom, paleta de cores, story, contagem regressiva, aviso de horário, antes e depois e cabeçalho de WhatsApp. Use sempre que o usuário pedir "faz a arte", "cria o carrossel", "monta o post da promoção", "arte do story", "imagem para o WhatsApp", "gera as artes da campanha" ou quando uma campanha de `campanhas/` precisar das peças visuais.
---

# Artes — Chiquinho Tintas

Gera artes prontas para Instagram, Facebook e WhatsApp a partir de um **roteiro JSON**: você escreve o texto de cada slide, escolhe o modelo, e o script desenha tudo com a identidade visual da loja e confere se o texto cabe.

## Dois caminhos

1. **Canva (preferido para peças de campanha)** — quando o conector do Canva estiver disponível. Gera artes mais ricas (ilustrações, pinceladas, elementos de Natal) e o usuário pode ajustar no próprio Canva. Ver "Fluxo no Canva".
2. **Script local (`render.mjs`)** — para peças simples e repetitivas (avisos, stories de contagem, cabeçalho de WhatsApp) ou quando não houver Canva.

Nos dois casos, siga a identidade da loja em **`marcas.md`** (logo, cores, tipografia de cada loja do grupo).

## Fluxo no Canva

1. `list-brand-kits` — se existir kit da loja, passe o `brand_kit_id` no `create-design`.
2. Logo: procure nos Uploads do Canva (`logo-<loja>`). Se não houver, peça o arquivo ao usuário (PNG) e envie com `create-upload-url`. Passe o id em `references`. Nunca peça para a IA "desenhar" a logo.
3. `create-design` com `format: "Instagram Post (Portrait)"` (ou `"Instagram Story"`) e um `brief` que tenha:
   - a identidade da loja copiada de `marcas.md` (cores com hex, tipografia, símbolo);
   - **todos os textos exatos, página por página** (o Canva não deve inventar texto);
   - as proibições: sem preços inventados, sem logos de fabricantes, sem fotos de pessoas, usar "×" e não emoji.
4. Aguarde o job (`get-create-design-async-job`, respeitando `wait_seconds`) e confira **cada página** com `read-design` (thumbnails + texto). A IA do Canva costuma errar:
   - palavras trocadas (ex.: "Desconto" no lugar de "Desconte");
   - símbolos virando emoji (ex.: "❎" no lugar de "×");
   - cor dominante fora da marca.
   Corrija com `read-design` (`open_transaction`) + `edit-design` (`find_and_replace_text`), mostre a prévia ao usuário e só faça `commit` com o "ok" dele.
5. Guarde o link do design no plano da campanha (seção da peça).

## Arquivos

| Arquivo | Para quê |
|---|---|
| `marcas.md` | Logo, cores e tipografia de **cada loja** do grupo |
| `logos/` | Arquivos oficiais das logos (`<loja>.png`) |
| `identidade.json` | Cores, fonte, @ do Instagram, cidade, WhatsApp e endereço. **Fonte única da identidade** — mude aqui, todas as artes mudam |
| `scripts/modelos.mjs` | Os modelos (layout + CSS) |
| `scripts/render.mjs` | Gera os PNGs e a `_previa.png` com todas as artes lado a lado |
| `exemplos/todos-os-modelos.json` | Um exemplo de cada modelo |

## Fluxo

1. **Ler o plano** da campanha (ex.: `campanhas/natal-2026-chiquinho-tintas.md`) para saber a peça, o texto e a data.
2. **Escrever o roteiro** em `campanhas/artes/<campanha>/roteiro.json` (ver formato abaixo). Um roteiro pode ter várias peças; nomeie as artes pela peça e ordem: `p4-oferta-1`, `p5-contagem-1`.
3. **Gerar:**
   ```bash
   node .claude/skills/artes-chiquinho/scripts/render.mjs campanhas/artes/<campanha>/roteiro.json
   # só algumas artes:  --so p4-oferta-1,p5-contagem-1
   # outra pasta:       --saida caminho/
   ```
4. **Conferir:** abrir a `_previa.png` (ferramenta Read) e olhar cada arte. Ler os **⚠️ Avisos** do script:
   - `[colchetes] não preenchido` → falta informação do usuário (preço, código de cor, horário). Perguntar; não inventar.
   - `texto grande demais` → encurtar o texto (não diminuir a fonte).
5. **Mostrar ao usuário** a prévia (SendUserFile) e ajustar o que ele pedir.
6. **Versionar:** apagar os `.html` gerados (`rm campanhas/artes/<campanha>/*.html`), manter `roteiro.json`, PNGs e `_previa.png`, e fazer commit.
7. **Publicar** só com a skill `redes-sociais-grupo-chiquinho` (plugin), que exige prévia e "sim" do usuário para cada post.

### Sem Playwright (ex.: no computador da loja)
Rode com `--so-html`: o script grava só os `.html`. Passe o conteúdo de cada um para a ferramenta `criar_arte` do plugin (`formato` igual ao do modelo), que gera o PNG no próprio computador.

## Formato do roteiro

```json
{
  "campanha": "Natal 2026",
  "formato": "feed_retrato",
  "identidade": { "whatsapp": "(16) 0000-0000" },
  "artes": [
    { "nome": "p4-oferta-1", "modelo": "oferta", "tema": "claro", "dados": { ... } }
  ]
}
```
- `formato` padrão de feed; `story`/`contagem` usam `story` e `whatsapp` usa `whatsapp_cabecalho` automaticamente. Também dá para pôr `formato` em cada arte.
- `identidade` (opcional) sobrescreve campos de `identidade.json` só neste roteiro.
- `tema: "claro"` usa fundo creme em vez do escuro.
- Textos aceitam `<b>`, `<br>` e `<span class='hl'>palavra</span>` (laranja). Destaque **1 ou 2 palavras** por título.

## Modelos

| Modelo | Uso | Campos (`dados`) |
|---|---|---|
| `capa` | 1º slide de carrossel | `etiqueta`, `titulo`, `subtitulo`, `faixa` (false tira a faixa de cores) |
| `passo` | Slides numerados | `numero`, `titulo`, `texto`, `destaque` (caixa), `pagina` ("2/6") |
| `fechamento` | Último slide com chamada | `etiqueta`, `titulo`, `texto`, `destaque`, `pagina` — mostra WhatsApp/endereço se estiverem na identidade |
| `oferta` | Promoção | `etiqueta`, `selo` ("-20%" ou emoji), `produto`, `preco_de`, `preco_por` **ou** `beneficio` (brinde), `cupom`, `validade`, `condicoes` |
| `paleta` | 3 a 6 cores | `etiqueta`, `titulo`, `cores: [{hex, nome, codigo}]` |
| `aviso` | Horário de feriado, comunicado | `etiqueta`, `titulo`, `texto`, `linhas: [["24/12","8h às 12h"], ...]` |
| `story` | Story de mensagem única | `etiqueta`, `titulo`, `texto`, `chamada` (botão no rodapé) |
| `story_produto` | Story de produto com preço (Auto Peças: `tema: "metal"`) | `etiqueta`, `produto`, `detalhe`, `rotulo`, `cor_lata`, `embalagem`, `preco`, `por_litro`, `chamada`, `foto` (opcional; sem foto, desenha uma lata) |
| `contagem` | Story de contagem regressiva | `etiqueta`, `numero`, `unidade`, `titulo`, `chamada` |
| `antes_depois` | Comparação | `antes`, `depois` (URL https ou caminho de foto local), `titulo` |
| `whatsapp` | Cabeçalho da mensagem modelo | `etiqueta`, `titulo`, `texto` |

## Regras de conteúdo

- **Nunca inventar** preço, desconto, validade, nome ou código de cor, horário, telefone ou endereço. Sem o dado, deixe `[colchetes]` e pergunte ao usuário.
- **Confira a conta do preço por litro/unidade** (preço ÷ volume) antes de publicar. Se o valor informado não bater, avise o usuário.
- Toda oferta mostra validade e "enquanto durar o estoque" (o modelo já põe) e as condições quando houver.
- Fotos: só da loja ou enviadas pelo usuário. Nada de foto de pessoas da internet nem logo de fabricante sem o arquivo oficial.
- Máx. ~25 palavras por slide; título de até ~8 palavras. Se o aviso de texto grande aparecer, corte palavras.
- Stories: a interface do Instagram cobre 250 px em cima e embaixo — o modelo já respeita; não ponha texto fora do `story-centro`.
- Carrossel: todos os slides no mesmo formato e tema; capa promete, passos entregam, fechamento pede ação (salvar, WhatsApp, visitar a loja).

## Mudando a identidade

Recebeu o manual da marca ou o logo? Atualize `identidade.json` (cores, fonte do Google Fonts, WhatsApp, endereço), gere `exemplos/todos-os-modelos.json` e confira a prévia antes de refazer as artes da campanha.
