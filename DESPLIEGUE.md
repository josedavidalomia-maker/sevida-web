# Despliegue de sevidapsicosocial.com (Hostinger)

Orden acordado: primero la radicación de la marca ante la SIC; después la compra del hosting y del dominio.

## 1. Hosting y dominio

1. Compre en Hostinger un plan de hosting web y el dominio `sevidapsicosocial.com` (sin tilde: los dominios con tilde funcionan, pero se escriben mal y fallan en correos y redes).
2. En hPanel, active el certificado SSL gratuito del dominio.
3. Cree el buzón `contacto@sevidapsicosocial.com` (*Correos*) y regístrelo en FormSubmit para obtener el token.

## 2. Publicar el sitio

El sitio no necesita compilación: se publica el **contenido** de la carpeta `public/` dentro de `public_html`.

**Opción A — Administrador de archivos (la más simple)**

1. Descargue el repositorio (*Code → Download ZIP*) y comprima solo el contenido de `public/`.
2. En hPanel → *Administrador de archivos* → `public_html`: suba el ZIP y extráigalo ahí.
3. Verifique que `index.html` y `.htaccess` queden directamente en `public_html` (los archivos que empiezan por punto pueden estar ocultos: active «mostrar archivos ocultos»).

**Opción B — Git en hPanel**

hPanel → *Avanzado → Git* puede clonar este repositorio, pero publica la raíz del repositorio, no `public/`. Si se usa esta opción, clone en una carpeta aparte y copie `public/` a `public_html`, o pida a soporte de Hostinger que apunte el dominio a `…/sevida-web/public`.

## 3. Comprobar

- Las 26 rutas del sitemap, la 404 y el ISMO completo.
- Un envío del formulario de contacto.
- Redirecciones: `http://` → `https://`, `www.` → sin www, `/index.html` → `/`, `/blog/<slug>.html` → `/blog/<slug>/`, `/ivso` → `/ismo/`.
- Las anclas del sitio anterior (`/#servicios`, `/#ivso`…) no llegan al servidor: las redirige `assets/js/site.js`.

## 4. Migración desde vitalis-web (GitHub Pages)

Cuando sevidapsicosocial.com esté en línea:

1. Cree la etiqueta `v-vitalis-final` en `vitalis-web` para poder volver atrás.
2. Reemplace el `index.html` de `vitalis-web` por una página puente con
   `<link rel="canonical" href="https://sevidapsicosocial.com/">` y `<meta http-equiv="refresh" content="0; url=https://sevidapsicosocial.com/">`.
3. Haga lo mismo con cada `blog/<slug>.html`, apuntando a `https://sevidapsicosocial.com/blog/<slug>/`.

## 5. Después de publicar

- Google Search Console: alta del dominio y envío de `sitemap.xml`.
- Probar Open Graph pegando el enlace en LinkedIn y WhatsApp.
- Validar el JSON-LD con la Prueba de resultados enriquecidos de Google.

## Alternativa: Cloudflare Pages

`public/_redirects` y `public/_headers` se mantienen por si se vuelve a Cloudflare Pages (build command vacío, salida `public`).
