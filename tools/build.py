#!/usr/bin/env python3
"""Generador del sitio SéVida™ (sevidapsicosocial.com).

Escribe HTML estático en public/. El sitio publicado no tiene paso de compilación:
este script solo se usa para regenerar las páginas cuando cambia el contenido.

    python3 tools/build.py

Para cambiar textos: edite este archivo (sección CONTENIDO) y vuelva a ejecutarlo.
"""
import json, os, re, html, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PUB = RAIZ / "public"
DATOS = RAIZ / "tools" / "datos"
DOMINIO = "https://sevidapsicosocial.com"
HOY = datetime.date.today().isoformat()

# ---------------------------------------------------------------- Configuración
CORREO_SEVIDA = "contacto@sevidapsicosocial.com"   # buzón definitivo: cuando exista, use CORREO = CORREO_SEVIDA
CORREO = "josedavidalomia@gmail.com"   # temporal mientras se compra el dominio
WHATSAPP = "573168768220"
TELEFONO = "+57 315 053 0457"
LINKEDIN = "https://www.linkedin.com/in/vitalisempresarial"   # renombrar a SéVida (checklist 3.4)
INSTAGRAM = "https://www.instagram.com/vitalisempresarial/"   # renombrar a SéVida (checklist 3.4)
CIUDAD = "Cali, Valle del Cauca"

e = html.escape
PAGINAS = []   # (ruta, prioridad) para el sitemap

MENU = [
    ("Servicios", [
        ("Todos los servicios", "/servicios/"),
        ("Diagnóstico SéVida · Batería", "/servicios/bateria-riesgo-psicosocial/"),
        ("Análisis de puesto (APT)", "/servicios/analisis-puesto-trabajo/"),
        ("Recalibra Empresarial", "/servicios/recalibra-empresarial/"),
        ("Vigilancia epidemiológica (PVE)", "/servicios/vigilancia-epidemiologica/"),
        ("Acompañamiento SST Mensual", "/servicios/acompanamiento-sst/"),
        ("Talleres", "/servicios/talleres/"),
        ("Coaching de líderes", "/servicios/coaching-lideres/"),
    ]),
    ("Método", "/metodo/"),
    ("Recursos", [("Normativa", "/normativa/"), ("Blog", "/blog/")]),
    ("Nosotros", "/nosotros/"),
    ("Índice ISMO", "/ismo/"),
]


def nav(actual):
    h = []
    for nombre, destino in MENU:
        if isinstance(destino, list):
            activo = any(actual.startswith(d) for _, d in destino if d != "/servicios/") or (actual.startswith("/servicios/") and nombre == "Servicios")
            items = "".join(f'<li><a href="{d}"{" aria-current=\"page\"" if d == actual else ""}>{e(n)}</a></li>' for n, d in destino)
            h.append(f'<li><button type="button" aria-haspopup="true" aria-expanded="false"{" class=\"activo\"" if activo else ""}>{e(nombre)}</button><ul class="submenu">{items}</ul></li>')
        else:
            cur = ' aria-current="page"' if actual == destino or (destino != "/" and actual.startswith(destino)) else ""
            h.append(f'<li><a href="{destino}"{cur}>{e(nombre)}</a></li>')
    h.append('<li><a class="btn btn-primario" href="/contacto/">Conversación diagnóstica</a></li>')
    return "".join(h)


def migas(items):
    if not items:
        return ""
    li = ['<li><a href="/">Inicio</a></li>'] + [
        (f'<li><a href="{u}">{e(n)}</a></li>' if u else f'<li aria-current="page">{e(n)}</li>') for n, u in items]
    return f'<nav class="migas" aria-label="Migas de pan"><ol>{"".join(li)}</ol></nav>'


def jsonld_migas(ruta, items):
    lista = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": DOMINIO + "/"}]
    for i, (n, u) in enumerate(items, 2):
        lista.append({"@type": "ListItem", "position": i, "name": n, "item": DOMINIO + (u or ruta)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lista}


ORG = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "name": "SéVida | Riesgo Psicosocial",
    "url": DOMINIO + "/", "logo": DOMINIO + "/assets/img/sevida-logo-principal.svg", "image": DOMINIO + "/assets/img/og-sevida.png",
    "description": "Consultoría en riesgo psicosocial, seguridad y salud en el trabajo y salud organizacional para empresas colombianas.",
    "address": {"@type": "PostalAddress", "addressLocality": "Cali", "addressRegion": "Valle del Cauca", "addressCountry": "CO"},
    "areaServed": "CO", "telephone": TELEFONO, "email": CORREO,
    "founder": {"@type": "Person", "name": "Jose David Alomía Gutiérrez", "jobTitle": "Psicólogo especialista en Gerencia de la Seguridad y Salud en el Trabajo"},
}


def pagina(ruta, titulo, descripcion, cuerpo, *, cabecera=None, kicker=None, lead=None, ruta_migas=None,
           scripts=(), jsonld=(), prioridad="0.7", tipo="website", indexar=True, titulo_corto=None):
    """Escribe public/<ruta>/index.html con la plantilla común."""
    canon = DOMINIO + ruta
    titulo_doc = titulo if titulo.endswith("SéVida") or ruta == "/" else f"{titulo} | SéVida"
    bloques_ld = [ORG] if ruta == "/" else []
    if ruta_migas:
        bloques_ld.append(jsonld_migas(ruta, ruta_migas))
    bloques_ld += list(jsonld)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in bloques_ld)
    cab = ""
    if cabecera is not False and ruta != "/":
        cab = (f'<header class="cabecera-pagina"><div class="contenedor">{migas(ruta_migas)}'
               f'{f"<span class=\"kicker\">{e(kicker)}</span>" if kicker else ""}<h1>{cabecera or e(titulo_corto or titulo)}</h1>'
               f'{f"<p class=\"lead\">{lead}</p>" if lead else ""}</div></header>')
    js = "".join(f'<script src="/assets/js/{s}" defer></script>' for s in ("site.js",) + tuple(scripts))
    doc = f"""<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo_doc)}</title>
<meta name="description" content="{e(descripcion)}">
<link rel="canonical" href="{canon}">
{'' if indexar else '<meta name="robots" content="noindex">'}
<meta property="og:type" content="{tipo}">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="SéVida | Riesgo Psicosocial">
<meta property="og:title" content="{e(titulo_doc)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMINIO}/assets/img/og-sevida.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0D1B2A">
<link rel="icon" type="image/svg+xml" href="/assets/img/sevida-isotipo.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/sevida.css">
{ld}
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="cabecera"><div class="contenedor">
<a class="marca" href="/" aria-label="SéVida, inicio"><img src="/assets/img/sevida-logo-principal.svg" alt="SéVida | Riesgo Psicosocial" width="130" height="46"></a>
<button class="hamburguesa" type="button" aria-label="Abrir menú" aria-controls="menu" aria-expanded="false"><span></span><span></span><span></span></button>
<nav aria-label="Principal"><ul class="menu" id="menu">{nav(ruta)}</ul></nav>
</div></header>
<main id="contenido">
{cab}
{cuerpo}
</main>
{PIE}
<a class="whatsapp" href="https://wa.me/{WHATSAPP}?text=Hola%2C%20quiero%20informaci%C3%B3n%20sobre%20S%C3%A9Vida" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">WhatsApp</a>
{js}
</body>
</html>
"""
    destino = PUB / ruta.strip("/") / "index.html" if ruta != "/" else PUB / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(doc, encoding="utf-8")
    if indexar:
        PAGINAS.append((ruta, prioridad))


PIE = f"""<footer class="pie"><div class="contenedor">
<div class="rejilla">
<div><img class="logo-pie" src="/assets/img/sevida-logo-principal-negativo.svg" alt="SéVida | Riesgo Psicosocial" width="147" height="52">
<p>Consultoría en riesgo psicosocial, seguridad y salud en el trabajo y salud organizacional para empresas colombianas.</p>
<p style="margin-top:10px">Dirección técnica: Jose David Alomía Gutiérrez, psicólogo especialista en Gerencia de la Seguridad y Salud en el Trabajo, con licencia en SST vigente.</p></div>
<div><h4>Servicios</h4><ul>
<li><a href="/servicios/bateria-riesgo-psicosocial/">Diagnóstico SéVida</a></li><li><a href="/servicios/analisis-puesto-trabajo/">Análisis de puesto</a></li><li><a href="/servicios/recalibra-empresarial/">Recalibra Empresarial</a></li>
<li><a href="/servicios/vigilancia-epidemiologica/">Vigilancia epidemiológica</a></li><li><a href="/servicios/acompanamiento-sst/">Acompañamiento SST</a></li>
<li><a href="/servicios/talleres/">Talleres</a></li><li><a href="/servicios/coaching-lideres/">Coaching de líderes</a></li></ul></div>
<div><h4>SéVida</h4><ul><li><a href="/metodo/">Método S·É·V·I·D·A</a></li><li><a href="/nosotros/">Nosotros</a></li>
<li><a href="/normativa/">Normativa</a></li><li><a href="/blog/">Blog</a></li><li><a href="/ismo/">Índice ISMO</a></li></ul></div>
<div><h4>Contacto</h4><ul><li><a href="https://wa.me/{WHATSAPP}">WhatsApp +57 316 876 8220</a></li><li><a href="tel:{TELEFONO.replace(' ', '')}">{TELEFONO}</a></li>
<li><a href="mailto:{CORREO}">{CORREO}</a></li><li>{CIUDAD}, Colombia</li>
<li><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a> · <a href="{INSTAGRAM}" rel="noopener" target="_blank">Instagram</a></li></ul></div>
</div>
<div class="pie-legal"><span>© <span id="anio">2026</span> SéVida | Riesgo Psicosocial. SéVida™, Método S·É·V·I·D·A™, RECALIBRA™ e ISMO son marcas en trámite ante la Superintendencia de Industria y Comercio.</span>
<a href="/politica-de-datos/">Política de tratamiento de datos</a></div>
</div></footer>"""


