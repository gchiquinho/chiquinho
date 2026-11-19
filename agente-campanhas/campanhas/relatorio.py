"""Formatação dos resultados em Markdown."""

from __future__ import annotations

from .estrategia import recomendar


def _brl(valor: float) -> str:
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def _int(valor: float) -> str:
    return f"{valor:,.0f}".replace(",", ".")


def _pct(valor: float, casas: int = 1) -> str:
    return f"{valor * 100:.{casas}f}%".replace(".", ",")


def _tabela_grupos(titulo: str, grupos: dict[str, dict]) -> list[str]:
    if not grupos:
        return []
    linhas = [f"### {titulo}", "", "| | Posts | Alcance médio | Engajamento | Salvamento | CTR |",
              "|---|---:|---:|---:|---:|---:|"]
    for nome, g in sorted(grupos.items(), key=lambda kv: kv[1]["taxa_engajamento"], reverse=True):
        linhas.append(f"| {nome} | {g['posts']} | {_int(g['alcance_medio'])} | {_pct(g['taxa_engajamento'])} "
                      f"| {_pct(g['taxa_salvamento'], 2)} | {_pct(g['ctr'], 2)} |")
    return linhas + [""]


def relatorio_engajamento(analise: dict, titulo: str = "Relatório de Engajamento") -> str:
    g = analise["geral"]
    c = analise["classificacao"]
    ini, fim = analise["periodo"]
    out = [f"# {titulo}", "", f"**Período:** {ini:%d/%m/%Y} a {fim:%d/%m/%Y} · **Posts analisados:** {g['posts']}", "",
           "## Visão geral", "", "| Métrica | Valor | Referência |", "|---|---:|---|",
           f"| Alcance total | {_int(g['alcance'])} | |",
           f"| Alcance médio por post | {_int(g['alcance_medio'])} | |",
           f"| Interações | {_int(g['interacoes'])} | |",
           f"| Taxa de engajamento | {_pct(g['taxa_engajamento'])} | {c['taxa_engajamento']} |",
           f"| Taxa de salvamento | {_pct(g['taxa_salvamento'], 2)} | {c['taxa_salvamento']} |",
           f"| Taxa de compartilhamento | {_pct(g['taxa_compartilhamento'], 2)} | |"]
    if g["cliques"]:
        out.append(f"| CTR | {_pct(g['ctr'], 2)} | {c['ctr']} |")
        out.append(f"| Conversão (cliques → vendas) | {_pct(g['taxa_conversao'])} | {c['taxa_conversao']} |")
    if g["investimento"]:
        out.append(f"| Investimento | {_brl(g['investimento'])} | |")
        if g["cliques"]:
            out.append(f"| Custo por clique | {_brl(g['custo_por_clique'])} | |")
        if g["conversoes"]:
            out.append(f"| Custo por conversão | {_brl(g['custo_por_conversao'])} | |")
    out.append("")

    t = analise.get("tendencia")
    if t:
        sentido = "alta" if t["variacao"] > 0.05 else "queda" if t["variacao"] < -0.05 else "estável"
        out += [f"**Tendência:** {sentido} — engajamento foi de {_pct(t['antes'])} (1ª metade) "
                f"para {_pct(t['depois'])} (2ª metade), variação de {_pct(t['variacao'])}.", ""]

    out += ["## Desempenho por segmento", ""]
    if len(analise["por_canal"]) > 1:
        out += _tabela_grupos("Por canal", analise["por_canal"])
    out += _tabela_grupos("Por formato", analise["por_formato"])
    out += _tabela_grupos("Por dia da semana", analise["por_dia"])
    out += _tabela_grupos("Por faixa horária", analise["por_faixa"])

    out += ["## Melhores posts", "", "| Data | Canal | Formato | Tema | Alcance | Engajamento |",
            "|---|---|---|---|---:|---:|"]
    for p in analise["top"]:
        tema = p.extras.get("tema") or p.extras.get("legenda", "")[:40]
        out.append(f"| {p.data:%d/%m %H:%M} | {p.canal} | {p.formato} | {tema} | {_int(p.alcance)} "
                   f"| {_pct(p.taxa_engajamento)} |")
    out.append("")
    if analise["piores"]:
        out += ["## Posts abaixo do esperado", ""]
        for p in analise["piores"]:
            tema = p.extras.get("tema") or p.formato
            out.append(f"- {p.data:%d/%m} · {p.formato} · {tema} — {_pct(p.taxa_engajamento)}")
        out.append("")

    recs = recomendar(analise)
    out += ["## Ações recomendadas", ""]
    if not recs:
        out.append("_Dados insuficientes para recomendações automáticas — inclua mais posts e formatos._")
    for i, r in enumerate(recs, 1):
        out += [f"{i}. {r['acao']}", f"   - **Por quê:** {r['motivo']}", f"   - **Impacto:** {r['impacto']}",
                f"   - **Como medir:** {r['medicao']}"]
    out += ["", "_Referências: engajamento bom 2–5%, salvamento 0,5–1,5%, CTR 0,8–2% (orgânico, contas pequenas/médias). "
            "O melhor benchmark é o histórico da própria conta._", ""]
    return "\n".join(out)


