import tempfile
import unittest
from datetime import date
from pathlib import Path

from campanhas import Briefing, analisar, carregar_csv, planejar, recomendar
from campanhas.cli import main
from campanhas.estrategia import _black_friday, datas_no_periodo
from campanhas.metricas import _numero

EXEMPLO = Path(__file__).resolve().parent.parent / "dados" / "exemplo_posts.csv"


class TestMetricas(unittest.TestCase):
    def test_numero_formato_brasileiro(self):
        self.assertEqual(_numero("1.234,56"), 1234.56)
        self.assertEqual(_numero("R$ 50"), 50)
        self.assertEqual(_numero(""), 0)

    def test_csv_ponto_e_virgula_e_taxa(self):
        with tempfile.TemporaryDirectory() as d:
            arq = Path(d) / "p.csv"
            arq.write_text("data;formato;alcance;curtidas;comentarios;salvamentos\n"
                           "2026-01-05 19:00;reels;1000;40;5;5\n"
                           "2026-01-06;feed;1000;10;0;0\n", encoding="utf-8")
            posts = carregar_csv(arq)
        self.assertEqual(len(posts), 2)
        self.assertAlmostEqual(posts[0].taxa_engajamento, 0.05)
        a = analisar(posts)
        self.assertAlmostEqual(a["geral"]["taxa_engajamento"], 0.03)
        self.assertEqual(list(a["por_faixa"]), ["noite (18-23h)"])  # post sem hora fica fora

    def test_data_invalida(self):
        with tempfile.TemporaryDirectory() as d:
            arq = Path(d) / "p.csv"
            arq.write_text("data,alcance\nontem,10\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                carregar_csv(arq)

    def test_exemplo_gera_recomendacoes(self):
        a = analisar(carregar_csv(EXEMPLO))
        self.assertEqual(a["geral"]["posts"], 48)
        recs = recomendar(a)
        self.assertTrue(recs)
        self.assertTrue(any("reels" in r["acao"] for r in recs))


class TestPlanejamento(unittest.TestCase):
    def test_black_friday(self):
        self.assertEqual(_black_friday(2026), date(2026, 11, 27))
        self.assertEqual(_black_friday(2025), date(2025, 11, 28))

    def test_datas_sazonais(self):
        nomes = [n for _, n in datas_no_periodo(date(2026, 5, 1), date(2026, 5, 31))]
        self.assertIn("Dia das Mães", nomes)

    def test_plano_fases_cobrem_periodo_e_verba(self):
        b = Briefing("Teste", "conversao", 1000, 21, ["instagram", "whatsapp"], inicio=date(2026, 11, 10))
        p = planejar(b)
        self.assertEqual(sum(f["dias"] for f in p["fases"]), 21)
        self.assertEqual(p["fases"][0]["inicio"], date(2026, 11, 10))
        self.assertEqual(p["fases"][-1]["fim"], date(2026, 11, 30))
        total = sum(p["verba_canal"].values()) + p["reserva"]
        self.assertAlmostEqual(total, 1000)
        self.assertAlmostEqual(sum(f["verba"] for f in p["fases"]), 850)
        for item in p["calendario"]:
            if item["canal"] == "whatsapp":
                self.assertNotIn("Reels", item["formato"])

    def test_google_fora_do_calendario_e_sem_post_no_natal(self):
        b = Briefing("Natal", "conversao", 1000, 31, ["instagram", "google"], inicio=date(2026, 12, 1), posts_semana=7)
        p = planejar(b)
        self.assertNotIn("google", {c["canal"] for c in p["calendario"]})
        self.assertNotIn(date(2026, 12, 25), {c["data"] for c in p["calendario"]})
        self.assertEqual(p["sempre_ativos"], ["google"])

    def test_objetivo_invalido(self):
        with self.assertRaises(ValueError):
            planejar(Briefing("x", "viralizar", 0, 10, ["instagram"]))

    def test_campanha_curta(self):
        p = planejar(Briefing("x", "engajamento", 300, 3, ["instagram"], inicio=date(2026, 1, 1)))
        self.assertEqual([f["dias"] for f in p["fases"]], [1, 1, 1])


class TestCli(unittest.TestCase):
    def test_comandos(self):
        with tempfile.TemporaryDirectory() as d:
            saida = Path(d) / "r.md"
            self.assertEqual(main(["analisar", str(EXEMPLO), "--saida", str(saida)]), 0)
            self.assertIn("Ações recomendadas", saida.read_text(encoding="utf-8"))
            self.assertEqual(main(["planejar", "--nome", "BF", "--objetivo", "leads", "--saida", str(saida)]), 0)
            self.assertIn("Plano de Campanha", saida.read_text(encoding="utf-8"))
        self.assertEqual(main(["analisar", "nao_existe.csv"]), 1)


if __name__ == "__main__":
    unittest.main()