def cta(titulo="Empecemos por entender su caso", texto="Una conversación diagnóstica de 30 minutos, sin costo: revisamos su situación y le decimos qué falta y en qué orden resolverlo.", boton="Agendar la conversación"):
    return (f'<section class="seccion"><div class="contenedor"><div class="cta"><div><h2>{titulo}</h2><p>{texto}</p></div>'
            f'<a class="btn btn-claro" href="/contacto/">{boton}</a></div></div></section>')


def tarjeta(titulo, texto, enlace=None, etiqueta=None, codigo=None, destacada=False):
    return (f'<article class="tarjeta{" tarjeta-destacada" if destacada else ""}">'
            f'{f"<span class=\"codigo\">{codigo}</span>" if codigo else ""}<h3>{titulo}</h3><p>{texto}</p>'
            f'{f"<a class=\"enlace\" href=\"{enlace}\">{etiqueta or "Ver más"} →</a>" if enlace else ""}</article>')


def lista(items):
    return '<ul class="lista-check">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def tabla(cabeceras, filas):
    th = "".join(f"<th scope=\"col\">{c}</th>" for c in cabeceras)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    return f'<div class="tabla-envoltura"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def seccion(contenido, clase="", kicker=None, titulo=None, lead=None, centro=False):
    cab = ""
    if kicker or titulo or lead:
        cab = (f'<div class="{"centro" if centro else ""}" style="margin-bottom:36px">'
               f'{f"<span class=\"kicker\">{kicker}</span>" if kicker else ""}{f"<h2>{titulo}</h2>" if titulo else ""}'
               f'{f"<p class=\"lead\">{lead}</p>" if lead else ""}</div>')
    return f'<section class="seccion {clase}"><div class="contenedor">{cab}{contenido}</div></section>'


def servicio_ld(nombre, desc, ruta):
    return {"@context": "https://schema.org", "@type": "Service", "name": nombre, "description": desc,
            "provider": {"@type": "ProfessionalService", "name": "SéVida | Riesgo Psicosocial", "url": DOMINIO + "/"},
            "areaServed": "CO", "url": DOMINIO + ruta}


# ================================================================ CONTENIDO

FUENTE_AUSENTISMO = ('<a href="https://www.andi.com.co/Home/Noticia/17758-en-el-encuentro-nacional-de-seguridad-y" rel="noopener" target="_blank">'
                     'CESLA-ANDI, Encuesta de Ausentismo Laboral e Incapacidades, datos de 2023 (134 empresas), presentada en noviembre de 2024</a>')


def inicio():
    c = f"""
<section class="hero"><div class="contenedor">
<span class="lema">Medir. Intervenir. Recalibrar.</span>
<h1>El riesgo psicosocial se puede medir, intervenir y demostrar.</h1>
<p class="lead">Ayudamos a empresas colombianas a cumplir la norma y a convertir esa obligación en decisiones de gestión: menos rotación, menos ausentismo y equipos que funcionan mejor.</p>
<div class="acciones"><a class="btn btn-claro" href="/contacto/">Conversación diagnóstica de 30 minutos</a>
<a class="btn btn-secundario" href="/ismo/">Hacer el Índice ISMO gratis</a></div>
</div></section>

<section class="seccion"><div class="contenedor rejilla r2" style="align-items:center">
<div><span class="kicker">El problema que nadie mide</span>
<h2>El riesgo psicosocial no aparece en el balance, pero sí en los resultados.</h2>
<p class="lead">Rotación, incapacidades, conflictos y baja productividad suelen tener un origen común en las condiciones de trabajo. La mayoría de empresas paga ese costo sin haberlo medido.</p></div>
<div class="rejilla r2">
<div class="tarjeta"><span class="numero">9,4</span><p style="margin-top:10px">días de ausencia por trabajador al año; 5,3 de ellos por enfermedad general.</p><p class="nota" style="margin-top:8px">Fuente: {FUENTE_AUSENTISMO}.</p></div>
<div class="tarjeta"><span class="numero">500</span><p style="margin-top:10px">salarios mínimos mensuales es la multa máxima por incumplir las normas de seguridad y salud en el trabajo.</p><p class="nota" style="margin-top:8px">Fuente: Ley 1562 de 2012, artículo 13.</p></div>
</div></div></section>

{seccion('<div class="rejilla r3">' +
    tarjeta("Diagnóstico SéVida", "Aplicación de la Batería de Riesgo Psicosocial en físico, informe técnico firmado, presentación a la dirección y hoja de ruta priorizada.", "/servicios/bateria-riesgo-psicosocial/", "Ver el diagnóstico", "NIVEL 1") +
    tarjeta("Recalibra Empresarial", "Intervención de 3 meses en 6 módulos sobre los factores que salieron en el diagnóstico, con medición antes y después.", "/servicios/recalibra-empresarial/", "Ver el programa", "NIVEL 2", True) +
    tarjeta("Programa Integral SéVida", "De 6 a 12 meses: diagnóstico, intervención, vigilancia epidemiológica, formación de líderes y documentación completa.", "/servicios/", "Ver todos los servicios", "NIVEL 3") +
    '</div>', "seccion-gris", "Servicios", "Una ruta para cada momento de su organización",
    "Empezamos por medir. Después intervenimos donde los datos lo indican y hacemos seguimiento hasta que el cambio se sostenga.")}

{seccion('<ol class="fases">' + "".join(f'<li><span class="letra">{l}</span><strong>{n}</strong><p>{d}</p></li>' for l, n, d in FASES) + '</ol><p style="margin-top:26px"><a class="btn btn-secundario" href="/metodo/">Conocer el método</a></p>',
    "", "Método S·É·V·I·D·A™", "Seis fases, un mismo sistema", "Cada servicio de SéVida se ubica en una o varias de estas fases. Así se sabe siempre en qué punto está la organización y qué sigue.")}

<section class="seccion seccion-oscura"><div class="contenedor rejilla r2" style="align-items:center">
<div><span class="kicker">Criterio de contratación</span><h2>Pregunte a su proveedor bajo qué resolución aplica la batería.</h2>
<p class="lead">Es la pregunta más rápida y la más reveladora. La Resolución 2764 de 2022 derogó la Resolución 2404 de 2019, no la 2646 de 2008, que sigue vigente. Un proveedor que no distinga esto puede estar trabajando con instrumentos desactualizados.</p>
<p style="margin-top:22px"><a class="btn btn-claro" href="/normativa/">Ver el marco normativo</a></p></div>
<div class="rejilla r2">
<div class="tarjeta"><span class="codigo">VIGENTE</span><h3>Res. 2764 de 2022</h3><p>Batería oficial de instrumentos.</p></div>
<div class="tarjeta"><span class="codigo">VIGENTE</span><h3>Res. 2646 de 2008</h3><p>Marco de identificación, evaluación e intervención.</p></div>
<div class="tarjeta"><span class="codigo">VIGENTE</span><h3>Res. 0312 de 2019</h3><p>Estándares mínimos: 7, 21 o 60 según la empresa.</p></div>
<div class="tarjeta"><span class="codigo">VIGENTE</span><h3>Res. 3461 de 2025</h3><p>Comité de Convivencia Laboral.</p></div>
</div></div></section>

{seccion('<div class="rejilla r2" style="align-items:center"><div><p class="lead">Ocho dimensiones, diez minutos y un resultado con recomendaciones concretas. Sirve para dimensionar la situación y para sustentar el presupuesto ante la dirección.</p>' +
    '<p style="margin-top:22px"><a class="btn btn-primario" href="/ismo/">Hacer el diagnóstico ISMO</a></p></div>' +
    '<div class="tarjeta"><span class="codigo">ISMO</span><h3>Índice SéVida de Madurez Organizacional</h3>' + lista(["Indicadores de negocio y de SST", "Factores de riesgo psicosocial y salud mental", "Liderazgo, cultura y bienestar", "Cumplimiento legal"]) + '</div></div>',
    "seccion-gris", "Herramienta gratuita", "¿En qué punto está su organización?")}

{seccion(BLOG_RESUMEN(), "", "Blog", "Contenido técnico para decidir mejor", None)}
{cta()}
"""
    pagina("/", "SéVida | Riesgo Psicosocial — Consultoría en riesgo psicosocial y SST en Colombia",
           "Diagnóstico, intervención y vigilancia del riesgo psicosocial y acompañamiento SST para empresas colombianas. Batería oficial aplicada en físico, informes firmados y resultados medibles.",
           c, prioridad="1.0")


FASES = [
    ("S", "Sensibilizar", "La dirección y los equipos entienden qué es el riesgo psicosocial y por qué se mide."),
    ("É", "Evaluar", "Aplicamos la batería oficial y recogemos los indicadores de la organización."),
    ("V", "Valorar", "Interpretamos los resultados por área y cargo, y priorizamos qué intervenir."),
    ("I", "Intervenir", "Actuamos sobre las condiciones de trabajo, los líderes y las personas."),
    ("D", "Dar seguimiento", "Vigilancia epidemiológica con indicadores y casos en seguimiento."),
    ("A", "Asegurar", "Documentación completa y mejora continua para sostener el cambio."),
]