def relatorio_plano(plano: dict) -> str:
    b = plano["briefing"]
    cfg = plano["objetivo"]
    out = [f"# Plano de Campanha — {b.nome}", "",
           f"**Objetivo:** {b.objetivo} — {cfg['descricao']}  ",
           f"**Período:** {plano['inicio']:%d/%m/%Y} a {plano['fim']:%d/%m/%Y} ({b.dias} dias)  ",
           f"**Orçamento:** {_brl(b.orcamento)}  ",
           f"**Público:** {b.publico}  ",
           f"**Canais:** {', '.join(plano['canais'])}", ""]

    if plano["datas"]:
        out += ["> **Datas sazonais no período:** " +
                ", ".join(f"{n} ({d:%d/%m})" for d, n in plano["datas"]) +
                " — aproveite como gancho de oferta.", ""]

    out += ["## Papel de cada canal", ""]
    out += [f"- **{c}:** {p}" for c, p in plano["papeis"].items()] + [""]

    out += ["## Funil e fases", "", "| Fase | Período | Objetivo | Formatos | Verba |", "|---|---|---|---|---:|"]
    for f in plano["fases"]:
        out.append(f"| {f['nome']} ({f['etapa']}) | {f['inicio']:%d/%m}–{f['fim']:%d/%m} | {f['objetivo']} "
                   f"| {', '.join(f['formatos'])} | {_brl(f['verba'])} |")
    out += ["", "## Verba", "", "| Destino | Valor |", "|---|---:|"]
    out += [f"| Mídia — {c} | {_brl(v)} |" for c, v in plano["verba_canal"].items()]
    out += [f"| Reserva para testes A/B e escalar o que funcionar (15%) | {_brl(plano['reserva'])} |", ""]

    out += ["## KPIs", ""] + [f"- {k}" for k in cfg["kpis"]] + [
        "", "Defina a meta de cada KPI com base no histórico (ex.: +20% sobre a média dos últimos 30 dias).", "",
        "## Calendário de conteúdo", "", "| Data | Dia | Fase | Canal | Formato | Tema / copy |",
        "|---|---|---|---|---|---|"]
    dias = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
    for item in plano["calendario"]:
        out.append(f"| {item['data']:%d/%m} | {dias[item['data'].weekday()]} | {item['fase']} | {item['canal']} "
                   f"| {item['formato']} | _a definir_ |")
    out += ["", "## Rotina de acompanhamento", "",
            "- **Diário:** responder comentários e directs em até 1h; acompanhar gasto dos anúncios.",
            "- **A cada 3 dias:** pausar anúncios com CTR < 0,8% e realocar para os melhores.",
            "- **Semanal:** rodar `python -m campanhas analisar` com os dados exportados e ajustar o calendário.",
            "- **Final:** relatório com resultado vs. meta, aprendizados e o que repetir na próxima campanha.", "",
            "## Riscos e plano B", "",
            "- Baixo alcance na fase de aquecimento → impulsionar os 2 melhores reels orgânicos.",
            "- Muitos cliques e poucas vendas → revisar oferta, preço e tempo de resposta no WhatsApp.",
            "- Fadiga de criativo (frequência > 3) → trocar arte/gancho mantendo a oferta.", ""]
    return "\n".join(out)
