"""Gera o carrossel de acabamentos da CooperTintas no padrão visual do grupo (HTML -> PNG)."""
import math, pathlib

NAVY = "#0A2478"; NAVY2 = "#071a5c"; OFF = "#F6F4EF"; GOLD = "#E8C46A"
LEQUE = ["#FFC20E", "#F7931E", "#E53935", "#E91E8C", "#8E24AA", "#1E5BD8", "#43A047"]
W, H = 1080, 1350

def leque(size=420, start=-200, span=200, gap=3):
    """Leque/roda de cores da logo: gomos com respiro branco."""
    r = size / 2; cx = cy = r; n = len(LEQUE); step = span / n; out = []
    for i, cor in enumerate(LEQUE):
        a0 = math.radians(start + i * step + gap / 2); a1 = math.radians(start + (i + 1) * step - gap / 2)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        out.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z" fill="{cor}"/>')
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">{"".join(out)}</svg>'

def estrela(s=40, cor=GOLD):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 40 40"><path d="M20 0 C22 14 26 18 40 20 C26 22 22 26 20 40 '
            f'C18 26 14 22 0 20 C14 18 18 14 20 0Z" fill="{cor}"/></svg>')

def luzinhas(w=700, y=60):
    pts = []; n = 9
    for i in range(n):
        x = 20 + i * (w - 40) / (n - 1); yy = y + 38 * math.sin(math.pi * i / (n - 1))
        pts.append((x, yy))
    fio = " ".join(f"{x:.0f},{yy:.0f}" for x, yy in pts)
    bulbos = "".join(f'<circle cx="{x:.0f}" cy="{yy+16:.0f}" r="9" fill="#FFE7A3"/><circle cx="{x:.0f}" cy="{yy+16:.0f}" r="22" fill="#FFE7A3" opacity=".25"/>' for x, yy in pts)
    return f'<svg width="{w}" height="{y+90}" viewBox="0 0 {w} {y+90}"><polyline points="{fio}" fill="none" stroke="#3a4a7a" stroke-width="3"/>{bulbos}</svg>'

ICONES = {
 "rolo": '<path d="M10 14h34v12H10z M44 20h6v14H27v8" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/><rect x="23" y="42" width="8" height="14" rx="2" fill="#fff"/>',
 "pano": '<path d="M14 40c6-14 22-24 36-22M14 50c10-8 22-12 36-10" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/><circle cx="46" cy="16" r="5" fill="#fff"/>',
 "escudo": '<path d="M32 8l20 8v14c0 12-9 21-20 26C21 51 12 42 12 30V16z" fill="none" stroke="#fff" stroke-width="4"/><path d="M23 31l7 7 12-14" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>',
 "alerta": '<circle cx="32" cy="32" r="22" fill="none" stroke="#fff" stroke-width="4"/><path d="M32 20v15" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="32" cy="43" r="3" fill="#fff"/>',
 "zap": '<path d="M32 10a22 22 0 0 0-19 33l-3 11 11-3a22 22 0 1 0 11-41z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/><path d="M25 24c0 9 6 15 15 16l3-4-5-3-3 2c-3-1-5-4-6-6l2-3-3-5z" fill="#fff"/>',
 "salvar": '<path d="M18 10h28v44L32 44 18 54z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>',
}
def icone(nome, bg=NAVY):
    return f'<div class="ic" style="background:{bg}"><svg width="64" height="64" viewBox="0 0 64 64">{ICONES[nome]}</svg></div>'


