/* SéVida™ — formulario de contacto (FormSubmit) */
(function () {
  'use strict';
  /* CONFIGURACIÓN DEL FORMULARIO (FormSubmit)
     Hoy los mensajes llegan a CORREO_TEMPORAL. Cuando exista el buzón de SéVida:
     1) cambie CORREO_ACTIVO = CORREO_SEVIDA (aquí y en el otro archivo: contacto.js / ismo.js);
     2) envíe un mensaje de prueba y active el formulario con el enlace que FormSubmit manda a ese buzón;
     3) opcional: pegue en FORMSUBMIT_TOKEN la cadena aleatoria que asigna FormSubmit, para no exponer el correo. */
  var CORREO_TEMPORAL = 'josedavidalomia@gmail.com';
  var CORREO_SEVIDA = 'contacto@sevidapsicosocial.com';
  var CORREO_ACTIVO = CORREO_TEMPORAL;
  var FORMSUBMIT_TOKEN = '';
  var ENDPOINT = 'https://formsubmit.co/ajax/' + (FORMSUBMIT_TOKEN || CORREO_ACTIVO);
  var WHATSAPP = 'https://wa.me/573168768220';

  var form = document.getElementById('form-contacto');
  if (!form) return;
  var estado = document.getElementById('estado-envio');

  function marcar(campo, invalido) {
    var c = campo.closest('.campo'); if (c) c.classList.toggle('invalido', invalido);
  }
  function mostrarError(msg) {
    estado.className = 'estado-envio falla'; estado.textContent = msg;
  }
  function valido() {
    var ok = true;
    form.querySelectorAll('[required]').forEach(function (el) {
      var malo = el.type === 'checkbox' ? !el.checked : !el.value.trim();
      if (el.type === 'email' && el.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value)) malo = true;
      marcar(el, malo); if (malo) ok = false;
    });
    return ok;
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var autorizacion = form.querySelector('#autorizacion');
    if (!autorizacion.checked) {
      marcar(autorizacion, true); autorizacion.focus();
      mostrarError('Para enviar el formulario debe autorizar el tratamiento de sus datos.');
      return;
    }
    if (!valido()) { mostrarError('Revise los campos marcados.'); return; }
    if (form.querySelector('[name="_honey"]').value) return; /* campo trampa contra spam */
    var boton = form.querySelector('button[type="submit"]');
    boton.disabled = true; boton.textContent = 'Enviando…';
    var datos = Object.fromEntries(new FormData(form).entries());
    datos._subject = 'Nuevo mensaje desde sevidapsicosocial.com — ' + (datos.empresa || '');
    datos._template = 'table';
    datos.fecha_autorizacion = new Date().toISOString();
    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(datos) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function () {
        form.reset(); estado.className = 'estado-envio ok';
        estado.textContent = 'Mensaje enviado. Le respondemos en un máximo de 24 horas hábiles.';
      })
      .catch(function () {
        mostrarError('No pudimos enviar el mensaje. Escríbanos por WhatsApp: ' + WHATSAPP.replace('https://wa.me/', '+'));
      })
      .finally(function () { boton.disabled = false; boton.textContent = 'Enviar mensaje'; });
  });
  form.querySelectorAll('input,select,textarea').forEach(function (el) {
    el.addEventListener('change', function () { marcar(el, false); });
  });
})();
