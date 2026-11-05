/* SéVida™ — navegación del sitio */
(function () {
  'use strict';
  var menu = document.getElementById('menu');
  var boton = document.querySelector('.hamburguesa');
  if (boton && menu) {
    boton.addEventListener('click', function () {
      var abierto = menu.classList.toggle('abierto');
      boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    });
  }
  document.querySelectorAll('.menu button[aria-haspopup]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var li = b.parentElement;
      var abierto = !li.classList.contains('abierto');
      document.querySelectorAll('.menu li.abierto').forEach(function (x) { x.classList.remove('abierto'); x.querySelector('button').setAttribute('aria-expanded', 'false'); });
      if (abierto) { li.classList.add('abierto'); b.setAttribute('aria-expanded', 'true'); }
    });
  });
  document.addEventListener('click', function () {
    document.querySelectorAll('.menu li.abierto').forEach(function (x) { x.classList.remove('abierto'); x.querySelector('button').setAttribute('aria-expanded', 'false'); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') document.querySelectorAll('.menu li.abierto').forEach(function (x) { x.classList.remove('abierto'); });
  });

  /* Redirección de enlaces antiguos con ancla (sitio de una página) a las páginas nuevas */
  var mapa = {
    '#servicios': '/servicios/', '#planes': '/servicios/', '#evolucion': '/servicios/recalibra-empresarial/',
    '#reset': '/servicios/recalibra-empresarial/', '#metodologia': '/metodo/', '#nosotros': '/nosotros/',
    '#talleres': '/servicios/talleres/', '#pve': '/servicios/vigilancia-epidemiologica/',
    '#coaching': '/servicios/coaching-lideres/', '#sst': '/servicios/acompanamiento-sst/',
    '#acompanamiento': '/servicios/acompanamiento-sst/', '#bateria': '/servicios/bateria-riesgo-psicosocial/',
    '#normativa': '/normativa/', '#ivso': '/ismo/', '#ismo': '/ismo/', '#contacto': '/contacto/',
    '#privacidad': '/politica-de-datos/', '#politica': '/politica-de-datos/', '#blog': '/blog/', '#faq': '/contacto/#preguntas'
  };
  if (location.pathname === '/' && location.hash && mapa[location.hash.toLowerCase()]) {
    location.replace(mapa[location.hash.toLowerCase()]);
  }
  var anio = document.getElementById('anio');
  if (anio) anio.textContent = new Date().getFullYear();
})();
