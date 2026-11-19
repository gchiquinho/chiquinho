// Modelos de arte. Cada modelo recebe (dados, id) e devolve o HTML do conteúdo.
// Textos aceitam HTML simples: <b>, <br>, <span class="hl"> (laranja).

export const FORMATOS = {
  feed_retrato: [1080, 1350],
  feed_quadrado: [1080, 1080],
  story: [1080, 1920],
  facebook_paisagem: [1200, 630],
  whatsapp_cabecalho: [1125, 600],
};

const esc = (v) => (v === undefined || v === null ? "" : String(v));

const faixa = (id, altura = 90) =>
  `<div class="faixa" style="height:${altura}px">${id.faixa_cores.map((c) => `<i style="background:${c}"></i>`).join("")}</div>`;

const rodape = (id, d) => {
  const direita = esc(d.pagina ?? "");
  return `<div class="rodape"><span>${id.instagram} · ${id.cidade}</span><span>${direita}</span></div>`;
};

export const MODELOS = {
  /** Capa de carrossel: etiqueta, titulo, subtitulo, faixa(bool) */
  capa: (d, id) => `
    <span class="etiqueta">${esc(d.etiqueta)}</span>
    <h1>${esc(d.titulo)}</h1>
    ${d.subtitulo ? `<p>${d.subtitulo}</p>` : ""}
    ${d.faixa === false ? "" : `<div class="base">${faixa(id, 110)}</div>`}
    ${rodape(id, { pagina: d.pagina ?? "arraste →" })}`,

  /** Passo numerado: numero, titulo, texto, destaque (caixa opcional) */
  passo: (d, id) => `
    <div class="numero">${esc(d.numero)}</div>
    <h2>${esc(d.titulo)}</h2>
    <p>${esc(d.texto)}</p>
    ${d.destaque ? `<div class="caixa">${d.destaque}</div>` : ""}
    ${rodape(id, d)}`,

  /** Fechamento com chamada: etiqueta, titulo, texto, destaque */
  fechamento: (d, id) => `
    <span class="etiqueta">${esc(d.etiqueta || "FALE COM A GENTE")}</span>
    <h1>${esc(d.titulo)}</h1>
    ${d.texto ? `<p>${d.texto}</p>` : ""}
    ${d.destaque ? `<div class="caixa">${d.destaque}</div>` : ""}
    ${id.whatsapp ? `<p class="contato">📲 ${id.whatsapp}${id.endereco ? `<br>📍 ${id.endereco}` : ""}</p>` : ""}
    <div class="base">${faixa(id, 70)}</div>
    ${rodape(id, d)}`,

  /** Oferta: etiqueta, produto, preco_de, preco_por, selo (ex.: "-20%"), validade, condicoes, cupom */
  oferta: (d, id) => `
    <span class="etiqueta">${esc(d.etiqueta || "OFERTA")}</span>
    ${d.selo ? `<div class="selo">${esc(d.selo)}</div>` : ""}
    <h2 class="produto">${esc(d.produto)}</h2>
    <div class="precos">
      ${d.preco_de ? `<div class="de">de R$ ${esc(d.preco_de)}</div>` : ""}
      ${d.preco_por ? `<div class="por"><small>por R$</small> ${esc(d.preco_por)}</div>` : ""}
      ${d.beneficio ? `<div class="beneficio">${d.beneficio}</div>` : ""}
    </div>
    ${d.cupom ? `<div class="cupom">Cupom <b>${esc(d.cupom)}</b></div>` : ""}
    <p class="validade">${esc(d.validade)}${d.validade ? " · " : ""}enquanto durar o estoque</p>
    ${d.condicoes ? `<p class="condicoes">${esc(d.condicoes)}</p>` : ""}
    ${rodape(id, d)}`,

  /** Paleta: etiqueta, titulo, cores: [{hex, nome, codigo}] (3 a 6). Nome/código SEMPRE vindos do usuário. */
  paleta: (d, id) => `
    <span class="etiqueta">${esc(d.etiqueta || "PALETA")}</span>
    <h2>${esc(d.titulo)}</h2>
    <div class="paleta n${(d.cores || []).length}">
      ${(d.cores || [])
        .map((c) => `<div class="cor"><div class="amostra" style="background:${c.hex}"></div>
          <div class="nome">${esc(c.nome)}</div><div class="codigo">${esc(c.codigo)}</div></div>`)
        .join("")}
    </div>
    ${rodape(id, d)}`,

  /** Story: etiqueta, titulo, texto, chamada (rodapé). Respeita 250 px livres em cima e embaixo. */
  story: (d, id) => `
    <div class="story-centro">
      ${d.etiqueta ? `<span class="etiqueta">${esc(d.etiqueta)}</span>` : ""}
      <h1>${esc(d.titulo)}</h1>
      ${d.texto ? `<p>${d.texto}</p>` : ""}
    </div>
    ${d.chamada ? `<div class="story-chamada">${d.chamada}</div>` : ""}
    <div class="story-marca">${id.instagram}</div>`,

  /** Contagem regressiva em story: etiqueta, numero (dias), unidade, titulo, chamada */
  contagem: (d, id) => `
    <div class="story-centro">
      <span class="etiqueta">${esc(d.etiqueta || "FALTAM")}</span>
      <div class="numero gigante">${esc(d.numero)}</div>
      <div class="unidade">${esc(d.unidade || "dias")}</div>
      <h2>${esc(d.titulo)}</h2>
    </div>
    ${d.chamada ? `<div class="story-chamada">${d.chamada}</div>` : ""}
    <div class="story-marca">${id.instagram}</div>`,


  /** Story de produto com preço: etiqueta, produto, detalhe, embalagem, preco, por_litro, chamada, validade.
   *  Lata desenhada em CSS (cor_lata, cor_rotulo) quando não houver foto; use `foto` (URL/caminho) se tiver. */
  story_produto: (d, id) => `
    <div class="sp">
      ${d.etiqueta ? `<span class="etiqueta">${esc(d.etiqueta)}</span>` : ""}
      <h1 class="sp-produto">${esc(d.produto)}</h1>
      ${d.detalhe ? `<div class="sp-detalhe">${esc(d.detalhe)}</div>` : ""}
      <div class="sp-meio">
        ${d.foto ? `<img class="sp-foto" src="${esc(d.foto)}">` : `<div class="lata" style="--lata:${esc(d.cor_lata || "#111")};--rot:${esc(d.cor_rotulo || id.cores.destaque)}">
          <div class="tampa"></div><div class="corpo"><div class="rot">${esc(d.rotulo || "")}</div></div></div>`}
        <div class="sp-preco">
          ${d.embalagem ? `<div class="sp-emb">${esc(d.embalagem)}</div>` : ""}
          <div class="sp-valor"><small>R$</small>${esc(d.preco)}</div>
          ${d.por_litro ? `<div class="sp-litro">${d.por_litro}</div>` : ""}
        </div>
      </div>
      ${d.validade ? `<div class="sp-validade">${esc(d.validade)}</div>` : ""}
    </div>
    ${d.chamada ? `<div class="story-chamada">${d.chamada}</div>` : ""}
    <div class="story-marca">${esc(id.assinatura || id.instagram)}</div>`,

  /** Aviso/mensagem (horário de feriado, boas festas): etiqueta, titulo, linhas: [[rótulo, valor]], texto */
  aviso: (d, id) => `
    <span class="etiqueta">${esc(d.etiqueta || "AVISO")}</span>
    <h2>${esc(d.titulo)}</h2>
    ${d.texto ? `<p>${d.texto}</p>` : ""}
    ${d.linhas ? `<div class="tabela">${d.linhas.map(([a, b]) => `<div><span>${esc(a)}</span><b>${esc(b)}</b></div>`).join("")}</div>` : ""}
    <div class="base">${faixa(id, 70)}</div>
    ${rodape(id, d)}`,

  /** Antes e depois: antes (URL https ou caminho local), depois, titulo. Só fotos reais da loja/cliente. */
  antes_depois: (d, id) => `
    <div class="ad">
      <div style="background-image:url('${esc(d.antes)}')"><span>ANTES</span></div>
      <div style="background-image:url('${esc(d.depois)}')"><span class="dep">DEPOIS</span></div>
    </div>
    ${d.titulo ? `<div class="ad-titulo">${esc(d.titulo)}</div>` : ""}
    ${rodape(id, d)}`,

  /** Cabeçalho de mensagem modelo do WhatsApp (1125x600): etiqueta, titulo, texto */
  whatsapp: (d, id) => `
    <div class="wa">
      <span class="etiqueta">${esc(d.etiqueta || "")}</span>
      <h2>${esc(d.titulo)}</h2>
      ${d.texto ? `<p>${d.texto}</p>` : ""}
    </div>
    <div class="wa-faixa">${faixa(id, 30)}</div>`,
};