def servicios():
    filas = [
        ["<strong>Diagnóstico SéVida</strong>", "Medir y priorizar", "Batería completa en físico, informe técnico, presentación a la dirección, hoja de ruta", "S · É · V"],
        ["<strong>Recalibra Empresarial</strong>", "Intervenir lo que salió en el diagnóstico", "3 meses, 6 módulos, medición antes y después, informe de impacto", "I · D"],
        ["<strong>Programa Integral SéVida</strong>", "Transformar y sostener", "6 a 12 meses: todo lo anterior, PVE, formación de líderes, documentación completa", "S a A"],
    ]
    comp = [
        ["Especialización", "Exclusiva en riesgo psicosocial y salud organizacional", "Una línea dentro de un portafolio amplio", "Depende del perfil del responsable de SST"],
        ["Firma del informe", "Psicólogo con licencia en SST y tarjeta profesional vigentes", "Variable; con frecuencia subcontratada", "Requiere psicólogo con licencia en nómina"],
        ["Instrumentos", "Intralaboral (formas A y B), extralaboral, estrés y estilos de afrontamiento", "Alcance variable según cotización", "Requiere el instrumento completo"],
        ["Entregable", "Informe, presentación a la dirección, hoja de ruta y PVE", "Con frecuencia termina en el informe", "Sujeto a la carga del área"],
        ["Lectura de resultados", "En lenguaje de gestión: rotación, ausentismo, exposición legal", "Reporte técnico sin traducción a negocio", "Riesgo de sesgo: el área mide su propia gestión"],
        ["Objetividad", "Tercero independiente", "Tercero independiente", "El evaluador reporta a la organización evaluada"],
    ]
    c = seccion(tabla(["Producto", "Para qué", "Qué incluye", "Fases S·É·V·I·D·A"], filas) +
                '<p class="nota">Cotización según el tamaño y las necesidades de la organización, después de la conversación diagnóstica.</p>',
                "", "Ruta principal", "Tres productos que se encadenan", "Cada nivel se apoya en el anterior. Se puede empezar por el diagnóstico y avanzar cuando los resultados lo justifiquen.")
    c += seccion('<div class="rejilla r3">' +
                 tarjeta("Esencial", "Seguimiento mensual de indicadores y del plan de intervención.", codigo="CONTINUIDAD") +
                 tarjeta("Evolución", "Seguimiento, actividades de intervención y acompañamiento al PVE.", codigo="CONTINUIDAD") +
                 tarjeta("Trascendencia", "Acompañamiento estratégico con la dirección y formación continua de líderes.", codigo="CONTINUIDAD") +
                 '</div>', "seccion-gris", "Después del proyecto", "Planes de continuidad mensual", "Se ofrecen cuando termina el diagnóstico o la intervención, para sostener los resultados.")
    c += seccion('<div class="rejilla r3">' +
                 tarjeta("Batería de Riesgo Psicosocial", "Aplicación de la batería oficial en físico, con informe técnico y hoja de ruta.", "/servicios/bateria-riesgo-psicosocial/") +
                 tarjeta("Análisis de puesto de trabajo", "APT preventivo o para determinación de origen, por cargo o por caso.", "/servicios/analisis-puesto-trabajo/") +
                 tarjeta("Vigilancia epidemiológica", "Programa de vigilancia epidemiológica psicosocial con indicadores y seguimiento.", "/servicios/vigilancia-epidemiologica/") +
                 tarjeta("Acompañamiento SST Mensual", "Su SG-SST gestionado por un especialista, en tres niveles según la Resolución 0312 de 2019.", "/servicios/acompanamiento-sst/") +
                 tarjeta("Talleres", "53 talleres en 6 líneas, de 1 a 2 horas, presenciales o virtuales.", "/servicios/talleres/") +
                 tarjeta("Coaching de líderes", "Sesiones individuales para liderar equipos sin desgastarlos.", "/servicios/coaching-lideres/") +
                 '</div>', "", "Servicios complementarios", "Para necesidades puntuales")
    c += seccion(tabla(["Criterio", "SéVida", "Firma generalista de SST", "Gestión interna"], comp) +
                 '<div class="aviso"><strong>Sobre la gestión interna.</strong> Es viable cuando la organización tiene un psicólogo con licencia en SST y capacidad para sostener la vigilancia epidemiológica. El punto a evaluar es la objetividad: cuando el área que gestiona el clima es la misma que mide el riesgo, el resultado queda expuesto a cuestionamiento en una inspección o en un proceso de determinación de origen.</div>',
                 "seccion-gris", "Criterios de decisión", "Tres formas de resolver la obligación. No entregan lo mismo.")
    c += cta()
    pagina("/servicios/", "Servicios", "Diagnóstico SéVida, Recalibra Empresarial y Programa Integral SéVida, más vigilancia epidemiológica, acompañamiento SST, talleres y coaching de líderes.",
           c, kicker="Servicios", lead="Del diagnóstico obligatorio a la transformación sostenida, con rigor técnico en cada paso.", ruta_migas=[("Servicios", None)], prioridad="0.9")


def recalibra():
    modulos = [("Gestión del estrés", "Identificación de estresores individuales y organizacionales; técnicas de regulación y afrontamiento aplicadas al trabajo."),
               ("Autocuidado activo", "Hábitos y rutinas protectoras sostenibles en la vida cotidiana del trabajador."),
               ("Comunicación asertiva", "Habilidades para reducir conflictos, mejorar el clima y manejar conversaciones difíciles."),
               ("Inteligencia emocional", "Reconocimiento y gestión de emociones bajo presión; empatía en el equipo."),
               ("Trabajo en equipo", "Cohesión, confianza, colaboración y manejo saludable de las diferencias."),
               ("Prevención del agotamiento", "Detección temprana del burnout; factores protectores y medidas organizacionales.")]
    mod = '<div class="rejilla r3">' + "".join(tarjeta(n, d, codigo=f"MÓDULO {i:02d}") for i, (n, d) in enumerate(modulos, 1)) + "</div>"
    c = seccion('<div class="rejilla r2"><div><p class="lead">Recalibra Empresarial no es un taller de motivación. Es una intervención de 3 meses que actúa sobre los factores de riesgo que mostró el diagnóstico. Cada módulo se apoya en el anterior.</p>'
                '<h3 style="margin-top:28px">Para quién</h3><p>Organizaciones que ya identificaron factores de riesgo y necesitan intervenirlos, o que quieren actuar de forma preventiva.</p></div>'
                '<div class="tarjeta tarjeta-destacada"><h3>Qué incluye</h3>' + lista(["6 sesiones grupales facilitadas, hasta 30 personas por sesión", "Guía digital individual por participante", "Evaluación antes y después con indicadores", "Informe de impacto para la dirección", "Duración: 3 meses"]) + '</div></div>',
                "", "Programa de intervención", "Del diagnóstico al cambio")
    c += seccion(mod, "seccion-gris", "Contenido", "Seis módulos progresivos")
    c += seccion('<div class="aviso"><strong>Qué no promete.</strong> Los resultados dependen del diagnóstico inicial, del nivel de riesgo y del compromiso de la organización. Por eso se mide antes y después: el informe de impacto muestra lo que cambió y lo que no.</div>')
    c += cta("¿Ya tiene el diagnóstico?", "Revisemos sus resultados y definamos qué módulos priorizar.")
    pagina("/servicios/recalibra-empresarial/", "Recalibra Empresarial", "Programa de intervención del riesgo psicosocial de 3 meses y 6 módulos, con medición antes y después e informe de impacto para la dirección.",
           c, kicker="Nivel 2 · Intervención", titulo_corto="Recalibra Empresarial", lead="Intervención de 3 meses sobre los factores de riesgo psicosocial que mostró el diagnóstico, con resultados medibles.",
           ruta_migas=[("Servicios", "/servicios/"), ("Recalibra Empresarial", None)], jsonld=[servicio_ld("Recalibra Empresarial", "Programa de intervención del riesgo psicosocial de 3 meses.", "/servicios/recalibra-empresarial/")], prioridad="0.8")


def bateria():
    c = seccion('<div class="rejilla r3">' +
                tarjeta("Forma A", "Para jefes, supervisores, coordinadores y profesionales con personal a cargo.", codigo="INTRALABORAL") +
                tarjeta("Forma B", "Para auxiliares, operarios y cargos sin personal a cargo.", codigo="INTRALABORAL") +
                tarjeta("Condiciones extralaborales", "Entorno familiar, social y económico del trabajador.", codigo="EXTRALABORAL") +
                tarjeta("Cuestionario de estrés", "Síntomas de estrés en el momento de la evaluación.", codigo="ESTRÉS") +
                tarjeta("Estilos de afrontamiento", "Cómo enfrentan las personas las situaciones difíciles. Es el cuestionario que más se omite.", codigo="AFRONTAMIENTO") +
                tarjeta("Ficha de datos generales", "Información sociodemográfica y ocupacional para el análisis por grupos.", codigo="DATOS") +
                '</div><div class="aviso aviso-dorado"><strong>Aplicación en físico.</strong> Los cuestionarios y el consentimiento informado se diligencian en papel, se sellan y se devuelven de inmediato. Así se protege el anonimato de las respuestas. El acompañamiento del especialista puede ser presencial o virtual.</div>',
                "", "Diagnóstico SéVida", "La batería oficial, completa y bien aplicada",
                "La Batería de Instrumentos para la Evaluación de Factores de Riesgo Psicosocial (Ministerio de la Protección Social, 2010, con la Pontificia Universidad Javeriana) es la adoptada por la Resolución 2764 de 2022.")
    c += seccion(lista(["Informe técnico por área y cargo, firmado por psicólogo con licencia en SST", "Presentación de hallazgos a la dirección", "Hoja de ruta de intervención priorizada", "Primeros auxilios psicológicos cuando un caso lo requiere", "Base para el Programa de Vigilancia Epidemiológica"]),
                 "seccion-gris", "Qué entrega", "Lo que recibe la organización")
    c += seccion('<div class="aviso"><strong>¿Necesita un análisis de puesto de trabajo?</strong> El APT preventivo y el APT para determinación de origen son un servicio aparte, que se contrata por cargo o por caso. <a href="/servicios/analisis-puesto-trabajo/">Ver el servicio de APT →</a></div>', "")
    faq = [("¿Cuánto tarda la aplicación?", "Cada trabajador tarda entre 40 y 70 minutos. El informe se entrega entre 2 y 3 semanas después de recoger todos los cuestionarios."),
           ("¿Cada cuánto hay que repetirla?", "Como mínimo cada dos años, y antes si hay cambios importantes en la organización. Si la última aplicación usó instrumentos anteriores a la Resolución 2764 de 2022, hay que actualizarlos sin importar el tiempo transcurrido."),
           ("¿Se puede aplicar en varias sedes?", "Sí. Los cuestionarios se diligencian en físico en cada sede; la coordinación y la entrega de resultados pueden ser virtuales. El informe se puede segmentar por sede, área o cargo."),
           ("¿Las respuestas son confidenciales?", "Sí. Los resultados se reportan siempre por grupos, nunca por persona, y el tratamiento de datos cumple la Ley 1581 de 2012.")]
    c += seccion("".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in faq), "seccion-gris", "Preguntas frecuentes", "Antes de contratar")
    c += cta("Solicite la propuesta de diagnóstico", "Con el número de trabajadores y las sedes le enviamos una propuesta ajustada.")
    pagina("/servicios/bateria-riesgo-psicosocial/", "Batería de Riesgo Psicosocial", "Aplicación de la Batería de Riesgo Psicosocial (Resolución 2764 de 2022) en físico, con informe técnico firmado y hoja de ruta de intervención.",
           c, kicker="Nivel 1 · Diagnóstico SéVida", titulo_corto="Batería de Riesgo Psicosocial", lead="El instrumento oficial, aplicado como lo exige la norma, con un informe que sirve para decidir.",
           ruta_migas=[("Servicios", "/servicios/"), ("Batería de Riesgo Psicosocial", None)], jsonld=[servicio_ld("Diagnóstico SéVida — Batería de Riesgo Psicosocial", "Aplicación de la batería oficial e informe técnico.", "/servicios/bateria-riesgo-psicosocial/")], prioridad="0.9")