FILTROS = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="pinc" filterUnits="userSpaceOnUse" x="-2000" y="-2000" width="6000" height="6000" color-interpolation-filters="sRGB">
 <feTurbulence type="fractalNoise" baseFrequency="0.02 0.12" numOctaves="3" seed="7" result="n1"/>
 <feDisplacementMap in="SourceGraphic" in2="n1" scale="24" xChannelSelector="R" yChannelSelector="G" result="d"/>
 <feTurbulence type="fractalNoise" baseFrequency="0.0025 0.42" numOctaves="2" seed="3" result="cerdas"/>
 <feColorMatrix in="cerdas" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 2.15" result="falhas"/>
 <feComposite in="d" in2="falhas" operator="in" result="tinta"/>
 <feGaussianBlur in="tinta" stdDeviation="1.6" result="alt"/>
 <feSpecularLighting in="alt" surfaceScale="6" specularConstant="1.1" specularExponent="28" lighting-color="#ffffff" result="spec"><feDistantLight azimuth="250" elevation="40"/></feSpecularLighting>
 <feComposite in="spec" in2="tinta" operator="in" result="spec2"/>
 <feComposite in="tinta" in2="spec2" operator="arithmetic" k1="0" k2="1" k3=".7" k4="0" result="final"/>
 <feDropShadow in="final" dx="0" dy="10" stdDeviation="8" flood-color="#000" flood-opacity=".4"/>
</filter>
<filter id="reboco" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="2" result="g"/>
 <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .22 -.04"/>
</filter>
<filter id="madeira" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency="0.004 0.18" numOctaves="3" seed="5" result="m"/>
 <feColorMatrix in="m" type="matrix" values="0 0 0 0 .45  0 0 0 0 .28  0 0 0 0 .15  0 0 0 .55 0"/>
</filter>
<filter id="borra"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="borra2"><feGaussianBlur stdDeviation="5"/></filter>
</defs></svg>"""

def pinceladas(cx, cy, raio, ang0, ang1, larg=70, escala=1.0):
    """Leque de pinceladas realistas saindo de (cx, cy), nas cores do leque da logo."""
    n = len(LEQUE); out = []
    for i, cor in enumerate(LEQUE):
        a = ang0 + (ang1 - ang0) * i / (n - 1)
        comp = raio * (0.82 + 0.18 * ((i * 37) % 7) / 6)
        curva = 30 if i % 2 else -30
        out.append(f'<g transform="rotate({a:.1f} {cx} {cy})"><path filter="url(#pinc)" d="M{cx+60} {cy} C {cx+comp*.35} {cy+curva}, {cx+comp*.7} {cy-curva}, {cx+comp} {cy}" '
                   f'stroke="{cor}" stroke-width="{larg}" stroke-linecap="round" fill="none"/></g>')
    return f'<svg class="abs" style="left:0;top:0" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(out)}</svg>'

def parede(brilho, cor="#D9A27E"):
    """Ambiente realista: parede com reboco, luz de janela com reflexo conforme o acabamento, rodapé e piso."""
    w, h = 420, 520
    refl = {0: (0.10, 26), 1: (0.38, 12), 2: (0.85, 3)}[brilho]   # (intensidade, desfoque do reflexo)
    janela = (f'<g opacity="{refl[0]}"><g filter="url(#borra{"2" if brilho==2 else ""})" style="filter:blur({refl[1]}px)">'
              f'<path d="M150 70 L300 40 L300 260 L150 300Z" fill="#ffffff"/>'
              f'<path d="M222 55 L228 54 L228 280 L222 282Z M150 180 L300 152 L300 158 L150 186Z" fill="{cor}"/></g></g>')
    luz_ambiente = f'<radialGradient id="la{brilho}" cx="35%" cy="25%" r="80%"><stop offset="0" stop-color="#fff" stop-opacity=".30"/><stop offset="1" stop-color="#3a1a00" stop-opacity=".22"/></radialGradient>'
    return f"""<div class="ambiente"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>{luz_ambiente}<linearGradient id="piso{brilho}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b98a5e"/><stop offset="1" stop-color="#7a5434"/></linearGradient></defs>
