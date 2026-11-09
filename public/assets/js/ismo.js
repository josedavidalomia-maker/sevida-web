/* ISMO — Índice SéVida de Madurez Organizacional
   Fórmula: ISMO = DIMS × 0,80 + LEGAL × 0,20 (0 a 100).
   Sin semáforo rojo/amarillo/verde a propósito: evita el sesgo de deseabilidad social en las respuestas. */
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

  var DIMS = [
    { id: 'negocio', n: 'Indicadores de negocio', w: 0.20, qs: [
      { t: 'La rotación voluntaria de personal en el último año:', ops: ['Disminuyó o se mantiene estable (menos del 10 % anual)', 'Aumentó moderadamente (entre 10 % y 25 % anual)', 'Aumentó de forma preocupante (más del 25 % anual)'] },
      { t: 'Las incapacidades médicas asociadas a estrés, ansiedad u otros problemas de salud mental:', ops: ['No se presentan o son escasas y aisladas', 'Han aumentado ocasionalmente en el último año', 'Han aumentado de forma sistemática; es un patrón visible'] },
      { t: '¿Hay cargos críticos con alta dificultad de retención o reposición?', ops: ['No; la mayoría de cargos son estables', 'En algunos cargos puntuales o especializados', 'Sí; es un problema recurrente que afecta la operación'] },
      { t: 'En el último año se han presentado conflictos laborales formales (quejas, derechos de petición, demandas):', ops: ['No se han presentado', 'Uno o dos casos aislados y resueltos', 'Con frecuencia, o hay casos activos sin resolver'] }
    ]},
    { id: 'psico', n: 'Factores de riesgo psicosocial', w: 0.25, qs: [
      { t: 'La carga laboral y los ritmos de trabajo son:', ops: ['Manejables; hay autonomía y tiempos de recuperación', 'Variables; altos en temporadas, con momentos de equilibrio', 'Permanentemente elevados; jornadas extendidas y presión constante'] },
      { t: 'La claridad de roles, funciones y expectativas de cada cargo es:', ops: ['Alta; cada persona conoce sus responsabilidades y metas', 'Moderada; hay ambigüedades o los roles cambian con frecuencia', 'Baja; roles confusos y funciones que se cruzan'] },
      { t: 'El control y la autonomía que tienen las personas sobre su trabajo es:', ops: ['Alto; deciden cómo organizar y ejecutar su trabajo', 'Moderado; con restricciones razonables según el cargo', 'Bajo; todo está microcontrolado y hay poca participación'] },
      { t: 'Las relaciones interpersonales y el apoyo entre compañeros son:', ops: ['Buenas; colaboración, respeto y apoyo mutuo', 'Regulares; tensiones puntuales que se manejan', 'Malas; conflictos frecuentes, rumores o desconfianza'] }
    ]},
    { id: 'mental', n: 'Salud mental laboral', w: 0.15, qs: [
      { t: '¿Con qué frecuencia se observan señales de agotamiento, desmotivación o desconexión?', ops: ['Rara vez', 'Ocasionalmente, en momentos de alta carga', 'Con frecuencia; se nota en la actitud y la productividad'] },
      { t: '¿La empresa tiene un programa estructurado de salud mental?', ops: ['Sí, con actividades regulares, seguimiento, indicadores y presupuesto', 'Hay acciones esporádicas sin plan formal', 'No existe'] },
      { t: 'Cuando una persona muestra señales de malestar emocional, la organización:', ops: ['Tiene un protocolo claro y los líderes saben cómo actuar', 'Atiende el caso, pero sin procedimiento formal', 'No tiene cómo identificarlo ni atenderlo a tiempo'] }
    ]},
    { id: 'lid', n: 'Liderazgo y cultura', w: 0.15, qs: [
      { t: 'El estilo de liderazgo predominante genera en los equipos:', ops: ['Confianza, desarrollo y buen desempeño sostenido', 'Resultados aceptables, con alta presión y tensión interna', 'Desmotivación, rotación o conflictos frecuentes'] },
      { t: '¿Los líderes están formados para gestionar el bienestar de sus equipos?', ops: ['Sí, tienen formación específica y la aplican', 'Algunos lo hacen por intuición, sin formación', 'No; el tema no está en la agenda de liderazgo'] },
      { t: 'La comunicación interna y la transparencia en las decisiones son:', ops: ['Altas; la gente entiende el rumbo y su papel en él', 'Moderadas; la información no siempre llega a tiempo', 'Bajas; incertidumbre, rumores y falta de dirección'] }
    ]},
    { id: 'biene', n: 'Bienestar organizacional', w: 0.10, qs: [
      { t: 'El equilibrio entre exigencias laborales y vida personal es:', ops: ['Saludable; hay políticas concretas de desconexión y flexibilidad', 'Parcial; depende del área o del jefe', 'Inexistente; se premia la disponibilidad permanente'] },
      { t: 'El reconocimiento del trabajo bien hecho es:', ops: ['Sistemático; hay mecanismos formales', 'Informal; depende de cada jefe', 'Escaso; la gente siente que su trabajo no se valora'] }
    ]},
    { id: 'ind', n: 'Indicadores operativos de SST', w: 0.15, qs: [
      { t: 'La accidentalidad laboral en el último año:', ops: ['Disminuyó o se mantiene en niveles mínimos', 'Estable, con incidentes menores', 'Aumentó o hay accidentes recurrentes sin intervención'] },
      { t: 'El ausentismo laboral (sin contar vacaciones) en el último año:', ops: ['Está controlado (menos del 3 % mensual)', 'En rango medio (entre 3 % y 6 % mensual)', 'Es elevado (más del 6 % mensual) o aumentó notablemente'] },
      { t: 'La productividad del equipo en los últimos 6 meses:', ops: ['Mejoró o se mantiene en lo esperado', 'Se mantiene, con áreas de bajo desempeño visible', 'Disminuyó; hay señales claras de desmotivación'] }
    ]}
  ];
  var LEGAL = { id: 'legal', n: 'Cumplimiento legal', qs: [
    { k: 'bateria', t: 'Batería de Riesgo Psicosocial (Resolución 2764 de 2022): última aplicación', ops: ['Hace menos de 2 años, con resultados documentados', 'Hace más de 2 años', 'Nunca se ha aplicado'] },
    { k: 'pve', t: 'Programa de Vigilancia Epidemiológica (PVE) psicosocial', ops: ['Activo, documentado, con indicadores y seguimiento', 'Parcial, sin indicadores ni seguimiento formal', 'No existe'] },
    { k: 'plan', t: 'Plan de intervención del riesgo psicosocial', ops: ['Activo, con responsables, cronograma y presupuesto', 'Existe en papel pero no se ejecuta o está desactualizado', 'No existe'] },
    { k: 'lideres', t: 'Formación de líderes en prevención del riesgo psicosocial', ops: ['Programa implementado con registros', 'Jornadas sueltas, sin continuidad', 'No se ha hecho'] },
    { k: 'comites', t: 'Comité de Convivencia Laboral y COPASST (o vigía)', ops: ['Activos, con reuniones documentadas', 'Conformados, con poca actividad en los últimos 6 meses', 'No existen o no están conformados según la norma'] },
    { k: 'sgsst', t: 'SG-SST según el Decreto 1072 de 2015 y la Resolución 0312 de 2019', ops: ['Implementado, con autoevaluación de estándares mínimos y evidencias', 'En implementación o con brechas en la documentación', 'No implementado'] }
  ]};
  var DESAFIOS = ['Rotación y retención del talento', 'Ausentismo y salud del equipo', 'Estrés y sobrecarga', 'Liderazgo y cultura', 'Cumplimiento legal en SST', 'Clima laboral y conflictos'];
  var NIVELES = [
    { min: 81, n: 'Cultura preventiva', d: 'La gestión del riesgo psicosocial está integrada a la operación. El reto es sostenerla y medir su efecto en el negocio.' },
    { min: 61, n: 'Gestión estratégica', d: 'Hay sistema y seguimiento. Las brechas que quedan son puntuales y conviene cerrarlas con prioridad.' },
    { min: 41, n: 'Gestión estructurada', d: 'Existen las bases, pero hay componentes sin ejecutar o sin medición. El riesgo está identificado a medias.' },
    { min: 21, n: 'Cumplimiento básico', d: 'La organización cumple de forma parcial y reactiva. Los factores de riesgo no se gestionan de manera sistemática.' },
    { min: 0, n: 'Reactivo', d: 'Las obligaciones básicas no están cubiertas y los factores de riesgo no se conocen. El primer paso es medir.' }
  ];
  var PUNTOS = [0, 2, 4]; /* opción 1 = sin riesgo · 2 = parcial · 3 = riesgo */

  var raiz = document.getElementById('ismo');
  if (!raiz) return;
  var pasos = DIMS.concat([LEGAL]);
  var resp = {}, perfil = {}, actual = -1;

  function el(tag, attrs, html) { var e = document.createElement(tag); for (var k in attrs || {}) e.setAttribute(k, attrs[k]); if (html !== undefined) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function pintarInicio() {
    raiz.innerHTML =
      '<p class="ismo-paso-titulo">Paso 1 de ' + (pasos.length + 1) + ' · Datos de la organización</p>' +
      '<div class="ismo-progreso"><span style="width:0%"></span></div>' +
      '<form id="ismo-inicio" class="formulario" novalidate>' +
      '<div class="campo-doble"><div class="campo"><label for="i-empresa">Empresa *</label><input id="i-empresa" name="empresa" required><p class="error">Escriba el nombre de la empresa.</p></div>' +
      '<div class="campo"><label for="i-sector">Sector *</label><select id="i-sector" name="sector" required><option value="">Seleccione…</option><option>Salud</option><option>Manufactura e industria</option><option>Educación</option><option>Comercio</option><option>Servicios profesionales</option><option>Tecnología</option><option>Transporte y logística</option><option>Construcción</option><option>Sector público</option><option>Otro</option></select><p class="error">Seleccione el sector.</p></div></div>' +
      '<div class="campo-doble"><div class="campo"><label for="i-tamano">Número de trabajadores *</label><select id="i-tamano" name="trabajadores" required><option value="">Seleccione…</option><option>1 a 10</option><option>11 a 50</option><option>51 a 200</option><option>201 a 500</option><option>Más de 500</option></select><p class="error">Seleccione un rango.</p></div>' +
      '<div class="campo"><label for="i-ciudad">Ciudad</label><input id="i-ciudad" name="ciudad"></div></div>' +
      '<div class="campo-doble"><div class="campo"><label for="i-nombre">Nombre</label><input id="i-nombre" name="nombre"></div>' +
      '<div class="campo"><label for="i-correo">Correo</label><input id="i-correo" name="correo" type="email"></div></div>' +
      '<div class="campo campo-autorizacion"><input type="checkbox" id="i-autoriza" name="autorizacion_datos" value="Sí" required>' +
      '<label for="i-autoriza" style="font-weight:400;font-family:inherit;color:inherit">Autorizo a SéVida a tratar estos datos para entregarme el resultado y, si lo envío, contactarme sobre él, incluida su transmisión a FormSubmit, conforme a la <a href="/politica-de-datos/" target="_blank" rel="noopener">política de tratamiento de datos</a>.</label></div>' +
      '<p class="error" id="i-autoriza-error">Debe autorizar el tratamiento de datos para continuar.</p>' +
      '<div class="ismo-nav"><span></span><button class="btn btn-primario" type="submit">Iniciar diagnóstico</button></div></form>';
    document.getElementById('ismo-inicio').addEventListener('submit', function (e) {
      e.preventDefault(); var ok = true;
      ['i-empresa', 'i-sector', 'i-tamano'].forEach(function (id) { var x = document.getElementById(id), m = !x.value.trim(); x.closest('.campo').classList.toggle('invalido', m); if (m) ok = false; });
      var a = document.getElementById('i-autoriza'); document.getElementById('i-autoriza-error').style.display = a.checked ? 'none' : 'block';
      if (!a.checked) ok = false;
      if (!ok) return;
      new FormData(e.target).forEach(function (v, k) { perfil[k] = v; });
      actual = 0; pintarPaso();
    });
  }

  function pintarPaso() {
    var d = pasos[actual], total = pasos.length + 1;
    var h = '<p class="ismo-paso-titulo">Paso ' + (actual + 2) + ' de ' + total + ' · ' + esc(d.n) + '</p>' +
      '<div class="ismo-progreso"><span style="width:' + Math.round((actual + 1) / total * 100) + '%"></span></div><h3>' + esc(d.n) + '</h3>';
    d.qs.forEach(function (q, qi) {
      var k = d.id + '_' + qi;
      h += '<fieldset class="pregunta" style="border:0"><legend style="font-weight:600;color:#0D1B2A;margin-bottom:10px">' + esc(q.t) + '</legend>';
      q.ops.forEach(function (o, oi) {
        var sel = resp[k] === oi ? ' elegida' : '';
        h += '<label class="opcion' + sel + '"><input type="radio" name="' + k + '" value="' + oi + '"' + (resp[k] === oi ? ' checked' : '') + '><span>' + esc(o) + '</span></label>';
      });
      h += '</fieldset>';
    });
    if (d.id === 'legal') {
      h += '<fieldset class="pregunta" style="border:0"><legend style="font-weight:600;color:#0D1B2A;margin-bottom:10px">¿Cuál es hoy el principal desafío de personas en su organización? (no suma al índice)</legend>';
      DESAFIOS.forEach(function (o, oi) { h += '<label class="opcion' + (resp.desafio === oi ? ' elegida' : '') + '"><input type="radio" name="desafio" value="' + oi + '"' + (resp.desafio === oi ? ' checked' : '') + '><span>' + esc(o) + '</span></label>'; });
      h += '</fieldset>';
    }
    h += '<p class="error" id="ismo-falta">Responda todas las preguntas de este paso.</p>' +
      '<div class="ismo-nav"><button class="btn btn-secundario" type="button" id="ismo-atras">Atrás</button>' +
      '<button class="btn btn-primario" type="button" id="ismo-siguiente">' + (actual === pasos.length - 1 ? 'Ver resultado' : 'Siguiente') + '</button></div>';
    raiz.innerHTML = h;
    raiz.querySelectorAll('input[type=radio]').forEach(function (r) {
      r.addEventListener('change', function () {
        resp[r.name] = parseInt(r.value, 10);
        raiz.querySelectorAll('input[name="' + r.name + '"]').forEach(function (x) { x.parentElement.classList.toggle('elegida', x.checked); });
      });
    });
    document.getElementById('ismo-atras').onclick = function () { if (actual === 0) pintarInicio(); else { actual--; pintarPaso(); } };
    document.getElementById('ismo-siguiente').onclick = function () {
      var completo = d.qs.every(function (q, qi) { return resp[d.id + '_' + qi] !== undefined; });
      document.getElementById('ismo-falta').style.display = completo ? 'none' : 'block';
      if (!completo) return;
      if (actual === pasos.length - 1) pintarResultado(); else { actual++; pintarPaso(); }
      raiz.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
  }

  function pct(d) {
    var t = 0; d.qs.forEach(function (q, qi) { t += PUNTOS[resp[d.id + '_' + qi]]; });
    return Math.round((1 - t / (d.qs.length * 4)) * 100);
  }
  function legalEstado(k) { var i = LEGAL.qs.map(function (q) { return q.k; }).indexOf(k); return resp['legal_' + i]; }

  function recomendaciones() {
    var r = [], b = legalEstado('bateria'), pve = legalEstado('pve'), plan = legalEstado('plan'), lid = legalEstado('lideres'), com = legalEstado('comites'), sg = legalEstado('sgsst');
    if (b === 2) r.push(['Medir el riesgo psicosocial con la batería oficial', 'Sin medición no hay base para intervenir ni para demostrar cumplimiento. La batería se aplica en físico, con consentimiento informado, e incluye los cuestionarios intralaboral (formas A y B), extralaboral, de estrés y de estilos de afrontamiento.', 'Diagnóstico SéVida', '/servicios/bateria-riesgo-psicosocial/']);
    else if (b === 1) r.push(['Actualizar la medición', 'La última aplicación tiene más de dos años. Si se hizo con instrumentos anteriores a la Resolución 2764 de 2022, también hay que actualizarlos.', 'Diagnóstico SéVida', '/servicios/bateria-riesgo-psicosocial/']);
    if (b !== 2 && pve > 0) r.push(['Poner en marcha el Programa de Vigilancia Epidemiológica', 'Los resultados de la batería necesitan seguimiento continuo con indicadores. Sin el programa, la medición se queda en un informe.', 'PVE psicosocial', '/servicios/vigilancia-epidemiologica/']);
    if (plan === 2 || (b === 0 && plan === 1)) r.push(['Convertir los hallazgos en un plan de intervención', 'El plan define qué se interviene, quién lo hace, cuándo y con qué recursos. Es la evidencia de que la organización actúa sobre lo que midió.', 'Recalibra Empresarial', '/servicios/recalibra-empresarial/']);
    if (lid === 2) r.push(['Formar a los líderes', 'El estilo de liderazgo es uno de los dominios que mide la batería. Formar a quienes dirigen equipos actúa sobre la fuente del riesgo.', 'Escuela de Liderazgo y coaching', '/servicios/talleres/']);
    if (com === 2) r.push(['Conformar los comités', 'El Comité de Convivencia Laboral (Resolución 3461 de 2025) y el COPASST o vigía son obligatorios y deben reunirse con actas.', 'Acompañamiento SST', '/servicios/acompanamiento-sst/']);
    if (sg > 0) r.push(['Cerrar las brechas del SG-SST', 'La autoevaluación de estándares mínimos (7, 21 o 60 según su empresa) indica qué falta y en qué orden resolverlo.', 'Acompañamiento SST Mensual', '/servicios/acompanamiento-sst/']);
    if (resp.negocio_0 === 2 || resp.negocio_1 === 2 || resp.negocio_3 === 2) r.push(['Intervenir los factores que mueven sus indicadores', 'Rotación, incapacidades o conflictos en aumento suelen tener origen en las condiciones de trabajo. Conviene intervenirlas de forma estructurada y medir antes y después.', 'Recalibra Empresarial', '/servicios/recalibra-empresarial/']);
    if (!r.length) r.push(['Sostener y medir', 'La organización muestra un buen nivel. El siguiente paso es sostener el sistema y medir su efecto en los indicadores del negocio.', 'Planes de continuidad', '/servicios/']);
    return r;
  }

  function pintarResultado() {
    var v = 0; DIMS.forEach(function (d) { v += pct(d) * d.w; });
    var lp = pct(LEGAL), ismo = Math.round(v * 0.80 + lp * 0.20);
    var nivel = NIVELES.filter(function (n) { return ismo >= n.min; })[0];
    var h = '<div class="ismo-resultado"><p class="kicker">Resultado de ' + esc(perfil.empresa) + '</p>' +
      '<div class="indice">' + ismo + '<span style="font-size:1.4rem;color:#5B6676"> / 100</span></div>' +
      '<h3 style="margin-top:12px">Nivel de madurez: ' + nivel.n + '</h3><p>' + nivel.d + '</p>' +
      '<h3 style="margin-top:28px">Perfil por dimensión</h3>';
    DIMS.concat([LEGAL]).forEach(function (d) {
      var p = pct(d);
      h += '<div class="barra"><div class="rotulo"><span>' + esc(d.n) + '</span><span>' + p + '</span></div><div class="pista"><span class="valor" style="width:' + p + '%"></span></div></div>';
    });
    h += '<h3 style="margin-top:28px">Qué hacer primero</h3>';
    recomendaciones().forEach(function (r, i) {
      h += '<div class="recomendacion"><strong>' + (i + 1) + '. ' + esc(r[0]) + '</strong><p>' + esc(r[1]) + '</p><p style="margin-top:8px"><a href="' + r[3] + '">' + esc(r[2]) + ' →</a></p></div>';
    });
    if (resp.desafio !== undefined) h += '<p style="margin-top:14px"><strong>Desafío que usted priorizó:</strong> ' + esc(DESAFIOS[resp.desafio]) + '.</p>';
    h += '<p class="meta" style="color:#5B6676">ISMO = 80 % dimensiones organizacionales + 20 % cumplimiento legal. Es una herramienta de orientación: no reemplaza la Batería de Riesgo Psicosocial ni la autoevaluación de estándares mínimos.</p>' +
      '<div class="ismo-nav" style="flex-wrap:wrap"><button class="btn btn-secundario" type="button" id="ismo-imprimir">Imprimir o guardar en PDF</button>' +
      '<button class="btn btn-primario" type="button" id="ismo-enviar">Enviar mi resultado a SéVida y agendar la conversación</button></div><p id="ismo-envio" class="estado-envio"></p></div>';
    raiz.innerHTML = h;
    document.getElementById('ismo-imprimir').onclick = function () { window.print(); };
    document.getElementById('ismo-enviar').onclick = function () {
      var est = document.getElementById('ismo-envio'), btn = this; btn.disabled = true;
      var datos = Object.assign({}, perfil, { _subject: 'Resultado ISMO — ' + perfil.empresa, ismo: ismo, nivel: nivel.n, desafio: resp.desafio !== undefined ? DESAFIOS[resp.desafio] : '', fecha_autorizacion: new Date().toISOString(), _honey: '' });
      DIMS.concat([LEGAL]).forEach(function (d) { datos['dim_' + d.id] = pct(d); });
      fetch('https://formsubmit.co/ajax/' + (FORMSUBMIT_TOKEN || CORREO_ACTIVO), { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(datos) })
        .then(function (r) { if (!r.ok) throw 0; est.className = 'estado-envio ok'; est.textContent = 'Recibimos su resultado. Le escribiremos para agendar la conversación diagnóstica de 30 minutos.'; })
        .catch(function () { est.className = 'estado-envio falla'; est.innerHTML = 'No se pudo enviar. Escríbanos por <a href="https://wa.me/573168768220">WhatsApp</a> con su resultado: ' + ismo + ' / 100.'; btn.disabled = false; });
    };
    raiz.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  pintarInicio();
})();