def apt():
    c = seccion('<div class="rejilla r2">' +
                tarjeta("APT Preventivo", "Analiza el dominio de demandas del trabajo de un cargo para prevenir la exposición: demandas cuantitativas, cognitivas y emocionales, y recomendaciones de rediseño.", codigo="SV-MD-APT-21") +
                tarjeta("APT para determinación de origen", "Protocolo completo para la calificación de origen ante la ARL, la EPS o las Juntas de Calificación: historia laboral, condiciones del cargo y concepto técnico.", codigo="SV-FT-APT-20 · SV-FT-APT-22") +
                '</div><div class="aviso"><strong>Son dos productos distintos.</strong> Llevan el mismo nombre, pero tienen propósitos, métodos y destinatarios diferentes. Mezclarlos debilita el informe.</div>',
                "", "Dos servicios", "Dos análisis, dos propósitos", "Se contratan por cargo o por caso, con o sin batería.")
    c += seccion('<div class="rejilla r2"><div><h3>APT Preventivo</h3>' + lista(["La batería identifica riesgo alto o muy alto en el dominio de demandas del trabajo en un cargo", "Se crea un cargo nuevo o se rediseña uno existente", "Un área presenta quejas recurrentes de sobrecarga o de ritmo de trabajo", "Entrega: descripción de las demandas del cargo y recomendaciones de rediseño priorizadas"]) +
                 '</div><div><h3>APT para determinación de origen</h3>' + lista(["Un trabajador tiene un diagnóstico en salud mental y debe establecerse si su origen es laboral", "La ARL, la EPS o una Junta de Calificación de Invalidez solicita el análisis del puesto", "La empresa necesita documentar las condiciones reales del cargo para el proceso de calificación", "Entrega: historia laboral, condiciones del cargo y concepto técnico firmado"]) + '</div></div>',
                 "seccion-gris", "Cuándo se necesita", "Cada análisis responde a una situación distinta")
    c += seccion('<div class="rejilla r2"><div><p>El APT no reemplaza la batería ni hace parte de ella. Puede contratarse solo o como complemento cuando la batería señala un cargo crítico.</p><p style="margin-top:14px">Lo firma un psicólogo especialista en Gerencia de la Seguridad y Salud en el Trabajo, con licencia en SST vigente.</p></div>' +
                 tarjeta("Batería de Riesgo Psicosocial", "Aplicación de la batería oficial en físico, con informe técnico y hoja de ruta.", "/servicios/bateria-riesgo-psicosocial/") +
                 '</div><p style="margin-top:22px">Para profundizar: <a href="/blog/analisis-puesto-trabajo-bateria-vs-determinacion-origen/">Análisis de puesto de trabajo: batería psicosocial vs. determinación de origen</a>.</p>',
                 "", "Relación con la batería", "Un servicio aparte, no un anexo")
    faq = [("¿Se puede contratar el APT sin la batería?", "Sí. Es un servicio independiente. Si la organización ya aplicó la batería, sus resultados orientan qué cargos analizar primero."),
           ("¿Qué diferencia hay entre los dos APT?", "El preventivo busca reducir la exposición en un cargo y se entrega a la empresa. El de determinación de origen aporta evidencia técnica para calificar si una enfermedad es laboral y se dirige a la ARL, la EPS o las Juntas de Calificación."),
           ("¿Cómo se hace el análisis?", "Incluye la revisión de la información del cargo, la observación del puesto en el lugar de trabajo y entrevistas con el trabajador y su jefe inmediato."),
           ("¿La información es confidencial?", "Sí. Se trata según la Ley 1581 de 2012 y solo se usa para el propósito del análisis.")]
    c += seccion("".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in faq), "seccion-gris", "Preguntas frecuentes", "Antes de contratar")
    c += cta("Solicite la propuesta de APT", "Indíquenos el cargo, el propósito del análisis y la ciudad.")
    pagina("/servicios/analisis-puesto-trabajo/", "Análisis de puesto de trabajo (APT)", "Análisis de puesto de trabajo (APT) como servicio independiente: APT preventivo del dominio de demandas y APT para determinación de origen ante la ARL, la EPS o las Juntas de Calificación.",
           c, kicker="Servicio independiente", titulo_corto="Análisis de puesto de trabajo", lead="Dos análisis distintos: uno para prevenir la exposición en un cargo y otro para aportar el concepto técnico en la calificación de origen.",
           ruta_migas=[("Servicios", "/servicios/"), ("Análisis de puesto de trabajo", None)], jsonld=[servicio_ld("Análisis de puesto de trabajo (APT)", "APT preventivo y APT para determinación de origen.", "/servicios/analisis-puesto-trabajo/")], prioridad="0.8")


def pve():
    pasos = [("Línea base", "Resultados de la Batería de Riesgo Psicosocial como punto de partida."),
             ("Plan de acción", "Intervenciones priorizadas según nivel de riesgo y área."),
             ("Intervención", "Talleres, seguimiento individual y ajustes en las condiciones de trabajo."),
             ("Seguimiento y medición", "Indicadores de gestión y casos en seguimiento, con revisión periódica."),
             ("Documentación", "Registros técnicos completos y disponibles para cualquier requerimiento.")]
    c = seccion('<div class="rejilla r2"><div><p class="lead">El Programa de Vigilancia Epidemiológica (PVE) psicosocial es el mecanismo para monitorear de forma permanente los factores de riesgo, medir su evolución y decidir a tiempo.</p>'
                '<p style="margin-top:14px">A diferencia de un diagnóstico puntual, es un proceso continuo: evaluación, seguimiento, intervención y medición. Sin él, la batería se queda en un informe.</p></div>'
                '<div class="tarjeta"><h3>Marco normativo</h3><p>Resolución 2646 de 2008 · Resolución 2764 de 2022 · Decreto 1072 de 2015 · Resolución 0312 de 2019 (ítem 3.1.2)</p></div></div>',
                "", "Vigilancia epidemiológica", "Un sistema, no un evento")
    c += seccion('<ol class="pasos">' + "".join(f"<li><strong>{n}</strong>{d}</li>" for n, d in pasos) + "</ol>", "seccion-gris", "Componentes", "Cómo funciona el PVE de SéVida")
    c += cta()
    pagina("/servicios/vigilancia-epidemiologica/", "Programa de Vigilancia Epidemiológica psicosocial", "Programa de Vigilancia Epidemiológica psicosocial con línea base, plan de acción, intervención, indicadores y documentación completa.",
           c, kicker="Seguimiento", titulo_corto="Vigilancia epidemiológica psicosocial", lead="Seguimiento continuo de los factores de riesgo psicosocial, con indicadores y documentación lista.",
           ruta_migas=[("Servicios", "/servicios/"), ("Vigilancia epidemiológica", None)], jsonld=[servicio_ld("Programa de Vigilancia Epidemiológica psicosocial", "PVE psicosocial con indicadores.", "/servicios/vigilancia-epidemiologica/")])


def sst():
    niveles = [
        ("SV-SST-01", "Hasta 10 trabajadores", "Riesgo I, II o III", "7", "art. 3"),
        ("SV-SST-02", "De 11 a 50 trabajadores", "Riesgo I, II o III", "21", "art. 9"),
        ("SV-SST-03", "De 51 a 200 trabajadores", "O cualquier tamaño con riesgo IV o V", "60", "art. 16"),
    ]
    tarjetas = '<div class="rejilla r3">' + "".join(
        f'<article class="tarjeta"><span class="codigo">{cod}</span><h3>{rango}</h3><p>{riesgo}</p>'
        f'<p style="margin-top:14px"><span class="nivel-cifra">{n}</span> estándares mínimos ({art})</p></article>' for cod, rango, riesgo, n, art in niveles) + "</div>"
    c = seccion(tarjetas + '<p class="nota" style="margin-top:18px">¿Más de 200 trabajadores? Cotizamos el acompañamiento a la medida.</p>',
                "", "Tres niveles", "Tres niveles, según su empresa",
                "El nivel lo define la Resolución 0312 de 2019 según el número de trabajadores y la clase de riesgo: cada empresa paga por los estándares que de verdad le exigen.")
    incluye = [("Autoevaluación de estándares mínimos", "Calificación según la tabla de valores del artículo 27 y plan de mejoramiento (art. 29)."),
               ("Plan anual de trabajo", "Objetivos, metas, recursos y cronograma, con seguimiento mensual."),
               ("Indicadores", "Frecuencia, severidad, ausentismo y demás indicadores mínimos del artículo 30, con reporte a la dirección."),
               ("Gestión documental", "Kit documental SéVida: matriz de peligros, profesiograma, programas, procedimientos y registros."),
               ("Comités", "Acompañamiento al COPASST o vigía y al Comité de Convivencia Laboral (Resolución 3461 de 2025)."),
               ("Riesgo psicosocial", "Seguimiento al estado del riesgo psicosocial y coordinación de las intervenciones.")]
    c += seccion('<div class="rejilla r3">' + "".join(tarjeta(n, d) for n, d in incluye) + "</div>", "seccion-gris", "Qué incluye", "Su SG-SST, gestionado por un especialista")
    c += seccion('<div class="aviso"><strong>Una precisión sobre la calificación oficial.</strong> En la tabla de valores de la Resolución 0312, los ítems que no le aplican a una empresa pequeña suman su valor máximo. Por eso una microempresa puede obtener una calificación «aceptable» sin cumplir sus propios estándares. En SéVida reportamos las dos cifras: la oficial y el cumplimiento real de sus estándares.</div>' +
                 lista(["Especialista con licencia en SST vigente", "Sin costos de nómina, prestaciones ni dotación", "Mirada externa e independiente", "Acceso a la metodología y las herramientas de SéVida"]),
                 "", "Por qué externo", "Lo que gana frente a contratar internamente")
    c += cta("¿Qué nivel le corresponde a su empresa?", "Con el número de trabajadores y la clase de riesgo de su ARL se lo decimos en la primera conversación.")
    pagina("/servicios/acompanamiento-sst/", "Acompañamiento SST Mensual", "Acompañamiento mensual del SG-SST en tres niveles según la Resolución 0312 de 2019: 7, 21 o 60 estándares mínimos según el tamaño y el riesgo de la empresa.",
           c, kicker="Continuidad · SST", titulo_corto="Acompañamiento SST Mensual", lead="Su sistema de gestión de seguridad y salud en el trabajo, al día y documentado, sin el costo de un área interna.",
           ruta_migas=[("Servicios", "/servicios/"), ("Acompañamiento SST", None)], jsonld=[servicio_ld("Acompañamiento SST Mensual", "Acompañamiento del SG-SST en tres niveles: SV-SST-01, SV-SST-02 y SV-SST-03.", "/servicios/acompanamiento-sst/")], prioridad="0.8")


