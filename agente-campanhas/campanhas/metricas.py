"""Leitura de dados de posts e cálculo de métricas de engajamento."""

from __future__ import annotations

import csv
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

DIAS_SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

CAMPOS_NUMERICOS = [
    "alcance",
    "impressoes",
    "curtidas",
    "comentarios",
    "compartilhamentos",
    "salvamentos",
    "cliques",
    "conversoes",
    "investimento",
]

# Referências de mercado (orgânico, contas pequenas/médias): (bom a partir de, ótimo a partir de)
BENCHMARKS = {
    "taxa_engajamento": (0.02, 0.05),
    "taxa_salvamento": (0.005, 0.015),
    "ctr": (0.008, 0.02),
    "taxa_conversao": (0.01, 0.03),
}


@dataclass
class Post:
    data: datetime
    canal: str
    formato: str
    alcance: float = 0
    impressoes: float = 0
    curtidas: float = 0
    comentarios: float = 0
    compartilhamentos: float = 0
    salvamentos: float = 0
    cliques: float = 0
    conversoes: float = 0
    investimento: float = 0
    tem_hora: bool = True
    extras: dict = field(default_factory=dict)

    @property
    def interacoes(self) -> float:
        return self.curtidas + self.comentarios + self.compartilhamentos + self.salvamentos

    @property
    def taxa_engajamento(self) -> float:
        return _div(self.interacoes, self.alcance)


def _div(a: float, b: float) -> float:
    return a / b if b else 0.0


def _numero(valor: str | None) -> float:
    if valor is None:
        return 0.0
    texto = str(valor).strip().replace("R$", "").replace("%", "").strip()
    if not texto:
        return 0.0
    # Aceita "1.234,56" (BR) e "1234.56"
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return 0.0


def _data(valor: str) -> tuple[datetime, bool]:
    texto = valor.strip()
    for formato, tem_hora in (
        ("%Y-%m-%d %H:%M", True),
        ("%Y-%m-%dT%H:%M", True),
        ("%Y-%m-%d %H:%M:%S", True),
        ("%d/%m/%Y %H:%M", True),
        ("%Y-%m-%d", False),
        ("%d/%m/%Y", False),
    ):
        try:
            return datetime.strptime(texto, formato), tem_hora
        except ValueError:
            continue
    raise ValueError(f"Data inválida: {valor!r} (use AAAA-MM-DD HH:MM)")


def carregar_csv(caminho: str | Path) -> list[Post]:
    """Lê o CSV de posts. Detecta separador ',' ou ';'."""
    caminho = Path(caminho)
    texto = caminho.read_text(encoding="utf-8-sig")
    primeira_linha = texto.splitlines()[0] if texto else ""
    separador = ";" if primeira_linha.count(";") > primeira_linha.count(",") else ","
    leitor = csv.DictReader(texto.splitlines(), delimiter=separador)
    if not leitor.fieldnames or "data" not in [c.strip().lower() for c in leitor.fieldnames]:
        raise ValueError("O CSV precisa ter ao menos a coluna 'data'.")

    posts: list[Post] = []
    for numero_linha, linha in enumerate(leitor, start=2):
        linha = {(k or "").strip().lower(): (v or "") for k, v in linha.items()}
        if not linha.get("data", "").strip():
            continue
        try:
            data, tem_hora = _data(linha["data"])
        except ValueError as erro:
            raise ValueError(f"Linha {numero_linha}: {erro}") from erro
        valores = {campo: _numero(linha.get(campo)) for campo in CAMPOS_NUMERICOS}
        extras = {k: v for k, v in linha.items() if k not in CAMPOS_NUMERICOS + ["data", "canal", "formato"]}
        posts.append(
            Post(
                data=data,
                canal=(linha.get("canal") or "instagram").strip().lower(),
                formato=(linha.get("formato") or "feed").strip().lower(),
                tem_hora=tem_hora,
                extras=extras,
                **valores,
            )
        )
    return posts


