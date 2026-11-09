# SéVida™ | Riesgo Psicosocial — sitio web

Sitio estático multipágina de **sevidapsicosocial.com**. Reemplaza la página única del repositorio `vitalis-web`.

## Estructura

```
public/                  ← carpeta que se publica (su contenido va a public_html en Hostinger)
  index.html             inicio
  servicios/…            8 páginas de servicios (incluye Análisis de puesto de trabajo)
  metodo/ nosotros/ normativa/ ismo/ contacto/ politica-de-datos/
  blog/ y blog/<slug>/   índice y 10 artículos
  404.html sitemap.xml robots.txt
  .htaccess              redirecciones, HTTPS y encabezados para Hostinger
  _redirects _headers    equivalentes para Cloudflare Pages (alternativa; Hostinger los ignora)
  assets/css/sevida.css  hoja de estilos única
  assets/js/site.js      navegación y redirección de anclas antiguas (#servicios, #ivso…)
  assets/js/ismo.js      motor del Índice ISMO (DIMS × 0,80 + LEGAL × 0,20)
  assets/js/contacto.js  formulario de contacto (FormSubmit)
  assets/img/            logotipo v2 (SVG), isotipo, favicons, imagen para redes
tools/build.py           generador de las páginas (no hace falta para publicar)
tools/datos/             catálogo de talleres y artículos originales del blog
```

## Cómo cambiar un texto

1. Edite el contenido en `tools/build.py` (sección CONTENIDO).
2. Ejecute `python3 tools/build.py` (requiere `beautifulsoup4`).
3. Revise el cambio en local: `cd public && python3 -m http.server 8000` y abra http://localhost:8000
4. Haga commit y push, y suba a Hostinger el contenido de `public/` (ver DESPLIEGUE.md).

## Antes de publicar (checklist de lanzamiento)

En este orden:

- [ ] Radicación de la marca ante la SIC.
- [ ] Compra del hosting en Hostinger y del dominio `sevidapsicosocial.com`.
- [ ] `contacto@sevidapsicosocial.com` activo. Hoy el sitio y los formularios usan el Gmail de forma temporal; al activarlo: en `tools/build.py` use `CORREO = CORREO_SEVIDA` y vuelva a generar, y en `public/assets/js/contacto.js` y `public/assets/js/ismo.js` use `CORREO_ACTIVO = CORREO_SEVIDA`.
- [ ] Activar FormSubmit con el enlace que llega al buzón tras el primer envío (se repite al cambiar de correo). Opcional: usar la cadena aleatoria en `FORMSUBMIT_TOKEN`.
- [ ] Redes renombradas a SéVida y enlaces actualizados (`LINKEDIN`, `INSTAGRAM` en `tools/build.py`).
- [ ] Foto profesional nueva en `/nosotros/` (hoy hay un marcador).
- [x] ISMO, nombres de las líneas de talleres y el lema «Medir. Intervenir. Recalibrar.» confirmados (5 de noviembre de 2026).

## Decisiones aplicadas

### 9 de noviembre de 2026

- Dominio principal: `sevidapsicosocial.com` (antes `sevida.com.co`) en URL canónicas, sitemap, Open Graph, JSON-LD, robots y correo de contacto.
- Hosting: Hostinger. Nuevo `public/.htaccess` (generado por `build.py`) con HTTPS, dominio sin www, redirecciones del sitio anterior y encabezados de seguridad.
- Análisis de puesto de trabajo (APT) separado de la batería: nueva página `/servicios/analisis-puesto-trabajo/` (APT preventivo SV-MD-APT-21 y APT para determinación de origen SV-FT-APT-20 · SV-FT-APT-22), con entrada en el menú, el pie, el índice de servicios y el sitemap. La página de la batería ya no incluye el APT; enlaza al servicio nuevo.
- Línea de talleres «Líderes» renombrada a **Gestión Directiva**.

### 5 de noviembre de 2026

- Acompañamiento SST en tres niveles: SV-SST-01 (hasta 10, 7 estándares), SV-SST-02 (11 a 50, 21), SV-SST-03 (51 a 200 o riesgo IV/V, 60).
- Cifra «más del 65 %» retirada del blog (sin fuente verificable). «9,4 días» citado como EALI con datos de 2023 (CESLA-ANDI, nov. 2024).
- Sanción en pesos actualizada a $875 millones (500 SMMLV de 2026), siempre con el año.
- Política de datos con FormSubmit como encargado y transmisión internacional; casilla obligatoria de autorización en los formularios.
- Índice ISMO en un solo lugar del menú; sin semáforo de colores; sin promesa de «análisis con IA».
- Normativa actualizada: Res. 3461 de 2025, Res. 1843 de 2025, Ley 2365 de 2024; Res. 0312 corregida a 7/21/60.

---

© 2026 SéVida | Riesgo Psicosocial · Dirección técnica: Jose David Alomía Gutiérrez