<rect width="{w}" height="{h-110}" fill="{cor}"/>
<rect width="{w}" height="{h-110}" filter="url(#reboco)"/>
{janela}
<rect width="{w}" height="{h-110}" fill="url(#la{brilho})"/>
<rect y="{h-110}" width="{w}" height="110" fill="url(#piso{brilho})"/>
<rect y="{h-110}" width="{w}" height="110" filter="url(#madeira)"/>
{"".join(f'<line x1="{x}" y1="{h-110}" x2="{x-60}" y2="{h}" stroke="#5c3d24" stroke-width="2" opacity=".5"/>' for x in range(-40, w+120, 85))}
<rect y="{h-140}" width="{w}" height="34" fill="#f4f2ec"/><rect y="{h-108}" width="{w}" height="5" fill="#000" opacity=".18"/>
<rect y="{h-142}" width="{w}" height="3" fill="#fff"/>
</svg></div>"""

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;font-family:'Montserrat',Arial,sans-serif;background:{OFF};color:{NAVY}}}
.r{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{OFF}}}
.onda{{position:absolute;left:0;right:0;bottom:0}}
.tag{{display:inline-block;background:{NAVY};color:#fff;font-weight:800;font-size:28px;letter-spacing:3px;padding:14px 26px;border-radius:40px}}
.tag.ouro{{background:{GOLD};color:{NAVY}}}
h1{{font-weight:900;font-size:112px;line-height:1.0;letter-spacing:-2px}}
h2{{font-weight:900;font-size:120px;line-height:1;letter-spacing:-2px}}
p{{font-weight:600;font-size:42px;line-height:1.3}}
.ic{{width:96px;height:96px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none}}
.card{{display:flex;gap:28px;align-items:center;background:#fff;border-radius:32px;padding:30px 36px;box-shadow:0 18px 40px rgba(10,36,120,.14)}}
.card b{{font-size:40px;font-weight:800;line-height:1.2}}
.rod{{position:absolute;left:0;right:0;bottom:0;height:96px;background:{NAVY2};color:#fff;display:flex;align-items:center;justify-content:center;gap:18px;font-weight:700;font-size:32px;letter-spacing:1px}}
.ambiente{{width:420px;height:520px;border-radius:210px 210px 30px 30px;overflow:hidden;box-shadow:0 30px 60px rgba(10,36,120,.35);border:12px solid #fff}}
.tinta{{position:absolute;inset:0}}
.rodape-p{{position:absolute;left:0;right:0;bottom:0;height:46px;background:#f2f0ea;border-top:4px solid #e2ded3}}
.abs{{position:absolute}}
"""
FONTE = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">'
ONDA = f'<svg class="onda" width="{W}" height="520" viewBox="0 0 1080 520" preserveAspectRatio="none"><path d="M0 150 C260 30 560 240 1080 80 L1080 520 L0 520Z" fill="{NAVY}"/></svg>'
ROD = f'<div class="rod">{leque(40,-200,200,4)}<span>CooperTintas</span></div>'

def pagina(corpo): return f'<!doctype html><html><head><meta charset="utf-8">{FONTE}<style>{CSS}</style></head><body>{FILTROS}<div class="r">{corpo}</div></body></html>'

slides = []
# 1 capa
slides.append(pagina(f"""
<div class="abs" style="left:0;top:0;right:0;bottom:0;background:{NAVY}"></div>
{pinceladas(1130, 1300, 640, -172, -98, 74)}
<div class="abs" style="left:300px;top:-10px">{luzinhas(760,40)}</div>
<div class="abs" style="left:80px;top:150px;width:520px;height:150px;border:3px dashed rgba(255,255,255,.35);border-radius:20px;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,.5);font-weight:700;font-size:26px;letter-spacing:2px">LOGO COOPERTINTAS</div>
<div class="abs" style="left:80px;top:360px;width:900px">
  <span class="tag ouro">CASA PRONTA PARA O NATAL</span>
  <h1 style="color:#fff;margin-top:40px;font-size:100px">Fosco, acetinado ou semibrilho?</h1>
  <p style="color:#dfe6ff;margin-top:30px;font-size:44px">Qual acabamento usar<br>em cada cômodo</p>
  <p style="color:{GOLD};margin-top:46px;font-weight:800;font-size:46px">arraste →</p>
</div>
<div class="abs" style="left:900px;top:250px">{estrela(56)}</div><div class="abs" style="left:640px;top:330px">{estrela(30)}</div>
<div class="abs" style="left:560px;top:1060px">{estrela(36)}</div>
{ROD}"""))

