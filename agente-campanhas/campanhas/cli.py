"""Interface de linha de comando: python -m campanhas <comando>."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from .estrategia import OBJETIVOS, Briefing, planejar
from .metricas import analisar, carregar_csv
from .relatorio import relatorio_engajamento, relatorio_plano


def _saida(texto: str, caminho: str | None) -> None:
    if caminho:
        Path(caminho).write_text(texto, encoding="utf-8")
        print(f"Relatório salvo em {caminho}")
    else:
        print(texto)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="campanhas", description="Agente de campanhas e análise de engajamento")
    sub = parser.add_subparsers(dest="comando", required=True)

    a = sub.add_parser("analisar", help="Analisa métricas de posts a partir de um CSV")
    a.add_argument("csv", help="Arquivo CSV com as métricas dos posts")
    a.add_argument("--canal", help="Filtrar por canal (ex.: instagram)")
    a.add_argument("--titulo", default="Relatório de Engajamento")
    a.add_argument("--saida", help="Salvar o relatório em arquivo .md")

    p = sub.add_parser("planejar", help="Gera um plano de campanha")
    p.add_argument("--nome", required=True)
    p.add_argument("--objetivo", required=True, choices=list(OBJETIVOS))
    p.add_argument("--orcamento", type=float, default=0)
    p.add_argument("--dias", type=int, default=30)
    p.add_argument("--canais", default="instagram,facebook")
    p.add_argument("--publico", default="a definir")
    p.add_argument("--inicio", help="Data de início AAAA-MM-DD (padrão: hoje)")
    p.add_argument("--posts-semana", type=int, default=5)
    p.add_argument("--saida", help="Salvar o plano em arquivo .md")

    args = parser.parse_args(argv)
    try:
        if args.comando == "analisar":
            posts = carregar_csv(args.csv)
            if args.canal:
                posts = [x for x in posts if x.canal == args.canal.lower()]
            _saida(relatorio_engajamento(analisar(posts), args.titulo), args.saida)
        else:
            briefing = Briefing(
                nome=args.nome, objetivo=args.objetivo, orcamento=args.orcamento, dias=args.dias,
                canais=args.canais.split(","), publico=args.publico,
                inicio=date.fromisoformat(args.inicio) if args.inicio else None,
                posts_semana=args.posts_semana,
            )
            _saida(relatorio_plano(planejar(briefing)), args.saida)
    except (ValueError, FileNotFoundError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    return 0
