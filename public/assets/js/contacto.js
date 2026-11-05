/* SéVida™ — formulario de contacto (FormSubmit) */
(function () {
  'use strict';
  /* CONFIGURACIÓN: reemplace por el token que FormSubmit envía a contacto@sevida.com.co al activar el formulario */
  var FORMSUBMIT_TOKEN = 'REEMPLAZAR_TOKEN_FORMSUBMIT';
  var ENDPOINT = 'https://formsubmit.co/ajax/' + FORMSUBMIT_TOKEN;
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
    datos._subject = 'Nuevo mensaje desde sevida.com.co — ' + (datos.empresa || '');
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