export function css(id, largura, altura) {
  const c = id.cores;
  return `
*{margin:0;padding:0;box-sizing:border-box}
body{background:${c.fundo}}
.r{width:${largura}px;height:${altura}px;overflow:hidden;position:relative;background:${c.fundo};color:${c.texto};
  font-family:'${id.fonte}',Arial,sans-serif;padding:110px 90px}
.r.claro{background:${c.fundo_claro};color:${c.texto_escuro}}
.r.claro p{color:#3a3a3d}.r.claro .caixa{background:#ebe5da}
.hl{color:${c.destaque}}
.etiqueta{display:inline-block;background:${c.destaque};color:${c.texto_escuro};font-weight:900;font-size:30px;letter-spacing:3px;padding:14px 26px;border-radius:8px}
h1{font-size:104px;line-height:1.02;font-weight:900;margin-top:70px}
h2{font-size:84px;line-height:1.05;font-weight:900;margin-top:40px}
p{font-size:44px;line-height:1.35;font-weight:500;margin-top:44px;color:#e8e8ea}
.numero{font-size:230px;font-weight:900;color:${c.destaque};line-height:1}
.caixa{margin-top:50px;background:${c.caixa};border-left:12px solid ${c.destaque};border-radius:12px;padding:34px 40px;font-size:44px;font-weight:700;line-height:1.3}
.contato{font-size:40px;font-weight:700}
.base{position:absolute;left:90px;right:90px;bottom:200px}
.faixa{display:flex;border-radius:14px;overflow:hidden}.faixa i{flex:1;display:block}
.rodape{position:absolute;left:90px;right:90px;bottom:80px;display:flex;justify-content:space-between;font-size:30px;color:${c.secundario};font-weight:500;border-top:2px solid ${c.linha};padding-top:30px}
/* oferta */
.selo{position:absolute;right:90px;top:90px;width:250px;height:250px;border-radius:50%;background:${c.destaque};color:${c.texto_escuro};
  display:flex;align-items:center;justify-content:center;font-size:84px;font-weight:900;transform:rotate(-10deg)}
.produto{margin-top:90px;max-width:640px}
.precos{margin-top:50px}.de{font-size:48px;color:${c.secundario};text-decoration:line-through;font-weight:700}
.por{font-size:150px;font-weight:900;color:${c.destaque};line-height:1}.por small{font-size:56px}
.beneficio{font-size:64px;font-weight:900;line-height:1.15;color:${c.destaque}}
.cupom{display:inline-block;margin-top:50px;border:4px dashed ${c.destaque};border-radius:14px;padding:22px 36px;font-size:44px}
.validade{font-size:38px;font-weight:700;color:${c.texto}}
.condicoes{position:absolute;left:90px;right:90px;bottom:170px;font-size:26px;line-height:1.3;margin:0;color:${c.secundario}}
/* paleta */
.paleta{display:grid;gap:30px;margin-top:60px;grid-template-columns:1fr 1fr}
.paleta.n3{grid-template-columns:1fr}.paleta.n3 .amostra{height:200px}
.amostra{height:250px;border-radius:16px;border:2px solid rgba(255,255,255,.15)}
.cor .nome{font-size:36px;font-weight:700;margin-top:14px}.cor .codigo{font-size:28px;color:${c.secundario}}
.paleta.n5 .cor:last-child{grid-column:span 2}.paleta.n5 .amostra,.paleta.n6 .amostra{height:170px}
/* story */
.story-centro{position:absolute;left:90px;right:90px;top:250px;bottom:420px;display:flex;flex-direction:column;justify-content:center}
.story-centro h1{font-size:120px}
.story-centro .etiqueta{align-self:flex-start}
.story-chamada{position:absolute;left:90px;right:90px;bottom:280px;background:${c.destaque};color:${c.texto_escuro};text-align:center;
  font-size:48px;font-weight:900;padding:36px;border-radius:20px}
.story-marca{position:absolute;left:0;right:0;bottom:260px;text-align:center;font-size:28px;color:${c.secundario};transform:translateY(130px)}
.gigante{font-size:420px;margin-top:20px}.unidade{font-size:70px;font-weight:900;margin-top:-20px}
/* story de produto */
.r.metal{background:radial-gradient(ellipse at 50% 38%,#4a4a4d 0%,#2a2a2c 45%,#141415 100%)}
.r.metal::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.035) 0 2px,transparent 2px 5px)}
.sp{position:absolute;left:90px;right:90px;top:250px;bottom:420px;display:flex;flex-direction:column}
.sp .etiqueta{align-self:flex-start}
.sp-produto{font-size:118px;margin-top:40px;font-style:italic;text-transform:uppercase;line-height:.95;letter-spacing:-2px}
.sp-detalhe{font-size:46px;font-weight:700;color:${c.destaque};margin-top:18px;font-style:italic;text-transform:uppercase;letter-spacing:2px}
.sp-meio{flex:1;display:flex;align-items:center;gap:40px;margin-top:30px}
.sp-foto{width:400px;object-fit:contain;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6)) drop-shadow(0 0 60px ${c.destaque}55)}
.lata{width:360px;position:relative;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6)) drop-shadow(0 0 60px ${c.destaque}55)}
.lata .tampa{height:46px;border-radius:50%;background:linear-gradient(90deg,#777,#ddd 40%,#888);position:relative;z-index:2}
.lata .corpo{height:420px;margin-top:-23px;border-radius:0 0 30px 30px / 0 0 22px 22px;background:linear-gradient(90deg,#000 0%,var(--lata) 18%,#555 32%,var(--lata) 48%,#000 100%);display:flex;align-items:center;justify-content:center}
.lata .rot{width:100%;background:var(--rot);color:#111;font-weight:900;font-style:italic;font-size:52px;text-align:center;padding:26px 10px;text-transform:uppercase;line-height:1}
.sp-preco{flex:1}
.sp-emb{font-size:40px;font-weight:700;color:${c.secundario};text-transform:uppercase}
.sp-valor{font-size:126px;font-weight:900;font-style:italic;color:${c.texto};line-height:1;letter-spacing:-4px;margin-top:6px}
.sp-valor small{font-size:56px;color:${c.destaque};margin-right:8px;letter-spacing:0}
.sp-litro{margin-top:26px;background:${c.destaque};color:#111;font-size:38px;font-weight:800;padding:18px 24px;border-radius:14px;line-height:1.2}
.sp-validade{font-size:32px;color:${c.secundario};margin-top:20px}
/* aviso */
.tabela{margin-top:50px;display:flex;flex-direction:column;gap:18px}
.tabela div{display:flex;justify-content:space-between;background:${c.caixa};border-radius:12px;padding:26px 36px;font-size:42px}
.tabela b{color:${c.destaque}}
/* antes e depois */
.r .ad{position:absolute;inset:0;display:flex;flex-direction:column}
.ad div{flex:1;background-size:cover;background-position:center;position:relative}
.ad span{position:absolute;left:60px;top:50px;background:${c.fundo};color:${c.texto};font-weight:900;font-size:40px;padding:12px 26px;border-radius:8px}
.ad span.dep{background:${c.destaque};color:${c.texto_escuro}}
.ad-titulo{position:absolute;left:60px;right:60px;bottom:150px;background:rgba(29,29,31,.85);padding:26px 34px;border-radius:14px;font-size:48px;font-weight:900}
/* whatsapp */
.r.wa-r{padding:70px 80px}.wa h2{font-size:78px;margin-top:30px}.wa p{font-size:38px;margin-top:20px}
.wa-faixa{position:absolute;left:0;right:0;bottom:0}.wa-faixa .faixa{border-radius:0}
`;
}
