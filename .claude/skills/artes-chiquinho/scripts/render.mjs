#!/usr/bin/env node
// Gera artes PNG a partir de um roteiro JSON.
// Uso: node render.mjs <roteiro.json> [--saida pasta] [--so nome1,nome2] [--so-html]
// --so-html: só grava os .html (para passar ao criar_arte do plugin quando não houver Playwright)
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { FORMATOS, MODELOS, css } from "./modelos.mjs";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const args = process.argv.slice(2);
if (!args[0] || args[0] === "-h" || args[0] === "--help") {
  console.log(`Uso: node render.mjs <roteiro.json> [--saida pasta] [--so nome1,nome2] [--so-html]
Modelos: ${Object.keys(MODELOS).join(", ")}
Formatos: ${Object.keys(FORMATOS).join(", ")}`);
  process.exit(args[0] ? 0 : 1);
}
const opt = (flag) => {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
};

const roteiroPath = path.resolve(args[0]);
const roteiro = JSON.parse(fs.readFileSync(roteiroPath, "utf8"));
const base = JSON.parse(fs.readFileSync(path.join(AQUI, "..", "identidade.json"), "utf8"));
const id = { ...base, ...(roteiro.identidade || {}), cores: { ...base.cores, ...(roteiro.identidade?.cores || {}) } };
const saida = path.resolve(path.dirname(roteiroPath), opt("--saida") || roteiro.saida || ".");
const so = opt("--so")?.split(",");
const soHtml = args.includes("--so-html");
let chromium = null;
if (!soHtml) {
  try {
    ({ chromium } = require("playwright"));
  } catch {
    console.error("Playwright não encontrado. Instale com: npm i -g playwright && npx playwright install chromium\n" +
      "ou rode com --so-html e passe cada .html para a ferramenta criar_arte do plugin.");
    process.exit(2);
  }
}
fs.mkdirSync(saida, { recursive: true });

const fonte = `<link href="https://fonts.googleapis.com/css2?family=${encodeURIComponent(id.fonte)}:wght@500;700;900&display=swap" rel="stylesheet">`;
const avisos = [];
const geradas = [];

const browser = soHtml ? null : await chromium.launch();
try {
  for (const arte of roteiro.artes) {
    if (so && !so.includes(arte.nome)) continue;
    const modelo = MODELOS[arte.modelo];
    if (!modelo) throw new Error(`${arte.nome}: modelo "${arte.modelo}" não existe (${Object.keys(MODELOS).join(", ")})`);
    const formato = arte.formato || (["story", "contagem", "story_produto"].includes(arte.modelo) ? "story" : arte.modelo === "whatsapp" ? "whatsapp_cabecalho" : roteiro.formato || "feed_retrato");
    const [w, h] = FORMATOS[formato] || [];
    if (!w) throw new Error(`${arte.nome}: formato "${formato}" inválido`);

    const dados = arte.dados || {};
    const textoBruto = JSON.stringify(dados);
    if (/\[[^\]]*\]/.test(textoBruto)) avisos.push(`${arte.nome}: tem campo entre [colchetes] não preenchido`);

    const classes = ["r", arte.tema === "claro" ? "claro" : arte.tema === "metal" ? "metal" : "", arte.modelo === "whatsapp" ? "wa-r" : ""].join(" ");
    const html = `<!doctype html><html><head><meta charset="utf-8">${fonte}<style>${css(id, w, h)}</style></head>
<body><div class="${classes}">${modelo(dados, id)}</div></body></html>`;

    const htmlPath = path.join(saida, `${arte.nome}.html`);
    const pngPath = path.join(saida, `${arte.nome}.png`);
    fs.writeFileSync(htmlPath, html);
    if (soHtml) {
      console.log(`📄 ${htmlPath} (${formato})`);
      continue;
    }

    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle" }).catch(() => {});
    await page.evaluate(() => document.fonts.ready);
    // Checa se algum texto invade o rodapé ou sai da arte
    const invade = await page.evaluate(() => {
      const r = document.querySelector(".r");
      const limite = (document.querySelector(".base") || document.querySelector(".rodape") || document.querySelector(".story-chamada"))
        ?.getBoundingClientRect().top ?? r.clientHeight;
      return [...r.querySelectorAll("h1,h2,p:not(.condicoes),.caixa,.paleta,.tabela,.precos,.cupom")]
        .filter((el) => !el.closest(".story-centro, .sp") || el.getBoundingClientRect().bottom > r.clientHeight - 250)
        .some((el) => el.getBoundingClientRect().bottom > limite - 10 || el.scrollWidth > el.clientWidth + 2);
    });
    if (invade) avisos.push(`${arte.nome}: texto grande demais — invade o rodapé ou a faixa; encurte o texto`);
    await page.locator(".r").screenshot({ path: pngPath });
    await page.close();
    geradas.push({ nome: arte.nome, png: pngPath, w, h });
    console.log(`🖼️  ${pngPath} (${w}x${h})`);
  }

  // Prévia: todas as artes lado a lado num PNG só
  if (!soHtml && geradas.length > 1) {
    const larg = 360;
    const cards = geradas
      .map((g) => `<figure><img src="${pathToFileURL(g.png).href}" style="width:${larg}px;height:${Math.round((g.h / g.w) * larg)}px"><figcaption>${g.nome}</figcaption></figure>`)
      .join("");
    const previaHtml = path.join(saida, "_previa.html");
    fs.writeFileSync(previaHtml, `<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#8a8a8f;font:16px Arial}
      .g{display:flex;flex-wrap:wrap;gap:14px;padding:14px;width:${larg * 3 + 14 * 4}px}figure{margin:0}figcaption{color:#fff;padding-top:4px}</style>
      <div class="g">${cards}</div>`);
    const page = await browser.newPage({ viewport: { width: larg * 3 + 56, height: 600 } });
    await page.goto(pathToFileURL(previaHtml).href);
    await page.locator(".g").screenshot({ path: path.join(saida, "_previa.png") });
    await page.close();
    fs.unlinkSync(previaHtml);
    console.log(`👀 Prévia: ${path.join(saida, "_previa.png")}`);
  }
} finally {
  await browser?.close();
}

if (avisos.length) {
  console.log("\n⚠️  Avisos:");
  avisos.forEach((a) => console.log(" - " + a));
}