def _resumo(posts: list[Post]) -> dict:
    soma = {campo: sum(getattr(p, campo) for p in posts) for campo in CAMPOS_NUMERICOS}
    interacoes = sum(p.interacoes for p in posts)
    return {
        "posts": len(posts),
        **soma,
        "interacoes": interacoes,
        "taxa_engajamento": _div(interacoes, soma["alcance"]),
        "taxa_salvamento": _div(soma["salvamentos"], soma["alcance"]),
        "taxa_compartilhamento": _div(soma["compartilhamentos"], soma["alcance"]),
        "ctr": _div(soma["cliques"], soma["alcance"]),
        "taxa_conversao": _div(soma["conversoes"], soma["cliques"]),
        "alcance_medio": _div(soma["alcance"], len(posts)),
        "custo_por_conversao": _div(soma["investimento"], soma["conversoes"]),
        "custo_por_clique": _div(soma["investimento"], soma["cliques"]),
    }


def _agrupar(posts: list[Post], chave) -> dict[str, dict]:
    grupos: dict[str, list[Post]] = {}
    for post in posts:
        grupos.setdefault(chave(post), []).append(post)
    return {nome: _resumo(itens) for nome, itens in grupos.items()}


def classificar(metrica: str, valor: float) -> str:
    if metrica not in BENCHMARKS:
        return ""
    bom, otimo = BENCHMARKS[metrica]
    if valor >= otimo:
        return "ótimo"
    if valor >= bom:
        return "bom"
    return "fraco"


def faixa_horaria(hora: int) -> str:
    if 5 <= hora < 12:
        return "manhã (05-12h)"
    if 12 <= hora < 18:
        return "tarde (12-18h)"
    if 18 <= hora < 23:
        return "noite (18-23h)"
    return "madrugada (23-05h)"


def analisar(posts: list[Post]) -> dict:
    """Calcula o panorama completo de engajamento."""
    if not posts:
        raise ValueError("Nenhum post encontrado no arquivo.")

    posts = sorted(posts, key=lambda p: p.data)
    geral = _resumo(posts)
    taxas = [p.taxa_engajamento for p in posts if p.alcance]
    media = statistics.mean(taxas) if taxas else 0.0
    desvio = statistics.pstdev(taxas) if len(taxas) > 1 else 0.0

    outliers_alta, outliers_baixa = [], []
    for p in posts:
        if not p.alcance or not desvio:
            continue
        z = (p.taxa_engajamento - media) / desvio
        if z >= 1.5:
            outliers_alta.append((p, z))
        elif z <= -1.5:
            outliers_baixa.append((p, z))

    # Tendência: compara a primeira metade com a segunda metade do período
    meio = len(posts) // 2
    tendencia = None
    if meio >= 2:
        antes = _resumo(posts[:meio])["taxa_engajamento"]
        depois = _resumo(posts[meio:])["taxa_engajamento"]
        tendencia = {"antes": antes, "depois": depois, "variacao": _div(depois - antes, antes)}

    com_hora = [p for p in posts if p.tem_hora]
    return {
        "periodo": (posts[0].data, posts[-1].data),
        "geral": geral,
        "classificacao": {m: classificar(m, geral[m]) for m in BENCHMARKS},
        "por_canal": _agrupar(posts, lambda p: p.canal),
        "por_formato": _agrupar(posts, lambda p: p.formato),
        "por_dia": _agrupar(posts, lambda p: DIAS_SEMANA[p.data.weekday()]),
        "por_faixa": _agrupar(com_hora, lambda p: faixa_horaria(p.data.hour)) if com_hora else {},
        "top": sorted(posts, key=lambda p: p.taxa_engajamento, reverse=True)[:5],
        "piores": sorted([p for p in posts if p.alcance], key=lambda p: p.taxa_engajamento)[:3],
        "outliers_alta": outliers_alta,
        "outliers_baixa": outliers_baixa,
        "media_post": media,
        "desvio_post": desvio,
        "tendencia": tendencia,
    }
