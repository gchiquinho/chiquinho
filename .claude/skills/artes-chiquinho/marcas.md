# Identidade visual das lojas do Grupo Chiquinho

Cores tiradas das logos oficiais que o Luiz enviou em 19/11/2026. Os códigos hex são aproximados (lidos da imagem). Se a loja tiver o manual da marca, substitua pelos oficiais.

> **Arquivos das logos:** guarde os PNG (de preferência com fundo transparente) em `.claude/skills/artes-chiquinho/logos/<loja>.png`, e também nos Uploads do Canva com o nome `logo-<loja>`. Nunca redesenhe nem "imite" a logo: use sempre o arquivo oficial.

| Loja | Logo | Cores | Tipografia | Clima |
|---|---|---|---|---|
| **Chiquinho Tintas** (`chiquinho-tintas`) | Casinha com telhado branco em linha e um **redemoinho de pinceladas arco-íris** dentro; "CHIQUINHO" em branco, "TINTAS" espaçado embaixo | Verde-escuro `#0B4A1C` (fundo), branco `#FFFFFF`, arco-íris do símbolo (amarelo `#FFC20E`, laranja `#F7931E`, vermelho `#E53935`, magenta `#E91E8C`, roxo `#8E24AA`, azul `#1E5BD8`, ciano `#00B5E2`, verde-limão `#8BC34A`) | Sans geométrica, grossa e em caixa alta (Montserrat ExtraBold) | Casa, cor, acabamento. Limpo e premium |
| **Chiquinho Auto Peças** (`chiquinho-auto-pecas`) | Silhueta de carro esportivo em laranja e preto sobre "CHIQUINHO" branco em itálico com contorno preto; "AUTO PEÇAS" laranja espaçado | Grafite/metal escovado `#1C1C1E` → `#3A3A3C`, laranja `#F39200`, branco | Itálico pesado e esportivo (estilo Racing/Bebas Italic) | Oficina, velocidade, força |
| **CooperTintas** (`coopertintas`) | "Cooper" branco, grande e arredondado, com "TINTAS" embaixo e um **leque/roda de cores** (amarelo, laranja, vermelho, magenta, roxo, azul, verde) | Azul-marinho `#0A2478`, branco, cores do leque | Sans arredondada e grossa (estilo Nunito Black / Fredoka) | Cooperativa, confiança, variedade de cores |
| **Leve Tintas** (`leve-tintas`) | Círculo vermelho com "Leve" e faixa azul com "Tintas" em branco com contorno preto, pincel pintando de vermelho. Slogan: **"A garantia de levar o melhor!"** | Laranja vibrante `#FF8A00` (fundo com raios), vermelho `#D71920`, azul `#1E88D8`, branco, contorno preto | Display divertida, com contorno (estilo cartoon) | Popular, alegre, oferta |

## Logos no Canva (conta do Luiz, plano gratuito)

| Loja | Asset ID no Canva | Arquivo original |
|---|---|---|
| Chiquinho Tintas | `MAHbY6TfRk0` | 1254×1254, fundo verde |
| Chiquinho Auto Peças | `MAHbY4-Rwak` | 900×1600, fundo grafite |
| CooperTintas | `MAHbYyBsawk` | 900×1600, fundo azul |
| Leve Tintas | `MAHbYy6FWag` | 900×1600, fundo laranja |

O design "logo todas loja" (`DAHbY2YuOrU`) tem as 4 logos, uma por página.

Como usar: `edit-design` → `insert_fill` (ou `update_fill`) com o asset_id acima. As logos vêm **com fundo**, então ponha a logo sobre a cor da própria marca ou recorte numa área da mesma cor.
O plano é gratuito: **não há remoção de fundo nem Kit de Marca**, e os créditos de IA (`create-design`) são poucos. Prefira copiar um modelo aprovado (`copy-design`) e editar.

### Fotos de produto
As fotos ficam em **Uploads** (`list-folder-items` com `folder_id: "uploads"`, mais recentes primeiro). Os nomes seguem o padrão `produto-<loja>-<produto>`. Fotos com fundo branco: remova o fundo localmente (script em Python/PIL, flood fill a partir das bordas), devolva o PNG ao usuário e peça que ele suba no Canva.

| Produto | Asset ID | Obs. |
|---|---|---|
| Laca nitrocelulose Farben preto semibrilho 3,6 L | `MAHbZEDhnas` | **sem fundo (PNG)** — usar esta |
| Laca nitrocelulose Farben 3,6 L (original) | `MAHbZNiRrfg` | fundo branco, 446 px |

## Regras

- Em cada arte, use **a logo e as cores da loja que está publicando**. Não misture identidades, a não ser em peças institucionais do grupo.
- A logo vai inteira, sem distorcer, com respiro em volta, num canto (topo ou rodapé) ou centralizada na capa.
- Fundo da logo: use a versão sobre a cor da marca (como nas imagens enviadas) ou PNG transparente.
- Elementos de campanha (Natal, Black Friday) entram como **detalhe**. A cor dominante continua sendo a da marca.