def slide_acab(num, nome, texto, destaque, icone_nome, brilho, usos, alerta=False):
    cor_card = "#fff" if not alerta else "#FFF1F0"
    return pagina(f"""
{ONDA}
<div class="abs" style="left:420px;top:-10px">{luzinhas(680,30)}</div>
{pinceladas(-80, 200, 360, -10, 10, 34)}
<div class="abs" style="left:80px;top:300px;width:920px">
  <div style="font-weight:800;font-size:30px;letter-spacing:3px;color:#5a6aa0">ACABAMENTO {num}/3</div>
  <h2 style="margin-top:14px;font-size:100px">{nome}</h2>
</div>
<div class="abs" style="left:80px;top:470px;width:470px"><p style="color:#22306a;font-size:40px">{texto}</p></div>
<div class="abs" style="left:630px;top:430px">{parede(brilho)}</div>
<div class="abs" style="left:80px;right:80px;top:1080px">
  <div style="color:#c9d3ff;font-weight:800;font-size:26px;letter-spacing:3px;margin-bottom:16px">ONDE USAR</div>
  <div style="display:flex;flex-wrap:wrap;gap:14px">{"".join(f'<span style="border:2px solid rgba(255,255,255,.5);color:#fff;border-radius:40px;padding:10px 24px;font-weight:700;font-size:30px">{u}</span>' for u in usos)}</div>
</div>
<div class="abs" style="left:80px;right:80px;top:900px"><div class="card" style="background:{cor_card}">{icone(icone_nome, "#E53935" if alerta else NAVY)}<b>{destaque}</b></div></div>
<div class="abs" style="left:960px;top:150px">{estrela(44)}</div>
{ROD}""")

slides.append(slide_acab(1, "Fosco", "Disfarça as imperfeições da parede. Ideal para tetos, salas e quartos.", "Limpeza mais delicada", "pano", 0, ["Tetos", "Salas", "Quartos"]))
slides.append(slide_acab(2, "Acetinado", "Brilho suave e mais fácil de limpar. Bom para salas, quartos e corredores.", "Equilíbrio entre beleza e resistência", "escudo", 1, ["Salas", "Quartos", "Corredores"]))
slides.append(slide_acab(3, "Semibrilho", "O mais resistente à limpeza. Indicado para cozinhas, banheiros, portas e áreas externas.", "Atenção: realça as imperfeições da parede", "alerta", 2, ["Cozinhas", "Banheiros", "Portas", "Áreas externas"], alerta=True))
# 5 fechamento
slides.append(pagina(f"""
<div class="abs" style="left:0;top:0;right:0;bottom:0;background:{NAVY}"></div>
{pinceladas(-60, -60, 560, 8, 72, 66)}
<div class="abs" style="left:80px;top:520px;width:920px">
  <span class="tag ouro">FICOU EM DÚVIDA?</span>
  <h1 style="color:#fff;margin-top:36px;font-size:104px">A gente indica o acabamento certo</h1>
  <p style="color:#dfe6ff;margin-top:28px">Chama no WhatsApp ou passa na loja.</p>
</div>
<div class="abs" style="left:80px;right:80px;top:1080px"><div class="card">{icone("salvar")}<b>Salve este post para a próxima pintura</b></div></div>
<div class="abs" style="left:920px;top:420px">{estrela(56)}</div><div class="abs" style="left:940px;top:1240px">{estrela(30)}</div>
{ROD}"""))

for i, html in enumerate(slides, 1):
    pathlib.Path(f"cooper-acabamentos-{i}.html").write_text(html, encoding="utf-8")
print(len(slides), "slides")