def talleres():
    lineas = json.loads((DATOS / "talleres.json").read_text(encoding="utf-8"))
    h = ""
    for l in lineas:
        h += f'<h2 style="margin-top:40px">{e(l["n"])} <span class="nota" style="font-family:var(--f-ui);font-size:1rem">· {len(l["t"])} talleres</span></h2><p class="lead">{e(l["d"])}</p><div class="rejilla r3" style="margin-top:18px">'
        h += "".join(f'<article class="tarjeta"><span class="codigo">{e(t["tema"].upper())}</span><h3>{e(t["titulo"])}</h3><p>{e(t["obj"])}</p></article>' for t in l["t"])
        h += "</div>"
    total = sum(len(l["t"]) for l in lineas)
    c = seccion('<div class="rejilla r4">' + "".join(f'<div class="tarjeta"><span class="numero">{len(l["t"])}</span><h3 style="margin-top:8px">{e(l["n"])}</h3></div>' for l in lineas) + "</div>" + h,
                "", "Formación", f"{total} talleres en 6 líneas", "Presencial, virtual o híbrido · De 1 a 2 horas · Hasta 30 participantes · Material digital y certificado de asistencia.")
    c += cta("¿Necesita un taller para su sector?", "Diseñamos talleres a la medida de su industria, su tamaño y sus retos.", "Solicitar un taller")
    pagina("/servicios/talleres/", "Talleres de bienestar y riesgo psicosocial", f"Catálogo de {total} talleres en 6 líneas: Fundamentos, Experiencias, Escuela de Liderazgo, Gestión Directiva, Familia y Alta Dirección.",
           c, kicker="Talleres", titulo_corto="Catálogo de talleres", lead="Formación práctica para trabajadores, líderes, familias y alta dirección.",
           ruta_migas=[("Servicios", "/servicios/"), ("Talleres", None)])


def coaching():
    c = seccion('<div class="rejilla r2"><div><p class="lead">Para gerentes, jefes y coordinadores que quieren liderar equipos saludables y obtener resultados sin desgastarse ni desgastar a su gente.</p>'
                '<h3 style="margin-top:26px">Qué resuelve</h3>' + lista(["Líderes que generan estrés en lugar de gestionarlo", "Equipos con alta rotación o bajo desempeño por el clima", "Retroalimentación que no funciona", "Transición a cargos de mayor responsabilidad", "Señales de agotamiento en el propio líder"]) + "</div>"
                '<div class="tarjeta tarjeta-destacada"><h3>Cómo funciona</h3>' + lista(["Sesiones de 60 minutos", "Virtual o presencial en Cali", "Frecuencia quincenal o mensual", "Herramientas y ejercicios entre sesiones", "Sesión única, paquete de 4 o de 8 sesiones"]) + "</div></div>",
                "", "Coaching de líderes", "Liderar sin quemarse ni quemar al equipo")
    c += seccion('<div class="rejilla r4">' + tarjeta("Autoconocimiento", "Estilo de liderazgo, puntos ciegos y fortalezas.") + tarjeta("Gestión emocional", "Regulación bajo presión y comunicación empática.") +
                 tarjeta("Equipo saludable", "Prevenir el riesgo psicosocial desde el liderazgo.") + tarjeta("Efectividad sostenible", "Resultados sin sacrificar el bienestar.") + "</div>", "seccion-gris", "Ejes", "Sobre qué se trabaja")
    c += cta("Agende una primera sesión", "Revisamos sus objetivos y definimos el número de sesiones.")
    pagina("/servicios/coaching-lideres/", "Coaching de líderes", "Coaching individual para líderes: liderazgo saludable, gestión emocional bajo presión y prevención del riesgo psicosocial en los equipos.",
           c, kicker="Desarrollo de líderes", titulo_corto="Coaching de líderes", ruta_migas=[("Servicios", "/servicios/"), ("Coaching de líderes", None)])


def metodo():
    detalle = '<div class="rejilla r3">' + "".join(
        f'<article class="tarjeta"><span class="numero">{l}</span><h3 style="margin-top:8px">{n}</h3><p>{d}</p></article>' for l, n, d in FASES) + "</div>"
    proceso = [("Conversación diagnóstica", "30 minutos, sin costo, para entender su contexto, sus retos y su estado normativo."),
               ("Propuesta", "Ajustada al tamaño, el sector y las necesidades de la organización."),
               ("Diagnóstico", "Aplicación de la batería oficial con análisis estadístico."),
               ("Intervención", "Programa, talleres, acompañamiento y herramientas para líderes y equipos."),
               ("Resultados", "Informe técnico, indicadores y presentación a la dirección."),
               ("Documentación", "Todo listo para inspecciones, auditorías y requerimientos.")]
    c = seccion(detalle, "", "Método S·É·V·I·D·A™", "Sensibilizar · Evaluar · Valorar · Intervenir · Dar seguimiento · Asegurar",
                "Es la estructura de todo lo que hace SéVida. Cada fase tiene entregables propios y prepara la siguiente.")
    c += seccion('<ol class="pasos">' + "".join(f"<li><strong>{n}</strong>{d}</li>" for n, d in proceso) + "</ol>", "seccion-gris", "Cómo trabajamos", "De la primera conversación al cambio sostenido")
    c += seccion('<div class="rejilla r3">' + tarjeta("Ausentismo", "Tendencia medida antes y después de la intervención.") + tarjeta("Rotación voluntaria", "Indicador trimestral.") +
                 tarjeta("Clima y riesgo", "Evaluación antes y después.") + "</div>" +
                 '<p class="nota" style="margin-top:16px">Los resultados dependen del diagnóstico inicial, del nivel de riesgo y del compromiso de la organización. Por eso se miden, no se prometen.</p>',
                 "", "Resultados", "Lo que la dirección puede ver")
    c += cta()
    pagina("/metodo/", "Método S·É·V·I·D·A", "El Método S·É·V·I·D·A™ de SéVida: Sensibilizar, Evaluar, Valorar, Intervenir, Dar seguimiento y Asegurar la gestión del riesgo psicosocial.",
           c, kicker="Método", titulo_corto="Método S·É·V·I·D·A™", lead="Seis fases para pasar del cumplimiento a una gestión del riesgo psicosocial que se sostiene.", ruta_migas=[("Método", None)], prioridad="0.8")


def nosotros():
    c = seccion('<div class="rejilla r2" style="align-items:start">'
                '<div class="foto-marcador" role="img" aria-label="Foto profesional pendiente">Foto profesional de Jose David Alomía Gutiérrez<br>(pendiente: checklist 1.7)</div>'
                '<div><span class="kicker">Dirección técnica</span><h2>Jose David Alomía Gutiérrez</h2>'
                '<p class="lead">Psicólogo de la Pontificia Universidad Javeriana y especialista en Gerencia de la Seguridad y Salud en el Trabajo de la Universidad Santiago de Cali, con licencia en SST vigente.</p>'
                '<p>Trabaja en salud ocupacional desde 2018: evaluaciones de aptitud laboral, seguimiento de casos de salud mental, aplicación de la Batería de Riesgo Psicosocial, análisis de puestos de trabajo y programas de bienestar laboral. Es docente universitario de modelos, técnicas e instrumentos de evaluación psicológica.</p>'
                '<p>En SéVida firma los informes técnicos y dirige la metodología de todos los servicios.</p></div></div>',
                "", None, None)
    c += seccion('<div class="rejilla r2"><div class="tarjeta"><h3>Misión</h3><p>Que las empresas colombianas gestionen el riesgo psicosocial con rigor técnico y lenguaje de gestión, y que el cumplimiento se convierta en mejores decisiones sobre su gente.</p></div>'
                 '<div class="tarjeta"><h3>Sectores con experiencia directa</h3><p><span class="etiqueta">Manufactura</span><span class="etiqueta">Salud</span><span class="etiqueta">Educación inicial</span><span class="etiqueta">Colegios privados</span><span class="etiqueta">Transporte</span><span class="etiqueta">Tecnología</span></p></div></div>',
                 "seccion-gris", "SéVida | Riesgo Psicosocial", "Una firma especializada")
    c += seccion('<div class="rejilla r3">' + tarjeta("Precisión normativa", "Citamos cada norma con su alcance real. La Resolución 2764 de 2022 derogó la 2404 de 2019, no la 2646 de 2008.") +
                 tarjeta("Aplicación en físico", "La batería se responde en papel, se sella y se devuelve de inmediato: así se protege el anonimato.") +
                 tarjeta("Costos antes que servicios", "Hablamos de rotación, ausentismo y exposición legal medidos, no prometidos.") + "</div>", "", "Principios", "Cómo trabajamos")
    c += cta()
    pagina("/nosotros/", "Nosotros", "SéVida es una firma especializada en riesgo psicosocial y SST en Cali, con dirección técnica de Jose David Alomía Gutiérrez, psicólogo especialista en SST.",
           c, kicker="Nosotros", titulo_corto="Rigor técnico aplicado a organizaciones reales", lead="Desde 2018 en salud ocupacional. Especialización exclusiva en riesgo psicosocial.", ruta_migas=[("Nosotros", None)])


