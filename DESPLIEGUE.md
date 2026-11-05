# Despliegue de sevida.com.co

## 1. Subir el repositorio a GitHub (una sola vez)

1. En GitHub, cree un repositorio **vacío** llamado `sevida-web` (sin README ni licencia).
2. Desde esta carpeta:
   ```
   git remote add origin https://github.com/josedavidalomia-maker/sevida-web.git
   git push -u origin main
   ```
   Con GitHub Desktop: *File → Add local repository* → elija esta carpeta → *Publish repository*.

## 2. Cloudflare Pages

1. *Workers & Pages → Create → Pages → Connect to Git* → `sevida-web`.
2. Build command: *(vacío)* · Build output directory: `public`.
3. Pruebe la URL de vista previa `*.pages.dev`: las 25 rutas, la 404, el ISMO completo y un envío de contacto.
4. *Custom domains* → `sevida.com.co` y `www.sevida.com.co`.

`public/_redirects` maneja las rutas viejas dentro del mismo dominio (`/blog/<slug>.html` → `/blog/<slug>/`, `/ivso` → `/ismo/`).
Las anclas del sitio anterior (`/#servicios`, `/#ivso`…) no llegan al servidor: las redirige `assets/js/site.js`.

## 3. Dominios secundarios (Bulk Redirects)

`_redirects` no admite reglas por dominio. Para `sevida.co`, `sevidapsicosocial.com` y similares:
*Cloudflare → Bulk Redirects → Create list*:

| Origen | Destino | Estado |
| --- | --- | --- |
| `sevida.co/*` | `https://sevida.com.co/${1}` | 301 |
| `www.sevida.co/*` | `https://sevida.com.co/${1}` | 301 |

Active «Preserve query string» y «Subpath matching».

## 4. Migración desde vitalis-web (GitHub Pages)

Cuando sevida.com.co esté en línea:

1. Cree la etiqueta `v-vitalis-final` en `vitalis-web` para poder volver atrás.
2. Reemplace el `index.html` de `vitalis-web` por una página puente con
   `<link rel="canonical" href="https://sevida.com.co/">` y `<meta http-equiv="refresh" content="0; url=https://sevida.com.co/">`.
3. Haga lo mismo con cada `blog/<slug>.html`, apuntando a `https://sevida.com.co/blog/<slug>/`.

## 5. Después de publicar

- Google Search Console: alta del dominio y envío de `sitemap.xml`.
- Probar Open Graph pegando el enlace en LinkedIn y WhatsApp.
- Validar el JSON-LD con la Prueba de resultados enriquecidos de Google.
