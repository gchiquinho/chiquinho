"""Recomendações estratégicas e geração de planos de campanha."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from .metricas import BENCHMARKS


def _p(valor: float, casas: int = 1) -> str:
    """Percentual no formato brasileiro (4,5%)."""
    return f"{valor * 100:.{casas}f}%".replace(".", ",")

# ---------------------------------------------------------------------------
# Recomendações a partir da análise
# ---------------------------------------------------------------------------

MIN_POSTS_GRUPO = 2  # evita conclusões com um único post


def _melhor_pior(grupos: dict[str, dict], metrica: str = "taxa_engajamento"):
    validos = {k: v for k, v in grupos.items() if v["posts"] >= MIN_POSTS_GRUPO and v["alcance"]}
    if len(validos) < 2:
        return None, None
    ordenado = sorted(validos.items(), key=lambda kv: kv[1][metrica], reverse=True)
    return ordenado[0], ordenado[-1]


def recomendar(analise: dict) -> list[dict]:
    """Gera ações priorizadas (ação, motivo, impacto, medição)."""
    recs: list[dict] = []
    geral = analise["geral"]

    melhor, pior = _melhor_pior(analise["por_formato"])
    if melhor and pior and melhor[1]["taxa_engajamento"] > pior[1]["taxa_engajamento"] * 1.3:
        recs.append({
            "prioridade": 1,
            "acao": f"Aumentar a participação de **{melhor[0]}** no mix e reduzir **{pior[0]}**.",
            "motivo": (f"{melhor[0]} engaja {_p(melhor[1]['taxa_engajamento'], 1)} contra "
                       f"{_p(pior[1]['taxa_engajamento'], 1)} de {pior[0]}."),
            "impacto": "Alta — redistribuir formato costuma ser o ganho mais rápido.",
            "medicao": "Taxa de engajamento média das próximas 2 semanas vs. período atual.",
        })

    melhor, pior = _melhor_pior(analise["por_faixa"])
    if melhor and pior:
        recs.append({
            "prioridade": 2,
            "acao": f"Concentrar publicações na faixa **{melhor[0]}**.",
            "motivo": (f"Engajamento de {_p(melhor[1]['taxa_engajamento'], 1)} nessa faixa vs. "
                       f"{_p(pior[1]['taxa_engajamento'], 1)} em {pior[0]}."),
            "impacto": "Média — melhora a entrega inicial que alimenta o algoritmo.",
            "medicao": "Alcance nas primeiras 24h de cada post.",
        })

    melhor, _ = _melhor_pior(analise["por_dia"])
    if melhor:
        recs.append({
            "prioridade": 3,
            "acao": f"Usar **{melhor[0]}** para os conteúdos mais importantes (ofertas, lançamentos).",
            "motivo": f"É o dia com maior engajamento médio ({_p(melhor[1]['taxa_engajamento'], 1)}).",
            "impacto": "Média.",
            "medicao": "Comparar o post-chave desse dia com a média semanal.",
        })

    if geral["alcance"] and geral["taxa_salvamento"] < BENCHMARKS["taxa_salvamento"][0]:
        recs.append({
            "prioridade": 2,
            "acao": "Criar conteúdo **salvável**: carrosséis de dicas, passo a passo, checklists e tabelas.",
            "motivo": f"Taxa de salvamento de {_p(geral['taxa_salvamento'], 2)}, abaixo da referência de 0,5%.",
            "impacto": "Alta — salvamentos são um forte sinal de relevância para o algoritmo.",
            "medicao": "Salvamentos / alcance por post.",
        })

    if geral["alcance"] and geral["ctr"] < BENCHMARKS["ctr"][0]:
        recs.append({
            "prioridade": 2,
            "acao": "Reforçar **CTAs** claros (link na bio, botão de WhatsApp, 'comente EU QUERO') e usar stories com link.",
            "motivo": f"CTR de {_p(geral['ctr'], 2)}, abaixo da referência de 0,8%.",
            "impacto": "Alta para tráfego e vendas.",
            "medicao": "Cliques / alcance; cliques no link da bio.",
        })

    if geral["cliques"] and geral["taxa_conversao"] < BENCHMARKS["taxa_conversao"][0]:
        recs.append({
            "prioridade": 1,
            "acao": "Revisar a **página de destino/atendimento**: oferta clara, preço visível, resposta rápida no WhatsApp.",
            "motivo": f"Só {_p(geral['taxa_conversao'], 1)} dos cliques viram conversão.",
            "impacto": "Alta — o tráfego já existe, o gargalo está depois do clique.",
            "medicao": "Conversões / cliques; tempo médio de primeira resposta.",
        })

    tendencia = analise.get("tendencia")
    if tendencia and tendencia["variacao"] <= -0.15:
        recs.append({
            "prioridade": 1,
            "acao": "Investigar a **queda de engajamento**: renovar ganchos (3 primeiros segundos/1ª linha) e retomar os temas dos melhores posts.",
            "motivo": f"Engajamento caiu {_p(abs(tendencia['variacao']), 0)} da 1ª para a 2ª metade do período.",
            "impacto": "Alta.",
            "medicao": "Engajamento semanal até voltar ao patamar anterior.",
        })

    if analise["outliers_alta"]:
        p, _ = analise["outliers_alta"][0]
        tema = p.extras.get("tema") or p.extras.get("legenda") or p.formato
        recs.append({
            "prioridade": 2,
            "acao": f"Replicar o padrão do post de {p.data:%d/%m} ({tema}) em 2 a 3 variações.",
            "motivo": f"Ficou bem acima da média ({_p(p.taxa_engajamento, 1)} vs. {_p(analise['media_post'], 1)}).",
            "impacto": "Média/alta — repetir o que já funcionou reduz risco.",
            "medicao": "Engajamento das variações vs. post original.",
        })

    if geral["posts"] and len(analise["por_formato"]) == 1:
        recs.append({
            "prioridade": 3,
            "acao": "Testar novos formatos (reels e carrossel) — hoje só um formato é usado.",
            "motivo": "Sem diversidade de formato não há base para comparar.",
            "impacto": "Média.",
            "medicao": "Teste A/B: 4 posts de cada formato com o mesmo tema.",
        })

    recs.sort(key=lambda r: r["prioridade"])
    return recs[:6]


# ---------------------------------------------------------------------------
# Planejamento de campanha
# ---------------------------------------------------------------------------

OBJETIVOS = {
    "reconhecimento": {
        "descricao": "Fazer a marca/oferta ser vista pelo maior número de pessoas do público certo.",
        "funil": {"topo": 0.70, "meio": 0.20, "fundo": 0.10},
        "kpis": ["Alcance", "Impressões", "Frequência (1,5–3)", "Crescimento de seguidores", "CPM"],
    },
    "engajamento": {
        "descricao": "Gerar conversa, salvamentos e compartilhamentos para fortalecer a comunidade.",
        "funil": {"topo": 0.40, "meio": 0.45, "fundo": 0.15},
        "kpis": ["Taxa de engajamento", "Salvamentos", "Compartilhamentos", "Comentários", "Respostas a stories"],
    },
    "trafego": {
        "descricao": "Levar pessoas ao site, catálogo, loja virtual ou WhatsApp.",
        "funil": {"topo": 0.30, "meio": 0.50, "fundo": 0.20},
        "kpis": ["Cliques no link", "CTR", "CPC", "Sessões no site", "Conversas iniciadas"],
    },
    "leads": {
        "descricao": "Captar contatos qualificados (WhatsApp, cadastro, orçamento).",
        "funil": {"topo": 0.25, "meio": 0.45, "fundo": 0.30},
        "kpis": ["Leads", "Custo por lead (CPL)", "Taxa de conversão do formulário", "Leads qualificados"],
    },
    "conversao": {
        "descricao": "Gerar vendas e faturamento no período da campanha.",
        "funil": {"topo": 0.20, "meio": 0.30, "fundo": 0.50},
        "kpis": ["Vendas", "Faturamento", "ROAS", "Custo por venda (CPA)", "Ticket médio"],
    },
    "retencao": {
        "descricao": "Fazer clientes atuais voltarem a comprar e indicarem.",
        "funil": {"topo": 0.10, "meio": 0.30, "fundo": 0.60},
        "kpis": ["Taxa de recompra", "Vendas de clientes recorrentes", "Indicações", "NPS"],
    },
}

FASES_FUNIL = {
    "topo": ("Aquecimento / Descoberta", "Atrair atenção e apresentar o problema ou desejo.",
             ["Reels com gancho forte", "Conteúdo educativo", "Tendências e bastidores"]),
    "meio": ("Consideração", "Mostrar a solução, gerar confiança e prova social.",
             ["Carrossel comparativo", "Depoimentos e antes/depois", "Lives e tira-dúvidas"]),
    "fundo": ("Conversão / Oferta", "Converter com oferta clara e senso de urgência.",
              ["Post de oferta", "Stories com contagem regressiva", "Remarketing", "Mensagem no WhatsApp"]),
}

PAPEL_CANAL = {
    "instagram": "Vitrine principal: reels para alcance, carrossel para salvar, stories para conversão.",
    "facebook": "Público 35+ e grupos locais; impulsionamento barato para alcance regional.",
    "whatsapp": "Fechamento de vendas e relacionamento com base própria (somente contatos com opt-in).",
    "tiktok": "Alcance orgânico com vídeos curtos e tendências.",
    "google": "Captura de demanda ativa (pesquisa e Perfil da Empresa no Google).",
    "email": "Nutrição e retenção da base de clientes.",
    "youtube": "Vídeos tutoriais de longa duração e shorts.",
}

# Datas sazonais fixas do varejo brasileiro (mês, dia, nome)
DATAS_SAZONAIS = [
    (3, 8, "Dia da Mulher"), (3, 15, "Dia do Consumidor"), (6, 12, "Dia dos Namorados"),
    (9, 15, "Dia do Cliente"), (10, 12, "Dia das Crianças"), (12, 25, "Natal"),
]


def _black_friday(ano: int) -> date:
    novembro = date(ano, 11, 1)
    primeira_quinta = novembro + timedelta(days=(3 - novembro.weekday()) % 7)
    return primeira_quinta + timedelta(days=22)  # 4ª quinta + 1 dia = sexta


def _domingo_n(ano: int, mes: int, n: int) -> date:
    d = date(ano, mes, 1)
    primeiro = d + timedelta(days=(6 - d.weekday()) % 7)
    return primeiro + timedelta(weeks=n - 1)


def datas_no_periodo(inicio: date, fim: date) -> list[tuple[date, str]]:
    datas = []
    for ano in range(inicio.year, fim.year + 1):
        candidatos = [(date(ano, m, d), nome) for m, d, nome in DATAS_SAZONAIS]
        candidatos += [
            (_domingo_n(ano, 5, 2), "Dia das Mães"),
            (_domingo_n(ano, 8, 2), "Dia dos Pais"),
            (_black_friday(ano), "Black Friday"),
        ]
        datas += [(d, n) for d, n in candidatos if inicio <= d <= fim]
    return sorted(datas)


@dataclass
class Briefing:
    nome: str
    objetivo: str
    orcamento: float
    dias: int
    canais: list[str]
    publico: str = "a definir"
    inicio: date | None = None
    posts_semana: int = 5


def planejar(b: Briefing) -> dict:
    if b.objetivo not in OBJETIVOS:
        raise ValueError(f"Objetivo inválido: {b.objetivo}. Use: {', '.join(OBJETIVOS)}")
    if b.dias < 3:
        raise ValueError("A campanha precisa ter pelo menos 3 dias.")
    canais = [c.strip().lower() for c in b.canais if c.strip()] or ["instagram"]
    inicio = b.inicio or date.today()
    fim = inicio + timedelta(days=b.dias - 1)
    cfg = OBJETIVOS[b.objetivo]

    # Fases em sequência, duração proporcional ao peso do funil (mínimo 1 dia)
    fases, cursor, restante = [], inicio, b.dias
    etapas = list(cfg["funil"].items())
    for i, (etapa, peso) in enumerate(etapas):
        dur = restante if i == len(etapas) - 1 else max(1, round(b.dias * peso))
        dur = min(dur, restante - (len(etapas) - 1 - i))
        nome, meta, formatos = FASES_FUNIL[etapa]
        fases.append({
            "etapa": etapa, "nome": nome, "objetivo": meta, "formatos": formatos,
            "inicio": cursor, "fim": cursor + timedelta(days=dur - 1), "dias": dur,
            "verba": b.orcamento * 0.85 * peso,
        })
        cursor += timedelta(days=dur)
        restante -= dur

    # Verba por canal: WhatsApp/e-mail têm custo de mídia baixo
    pesos_canal = {c: (0.3 if c in ("whatsapp", "email") else 1.0) for c in canais}
    total_pesos = sum(pesos_canal.values())
    verba_canal = {c: b.orcamento * 0.85 * p / total_pesos for c, p in pesos_canal.items()}

    # Calendário: distribui N posts por semana em dias alternados
    dias_post = {0: [0], 1: [2], 2: [0, 3], 3: [0, 2, 4], 4: [0, 1, 3, 4], 5: [0, 1, 2, 3, 4],
                 6: [0, 1, 2, 3, 4, 5], 7: list(range(7))}
    semana_padrao = dias_post[max(1, min(7, b.posts_semana))]
    # Canais de mensagem (WhatsApp/e-mail) não recebem reels/carrossel: entram só na oferta
    mensageria = [c for c in canais if c in ("whatsapp", "email")]
    sociais = [c for c in canais if c not in mensageria] or canais
    calendario = []
    dia = inicio
    while dia <= fim:
        if dia.weekday() in semana_padrao:
            fase = next(f for f in fases if f["inicio"] <= dia <= f["fim"])
            formatos = [f for f in fase["formatos"] if f != "Mensagem no WhatsApp" or "whatsapp" in canais]
            n_fase = len([c for c in calendario if c["fase"] == fase["nome"]])
            formato = formatos[n_fase % len(formatos)]
            if formato == "Mensagem no WhatsApp":
                canal = "whatsapp"
            else:
                canal = sociais[len([c for c in calendario if c["canal"] in sociais]) % len(sociais)]
            calendario.append({"data": dia, "fase": fase["nome"], "formato": formato, "canal": canal})
        dia += timedelta(days=1)
    if mensageria and not any(c["canal"] in mensageria for c in calendario):
        oferta = fases[-1]
        calendario.append({"data": oferta["inicio"], "fase": oferta["nome"],
                           "formato": "Mensagem de oferta para a base", "canal": mensageria[0]})
        calendario.sort(key=lambda c: c["data"])

    return {
        "briefing": b, "canais": canais, "inicio": inicio, "fim": fim,
        "objetivo": cfg, "fases": fases, "verba_canal": verba_canal,
        "reserva": b.orcamento * 0.15, "calendario": calendario,
        "datas": datas_no_periodo(inicio, fim),
        "papeis": {c: PAPEL_CANAL.get(c, "Canal complementar.") for c in canais},
    }