NORMAS = [
    ("Resolución 2764 de 2022", "Ministerio del Trabajo · Batería de instrumentos", "Adopta la Batería de Instrumentos para la Evaluación de Factores de Riesgo Psicosocial como instrumento oficial. Derogó la Resolución 2404 de 2019; no derogó la 2646 de 2008. Los cuestionarios y el consentimiento se aplican en físico."),
    ("Resolución 2646 de 2008", "Ministerio de la Protección Social · Marco de obligaciones", "Define los factores de riesgo intralaborales, extralaborales e individuales y las obligaciones de identificar, evaluar, intervenir y monitorear. Sigue vigente y se aplica junto con la 2764 de 2022."),
    ("Decreto 1072 de 2015", "Decreto Único Reglamentario del Sector Trabajo", "El Libro 2, Parte 2, Título 4, Capítulo 6 regula el Sistema de Gestión de la Seguridad y Salud en el Trabajo. Todo empleador debe implementarlo."),
    ("Resolución 0312 de 2019", "Ministerio del Trabajo · Estándares mínimos del SG-SST", "7 estándares para empresas de hasta 10 trabajadores con riesgo I a III; 21 para empresas de 11 a 50 con riesgo I a III; 60 para empresas de más de 50 o con riesgo IV o V. Fija la tabla de valores (art. 27), los rangos de valoración (art. 28) y los indicadores mínimos (art. 30)."),
    ("Ley 1562 de 2012", "Sistema General de Riesgos Laborales", "Fija las sanciones por incumplir las normas de SST: hasta 500 salarios mínimos mensuales legales vigentes (art. 13)."),
    ("Ley 1010 de 2006", "Acoso laboral", "Define, previene, corrige y sanciona el acoso laboral en las relaciones de trabajo."),
    ("Resolución 3461 de 2025", "Ministerio del Trabajo · Comité de Convivencia Laboral", "Rige desde el 1 de septiembre de 2025 y derogó las Resoluciones 652 y 1356 de 2012. Reuniones ordinarias mensuales; procedimiento de queja de máximo 65 días calendario; el comité no tramita acoso sexual. En 2026 el Ministerio publicó para comentarios un proyecto que la modificaría."),
    ("Ley 2365 de 2024", "Acoso sexual en el ámbito laboral", "Las quejas de acoso sexual se tramitan por fuera del Comité de Convivencia, con protocolos internos de la empresa."),
    ("Resolución 1843 de 2025", "Ministerio del Trabajo · Evaluaciones médicas ocupacionales", "Vigente desde el 6 de mayo de 2025. Derogó las Resoluciones 2346 de 2007, 1918 de 2009, 1075 de 1992 y 4050 de 1994. Regula las evaluaciones médicas, el plazo de 20 días hábiles para adaptar el puesto y la custodia de la historia clínica por la IPS."),
    ("Decreto 728 de 2025", "Ministerio del Trabajo · Salud mental y sustancias psicoactivas", "Incorpora al Decreto 1072 de 2015 obligaciones de promoción de la salud mental y prevención del consumo de sustancias psicoactivas en el trabajo."),
    ("Ley 2088 de 2021", "Trabajo en casa", "Modalidad ocasional y temporal. El empleador mantiene sus obligaciones de SST, incluido el riesgo psicosocial."),
    ("Ley 2121 de 2021 y Decreto 555 de 2022", "Trabajo remoto", "Modalidad permanente. El empleador gestiona los riesgos del trabajador remoto, incluidos el aislamiento y la dificultad de desconexión."),
]


def normativa():
    h = '<div class="rejilla r2">' + "".join(f'<article class="tarjeta"><span class="codigo">{e(s)}</span><h3>{e(n)}</h3><p>{e(d)}</p></article>' for n, s, d in NORMAS) + "</div>"
    c = seccion('<div class="aviso aviso-dorado"><strong>Actualizado a noviembre de 2026.</strong> Las normas cambian. Antes de una decisión legal, verifique el texto vigente en la fuente oficial o consúltelo con nosotros.</div>' + h, "", None, None)
    c += cta("¿Su empresa cumple con todo esto?", "En 30 minutos revisamos su estado normativo y le entregamos las prioridades.", "Revisar mi empresa")
    pagina("/normativa/", "Normativa de riesgo psicosocial y SST en Colombia", "Marco normativo vigente del riesgo psicosocial y la SST en Colombia: Resoluciones 2764 de 2022, 2646 de 2008, 0312 de 2019, 3461 de 2025, 1843 de 2025 y más.",
           c, kicker="Recursos", titulo_corto="Normativa vigente", lead="Las normas que regulan la evaluación y la gestión del riesgo psicosocial, con su alcance real.", ruta_migas=[("Normativa", None)], prioridad="0.8")


def ismo():
    c = seccion('<div class="rejilla r2" style="align-items:start"><div id="ismo" class="ismo" aria-live="polite"><noscript>Active JavaScript para usar el Índice ISMO.</noscript></div>'
                '<div><div class="tarjeta"><h3>Cómo se calcula</h3><p>Seis dimensiones organizacionales pesan el 80 % y el cumplimiento legal el 20 %. Cada respuesta suma según el nivel de riesgo que describe.</p>'
                '<p>El resultado ubica a la organización en uno de cinco niveles de madurez: Reactivo, Cumplimiento básico, Gestión estructurada, Gestión estratégica y Cultura preventiva.</p></div>'
                '<div class="aviso"><strong>Por qué no usamos colores de semáforo.</strong> Los colores rojo, amarillo y verde empujan a responder lo que «se ve bien». Sin ellos, las respuestas son más honestas y el resultado más útil.</div>'
                '<div class="aviso aviso-dorado"><strong>Qué no es.</strong> El ISMO orienta. No reemplaza la Batería de Riesgo Psicosocial ni la autoevaluación de estándares mínimos.</div></div></div>')
    pagina("/ismo/", "Índice ISMO — diagnóstico gratuito de madurez organizacional", "Índice SéVida de Madurez Organizacional (ISMO): diagnóstico gratuito de 10 minutos sobre riesgo psicosocial, salud mental, liderazgo, indicadores y cumplimiento legal.",
           c, kicker="Herramienta gratuita", titulo_corto="Índice SéVida de Madurez Organizacional (ISMO)", lead="Ocho dimensiones, diez minutos y un resultado con recomendaciones concretas para su organización.",
           ruta_migas=[("Índice ISMO", None)], scripts=("ismo.js",), prioridad="0.9")


FAQ = [
    ("Recibí una cotización más económica. ¿Por qué la diferencia?", "Casi siempre se explica por una de cuatro razones: instrumentos incompletos (el cuestionario de estilos de afrontamiento es el que más se omite), ausencia del programa de vigilancia epidemiológica, informe sin firma de un profesional con licencia en SST o aplicación sin condiciones controladas. Pida a cada proveedor el detalle de los instrumentos incluidos y el nombre de quien firma el informe."),
    ("Ya tenemos un proveedor para todo el SG-SST. ¿Vale la pena separar el psicosocial?", "El riesgo psicosocial es el único del SG-SST que exige un instrumento psicométrico estandarizado, interpretación por un profesional con licencia y un programa de vigilancia propio. Trabajamos con frecuencia en paralelo a la firma que lleva el SG-SST: no hay que cambiar de proveedor."),
    ("Tenemos psicóloga en talento humano. ¿Podemos aplicar la batería internamente?", "Depende de dos condiciones: licencia en SST vigente, no solo tarjeta profesional, y capacidad para sostener la vigilancia epidemiológica. Además, cuando el área que gestiona el clima es la misma que mide el riesgo, el resultado queda expuesto a cuestionamiento, sobre todo en una determinación de origen."),
    ("¿No basta con talleres de manejo del estrés?", "No. La Resolución 2646 de 2008 obliga a identificar, evaluar, intervenir y monitorear. Un taller no documenta esas fases ni cambia la fuente del riesgo: si el factor crítico es la sobrecarga, se interviene la distribución de la carga."),
    ("No tenemos presupuesto este año. ¿Qué alternativas hay?", "Empiece por el Índice ISMO y por la conversación diagnóstica, que no tienen costo. Si hay decisión de avanzar, se puede hacer el diagnóstico en este período y la intervención en el siguiente. Revise también qué actividades de prevención cubre su ARL."),
    ("¿Cada cuánto hay que repetir la batería?", "Como mínimo cada dos años, y antes si hay cambios organizacionales relevantes. Si la última aplicación usó la Resolución 2404 de 2019, hoy derogada, hay que actualizar los instrumentos."),
    ("¿Trabajan con empresas pequeñas?", "Sí. La obligación de evaluar el riesgo psicosocial aplica a toda empresa con trabajadores. Para empresas de hasta 10 trabajadores tenemos el nivel SV-SST-01 del Acompañamiento SST."),
]


