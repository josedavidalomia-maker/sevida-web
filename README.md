# SéVida™ | Riesgo Psicosocial — sitio web

Sitio estático multipágina de **sevida.com.co**. Reemplaza la página única del repositorio `vitalis-web`.

## Estructura

```
public/                  ← carpeta que se publica (Cloudflare Pages, salida "public")
  index.html             inicio
  servicios/…            7 páginas de servicios
  metodo/ nosotros/ normativa/ ismo/ contacto/ politica-de-datos/
  blog/ y blog/<slug>/   índice y 10 artículos
  404.html  sitemap.xml  robots.txt  _redirects  _headers
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
4. Haga commit y push. Cloudflare Pages publica solo.

## Antes de publicar (checklist de lanzamiento)

- [ ] `contacto@sevida.com.co` activo (en `tools/build.py`, variable `CORREO`).
- [ ] Token de FormSubmit en `public/assets/js/contacto.js` y `public/assets/js/ismo.js` (`FORMSUBMIT_TOKEN`).
- [ ] Redes renombradas a SéVida y enlaces actualizados (`LINKEDIN`, `INSTAGRAM` en `tools/build.py`).
- [ ] Foto profesional en `/nosotros/` (hoy hay un marcador).
- [ ] Confirmar ISMO, nombres de las líneas de talleres y el lema «Medir. Intervenir. Recalibrar.».
- [ ] Radicación de la marca ante la SIC.

## Decisiones aplicadas en esta versión (5 de noviembre de 2026)

- Acompañamiento SST en tres niveles: SV-SST-01 (hasta 10, 7 estándares), SV-SST-02 (11 a 50, 21), SV-SST-03 (51 a 200 o riesgo IV/V, 60).
- Cifra «más del 65 %» retirada del blog (sin fuente verificable). «9,4 días» citado como EALI con datos de 2023 (CESLA-ANDI, nov. 2024).
- Sanción en pesos actualizada a $875 millones (500 SMMLV de 2026), siempre con el año.
- Política de datos con FormSubmit como encargado y transmisión internacional; casilla obligatoria de autorización en los formularios.
- Índice ISMO en un solo lugar del menú; sin semáforo de colores; sin promesa de «análisis con IA».
- Normativa actualizada: Res. 3461 de 2025, Res. 1843 de 2025, Ley 2365 de 2024; Res. 0312 corregida a 7/21/60.

© 2026 SéVida | Riesgo Psicosocial · Dirección técnica: Jose David Alomía Gutiérrez