def contacto():
    form = f"""<form id="form-contacto" class="formulario" novalidate>
<input type="text" name="_honey" class="oculto" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="campo-doble"><div class="campo"><label for="nombre">Nombre completo *</label><input id="nombre" name="nombre" required autocomplete="name"><p class="error">Escriba su nombre.</p></div>
<div class="campo"><label for="cargo">Cargo</label><input id="cargo" name="cargo" autocomplete="organization-title"></div></div>
<div class="campo-doble"><div class="campo"><label for="empresa">Empresa *</label><input id="empresa" name="empresa" required autocomplete="organization"><p class="error">Escriba el nombre de la empresa.</p></div>
<div class="campo"><label for="trabajadores">Número de trabajadores</label><select id="trabajadores" name="trabajadores"><option value="">Seleccione…</option><option>Hasta 10</option><option>11 a 50</option><option>51 a 200</option><option>201 a 500</option><option>Más de 500</option></select></div></div>
<div class="campo-doble"><div class="campo"><label for="correo">Correo electrónico *</label><input id="correo" name="correo" type="email" required autocomplete="email"><p class="error">Escriba un correo válido.</p></div>
<div class="campo"><label for="telefono">Teléfono</label><input id="telefono" name="telefono" type="tel" autocomplete="tel"></div></div>
<div class="campo"><label for="servicio">¿En qué podemos ayudarle? *</label><select id="servicio" name="servicio" required><option value="">Seleccione…</option>
<option>Diagnóstico SéVida (Batería de Riesgo Psicosocial)</option><option>Recalibra Empresarial</option><option>Programa Integral SéVida</option><option>Vigilancia epidemiológica (PVE)</option>
<option>Acompañamiento SST Mensual</option><option>Análisis de puesto de trabajo</option><option>Talleres</option><option>Coaching de líderes</option><option>Información general</option></select><p class="error">Seleccione una opción.</p></div>
<div class="campo"><label for="mensaje">Mensaje</label><textarea id="mensaje" name="mensaje" rows="5"></textarea></div>
<div class="campo campo-autorizacion">
  <input type="checkbox" id="autorizacion" name="autorizacion_datos" value="Sí" required>
  <label for="autorizacion" style="font-weight:400;font-family:inherit;color:inherit">Autorizo a SéVida a tratar mis datos personales para responder mi solicitud, incluida su transmisión a FormSubmit, conforme a la <a href="/politica-de-datos/" target="_blank" rel="noopener">política de tratamiento de datos</a>.</label>
</div>
<p class="error" style="margin-top:-8px">Para enviar el formulario debe autorizar el tratamiento de sus datos.</p>
<button class="btn btn-primario" type="submit">Enviar mensaje</button>
<p id="estado-envio" class="estado-envio" role="status"></p>
</form>"""
    canales = (f'<div class="tarjeta"><h3>Canales directos</h3>' + lista([
        f'<strong>WhatsApp:</strong> <a href="https://wa.me/{WHATSAPP}">+57 316 876 8220</a>',
        f'<strong>Teléfono:</strong> <a href="tel:{TELEFONO.replace(" ", "")}">{TELEFONO}</a> · lunes a viernes, 8:00 a. m. a 6:00 p. m.',
        f'<strong>Correo:</strong> <a href="mailto:{CORREO}">{CORREO}</a> · respuesta en 24 horas hábiles',
        f'<strong>Ubicación:</strong> {CIUDAD}. Atención presencial y virtual en todo el país.']) +
        '<div class="aviso" style="margin-top:22px"><strong>Conversación diagnóstica de 30 minutos.</strong> Sin costo. Revisamos su situación y le decimos qué falta y en qué orden resolverlo.</div></div>')
    c = seccion(f'<div class="rejilla r2" style="align-items:start"><div class="tarjeta">{form}</div>{canales}</div>')
    c += f'<section class="seccion seccion-gris" id="preguntas"><div class="contenedor"><span class="kicker">Antes de decidir</span><h2>Preguntas frecuentes</h2>' + "".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in FAQ) + "</div></section>"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    pagina("/contacto/", "Contacto", "Agende una conversación diagnóstica de 30 minutos sin costo con SéVida. WhatsApp, teléfono, correo y formulario de contacto.",
           c, kicker="Contacto", titulo_corto="Hablemos de su organización", lead="Déjenos sus datos y le respondemos en un máximo de 24 horas hábiles.",
           ruta_migas=[("Contacto", None)], scripts=("contacto.js",), jsonld=[ld], prioridad="0.9")


def politica():
    s = [
        ("1. Responsable del tratamiento", f"SéVida | Riesgo Psicosocial, representada por Jose David Alomía Gutiérrez, psicólogo especialista en Gerencia de la Seguridad y Salud en el Trabajo. Domicilio: {CIUDAD}, Colombia. Correo: <a href=\"mailto:{CORREO}\">{CORREO}</a>. Teléfono: {TELEFONO}."),
        ("2. Datos que recolectamos", "A través del formulario de contacto y del Índice ISMO recolectamos: nombre, cargo, empresa, sector, número de trabajadores, ciudad, correo electrónico, teléfono, el contenido de su mensaje y las respuestas organizacionales que usted entregue. No solicitamos datos sensibles ni datos de menores de edad por estos medios."),
        ("3. Finalidades", "Usamos sus datos para: (a) responder su solicitud de información o cotización; (b) entregarle y explicarle el resultado del Índice ISMO cuando usted decide enviarlo; (c) contactarlo sobre los servicios de SéVida relacionados con su solicitud; (d) gestionar la relación contractual si se concreta; y (e) llevar registro interno de las solicitudes recibidas. No vendemos, arrendamos ni cedemos sus datos."),
        ("4. Encargados del tratamiento y transmisión internacional de datos", "Para recibir los mensajes del formulario de contacto y los resultados del Índice ISMO, SéVida usa el servicio FormSubmit (formsubmit.co), que actúa como encargado del tratamiento: recibe los datos que usted escribe (nombre, empresa, correo, teléfono, mensaje y, si lo envía, el resultado del ISMO) y los reenvía al correo de SéVida. FormSubmit procesa esta información en servidores ubicados fuera de Colombia, por lo que su envío constituye una transmisión internacional de datos personales.<br><br>Al marcar la casilla de autorización del formulario, usted autoriza de manera previa, expresa e informada esta transmisión. SéVida solo usa sus datos para las finalidades de esta política. El correo de SéVida se gestiona con un proveedor de correo electrónico que también actúa como encargado."),
        ("5. Derechos del titular", "Usted puede conocer, actualizar y rectificar sus datos; solicitar prueba de la autorización; ser informado sobre su uso; presentar quejas ante la Superintendencia de Industria y Comercio; revocar la autorización o pedir la supresión de sus datos cuando no exista un deber legal o contractual de conservarlos; y acceder gratuitamente a ellos."),
        ("6. Cómo ejercer sus derechos", f"Escriba a <a href=\"mailto:{CORREO}\">{CORREO}</a> con el asunto «Habeas data», indicando su nombre, el derecho que quiere ejercer y los hechos de su solicitud. Respondemos las consultas en máximo 10 días hábiles y los reclamos en máximo 15 días hábiles (Ley 1581 de 2012, artículos 14 y 15)."),
        ("7. Conservación y vigencia", "Conservamos los datos mientras se mantenga la finalidad del tratamiento o la relación comercial, y los suprimimos cuando usted lo solicite y no exista deber legal de conservarlos. Esta política rige desde su publicación en este sitio."),
    ]
    h = '<div class="articulo">' + "".join(f"<h2>{t}</h2><p>{x}</p>" for t, x in s) + f'<p class="nota" style="margin-top:30px">Ley Estatutaria 1581 de 2012 · Decreto 1377 de 2013 (compilado en el Decreto 1074 de 2015). Última actualización: noviembre de 2026.</p></div>'
    pagina("/politica-de-datos/", "Política de tratamiento de datos personales", "Política de tratamiento de datos personales de SéVida conforme a la Ley 1581 de 2012: responsable, finalidades, encargados, transmisión internacional y derechos del titular.",
           seccion(h), kicker="Protección de datos", titulo_corto="Política de tratamiento de datos personales", ruta_migas=[("Política de datos", None)], prioridad="0.3")


# ---------------------------------------------------------------- Blog
ARTICULOS = []


def limpiar_marca(s):
    reemplazos = [("Vitalis Empresarial®", "SéVida"), ("Vitalis Empresarial", "SéVida"), ("RESET LABORAL®", "Recalibra"), ("RESET LABORAL", "Recalibra"),
                  ("Programa RESET Empresarial", "Recalibra Empresarial"), ("IVSO™", "ISMO"), ("IVSO", "ISMO"), ("Índice Vitalis", "Índice SéVida"),
                  ("Vitalis", "SéVida"), ("®", ""), ("Diagnóstico Express", "conversación diagnóstica"),
                  ("Programa Evolución", "Recalibra Empresarial"), ("programa Evolución", "programa Recalibra Empresarial")]
    for a, b in reemplazos:
        s = s.replace(a, b)
    return s


def migrar_blog():
    from bs4 import BeautifulSoup
    origen = DATOS / "blog-origen"
    for f in sorted(origen.glob("*.html")):
        if f.name == "index.html":
            continue
        slug = f.stem
        soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
        titulo = soup.find("h1").get_text(" ", strip=True)
        desc = (soup.find("meta", attrs={"name": "description"}) or {}).get("content", "")
        meta = soup.find(class_="meta")
        eyebrow = soup.find(class_="eyebrow")
        cuerpo = soup.find("div", class_="body") or soup.find("article")
        intro = soup.find("p", class_="intro")
        for basura in cuerpo.find_all(class_=["tags", "author", "cta-box", "cta", "firma", "cierre"]):
            basura.decompose()
        mapa = {"alerta": "aviso aviso-rojo", "destaque": "aviso aviso-dorado", "verde": "aviso aviso-verde", "tabla-wrapper": "tabla-envoltura", "pregunta": "pregunta-clave", "checklist": "aviso"}
        for t in cuerpo.find_all(True):
            if t.get("class"):
                t["class"] = [mapa.get(c, c) for c in t["class"]]
            if t.name == "a" and t.get("href"):
                h = t["href"]
                h = re.sub(r"^\.\./index\.html#ivso", "/ismo/", h)
                h = re.sub(r"^\.\./index\.html#([a-z-]+)", lambda m: {"contacto": "/contacto/", "normativa": "/normativa/", "bateria": "/servicios/bateria-riesgo-psicosocial/", "servicios": "/servicios/"}.get(m.group(1), "/"), h)
                h = re.sub(r"^\.\./index\.html$", "/", h)
                h = re.sub(r"^index\.html$", "/blog/", h)
                h = re.sub(r"^([a-z0-9-]+)\.html(#.*)?$", lambda m: f"/blog/{m.group(1)}/" + (m.group(2) or ""), h)
                t["href"] = h
            if t.has_attr("style"):
                del t["style"]
        html_cuerpo = (str(intro).replace('class="intro"', 'class="lead"') if intro else "") + "".join(str(x) for x in cuerpo.contents)
        html_cuerpo = limpiar_marca(html_cuerpo)
        # Cifra sin fuente verificable (checklist 1.3): se reemplaza por una afirmación sin cifra
        html_cuerpo = html_cuerpo.replace(
            "Según datos del Ministerio del Trabajo, más del 65% de las empresas evaluadas presentan niveles de riesgo medio o alto en al menos una dimensión de la batería psicosocial — y la mayoría lo desconoce.",
            "Muchas empresas tienen niveles de riesgo medio o alto en al menos un dominio de la batería y no lo saben, porque nunca la han aplicado o no han leído sus resultados por área.")
        assert "65%" not in html_cuerpo, slug
        # Cifras revisadas el 5 nov 2026: OIT (2000) decía 3-4 % del PNB solo para la UE; se reemplaza por OMS/OIT (2022).
        # El rango 50-200 % es de Gallup (2019), estimación conservadora para Estados Unidos y rotación voluntaria.
        CORRECCIONES = [
            ("La Organización Internacional del Trabajo (OIT) estima que los trastornos de salud mental relacionados con el trabajo representan entre el 2,5% y el 4% del PIB de los países industrializados en términos de pérdida de productividad, ausentismo y costos de atención en salud.",
             'Según la Organización Mundial de la Salud y la Organización Internacional del Trabajo, cada año se pierden en el mundo unos 12.000 millones de jornadas laborales por depresión y ansiedad, con un costo cercano a un billón de dólares en productividad (<a href="https://www.paho.org/es/noticias/28-9-2022-oms-oit-piden-nuevas-medidas-para-abordar-problemas-salud-mental-trabajo" target="_blank" rel="noopener">OMS y OIT, 2022</a>).'),
            ("El costo de reemplazar un trabajador que rota involuntariamente se estima entre el 50% y el 200% de su salario anual, dependiendo del nivel de calificación del cargo — y el riesgo psicosocial no gestionado es uno de los predictores más consistentes de la rotación no deseada.",
             'Gallup estima, de forma conservadora y con datos de Estados Unidos, que reemplazar a un trabajador que renuncia cuesta entre la mitad y el doble de su salario anual, según el cargo (<a href="https://www.gallup.com/workplace/247391/fixable-problem-costs-businesses-trillion.aspx" target="_blank" rel="noopener">Gallup, 2019</a>). No hay una cifra equivalente publicada para Colombia, pero el orden de magnitud sirve para dimensionar el problema; las condiciones de trabajo que mide la batería están entre los factores que empujan esas renuncias.'),
            ("como se mencionó antes, el costo de reemplazar un trabajador calificado puede equivaler a entre el 50% y el 200% de su salario anual. El riesgo psicosocial no gestionado es un predictor robusto de rotación voluntaria.",
             "como se mencionó antes, reemplazar a un trabajador que renuncia puede costar entre la mitad y el doble de su salario anual (Gallup, 2019, datos de Estados Unidos). Las condiciones de trabajo que mide la batería influyen en esas renuncias."),
        ]
        for a, b in CORRECCIONES:
            html_cuerpo = html_cuerpo.replace(a, b)
        for prohibida in ("2,5% y el 4%", "50% y el 200%"):
            assert prohibida not in html_cuerpo, (slug, prohibida)
        # Sanción en pesos actualizada al salario mínimo de 2026 ($1.750.905): 500 SMMLV ≈ $875 millones (checklist 2.1)
        html_cuerpo = re.sub(r"\$711 millones( de pesos)?", "$875 millones", html_cuerpo)
        titulo, desc = limpiar_marca(titulo), limpiar_marca(desc)
        meta_txt = limpiar_marca(meta.get_text(" ", strip=True)) if meta else "Por Jose David Alomía Gutiérrez"
        cat = limpiar_marca(eyebrow.get_text(" ", strip=True)).replace("Blog · ", "") if eyebrow else "Riesgo psicosocial"
        ARTICULOS.append((slug, titulo, desc, cat))
        autor = ('<div class="autor"><img src="/assets/img/sevida-isotipo.svg" alt="" width="56" height="56"><div><strong>Jose David Alomía Gutiérrez</strong><br>'
                 '<span class="nota">Dirección técnica de SéVida · Psicólogo especialista en Gerencia de la Seguridad y Salud en el Trabajo</span></div></div>')
        cuerpo_final = f'<section class="seccion"><div class="contenedor"><article class="articulo">{html_cuerpo}{autor}</article></div></section>' + cta("¿Quiere aplicar esto en su empresa?", "Revisemos su caso en una conversación diagnóstica de 30 minutos, sin costo.")
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es-CO",
              "author": {"@type": "Person", "name": "Jose David Alomía Gutiérrez"}, "publisher": {"@type": "Organization", "name": "SéVida | Riesgo Psicosocial", "logo": {"@type": "ImageObject", "url": DOMINIO + "/assets/img/sevida-logo-principal.svg"}},
              "mainEntityOfPage": f"{DOMINIO}/blog/{slug}/"}
        pagina(f"/blog/{slug}/", titulo, desc, cuerpo_final, kicker=cat, titulo_corto=titulo, lead=f'<span class="meta" style="color:#C9D3DF">{e(meta_txt)}</span>',
               ruta_migas=[("Blog", "/blog/"), (titulo, None)], jsonld=[ld], tipo="article", prioridad="0.6")


def BLOG_RESUMEN():
    if not ARTICULOS:
        return ""
    return '<div class="rejilla r3">' + "".join(tarjeta(e(t), e(d), f"/blog/{s}/", "Leer", e(c.upper())) for s, t, d, c in ARTICULOS[:3]) + \
           '</div><p style="margin-top:22px"><a class="btn btn-secundario" href="/blog/">Ver todos los artículos</a></p>'


def blog_indice():
    h = '<div class="rejilla r3">' + "".join(tarjeta(e(t), e(d), f"/blog/{s}/", "Leer el artículo", e(c.upper())) for s, t, d, c in ARTICULOS) + "</div>"
    pagina("/blog/", "Blog de riesgo psicosocial y SST", "Artículos técnicos sobre riesgo psicosocial y SST en Colombia, escritos por psicólogo especialista con licencia en SST.",
           seccion(h), kicker="Recursos", titulo_corto="Blog", lead="Contenido técnico con base normativa actualizada, para decidir mejor.", ruta_migas=[("Blog", None)], prioridad="0.7")


def error_404():
    c = seccion('<div class="centro"><span class="numero" style="font-size:5rem">404</span><h2 style="margin-top:12px">Esta página no existe</h2><p class="lead">Puede que el enlace sea del sitio anterior o que la página haya cambiado de dirección.</p>'
                '<p style="margin-top:24px"><a class="btn btn-primario" href="/">Ir al inicio</a> <a class="btn btn-secundario" href="/servicios/">Ver servicios</a></p></div>')
    pagina("/404/", "Página no encontrada", "La página que busca no existe.", c, cabecera=False, indexar=False)
    (PUB / "404.html").write_text((PUB / "404" / "index.html").read_text(encoding="utf-8"), encoding="utf-8")
    import shutil
    shutil.rmtree(PUB / "404")


HTACCESS = r"""# SéVida — Hostinger (Apache / LiteSpeed). Lo genera tools/build.py.
# Equivale a _redirects y _headers, que solo usa Cloudflare Pages.
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
RewriteEngine On

# HTTPS y dominio sin www
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\. [NC]
RewriteRule ^(.*)$ https://@HOST@/$1 [R=301,L]

# /index.html -> /   y   /carpeta/index.html -> /carpeta/
RewriteCond %{THE_REQUEST} \s/+((?:[^\s?]*/)?)index\.html[\s?]
RewriteRule ^ /%1 [R=301,L]

# Rutas del sitio anterior
RewriteRule ^blog/([a-z0-9-]+)\.html$ /blog/$1/ [R=301,L]
RewriteRule ^ivso/?$ /ismo/ [R=301,L]
RewriteRule ^(evolucion|reset-laboral)/?$ /servicios/recalibra-empresarial/ [R=301,L]
</IfModule>

<FilesMatch "^_(redirects|headers)$">
Require all denied
</FilesMatch>

<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
<FilesMatch "\.(css|js|png|jpe?g|svg|webp|ico|woff2?)$">
Header set Cache-Control "public, max-age=604800"
</FilesMatch>
</IfModule>
"""


def extras():
    urls = "".join(f"<url><loc>{DOMINIO}{r}</loc><lastmod>{HOY}</lastmod><priority>{p}</priority></url>" for r, p in sorted(PAGINAS))
    (PUB / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    redir = ["# Solo para Cloudflare Pages (alternativa). En Hostinger las redirecciones están en public/.htaccess",
             "/index.html / 301", "/blog/index.html /blog/ 301"]
    redir += [f"/blog/{s}.html /blog/{s}/ 301" for s, *_ in ARTICULOS]
    redir += ["/ivso /ismo/ 301", "/ivso/ /ismo/ 301", "/evolucion/ /servicios/recalibra-empresarial/ 301", "/reset-laboral/ /servicios/recalibra-empresarial/ 301"]
    (PUB / "_redirects").write_text("\n".join(redir) + "\n", encoding="utf-8")
    (PUB / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n/assets/*\n  Cache-Control: public, max-age=604800\n", encoding="utf-8")
    (PUB / ".htaccess").write_text(HTACCESS.replace("@HOST@", DOMINIO.split("//")[1]), encoding="utf-8")


if __name__ == "__main__":
    migrar_blog()
    for f in (inicio, servicios, recalibra, bateria, apt, pve, sst, talleres, coaching, metodo, nosotros, normativa, ismo, contacto, politica, blog_indice, error_404):
        f()
    extras()
    print(f"{len(PAGINAS)} páginas indexables generadas en {PUB}")
