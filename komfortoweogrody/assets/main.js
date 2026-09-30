/* Komfortowe Ogrody – skrypty strony */
(function(){
  'use strict';
  document.documentElement.classList.remove('no-js');

  // Zdjęcia są hostowane na serwerze kreatora Zyro/Hostinger; jeśli przestaną tam działać,
  // strona sięga po ich kopię z Internet Archive.
  function archiveFallback(img){
    img.addEventListener('error', function onErr(){
      img.removeEventListener('error', onErr);
      var src = img.getAttribute('src');
      img.removeAttribute('srcset');
      img.src = 'https://web.archive.org/web/2025im_/' + src;
    });
  }
  document.querySelectorAll('img[src^="https://assets.zyrosite.com/"]').forEach(archiveFallback);

  // Nagłówek: cień po przewinięciu i menu mobilne
  var header = document.querySelector('.header');
  if (header) {
    var burger = header.querySelector('.burger');
    var onScroll = function(){ header.classList.toggle('scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, {passive: true});
    burger.addEventListener('click', function(){
      var open = header.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      burger.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
    });
    header.querySelectorAll('.nav a').forEach(function(a){
      a.addEventListener('click', function(){ header.classList.remove('open'); burger.setAttribute('aria-expanded', false); });
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && header.classList.contains('open')) { header.classList.remove('open'); burger.setAttribute('aria-expanded', false); burger.focus(); }
    });
  }

  // Animacja pojawiania się sekcji
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, {threshold: 0.12, rootMargin: '0px 0px -40px 0px'});
    reveals.forEach(function(el){ io.observe(el); });
  } else {
    reveals.forEach(function(el){ el.classList.add('in'); });
  }

  // Lata doświadczenia i bieżący rok liczone automatycznie
  var year = new Date().getFullYear();
  document.querySelectorAll('[data-years-since]').forEach(function(el){
    el.textContent = (year - parseInt(el.getAttribute('data-years-since'), 10)) + '+';
  });
  document.querySelectorAll('[data-year]').forEach(function(el){ el.textContent = year; });

  // Animowane liczniki
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var co = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (!en.isIntersecting) return;
        co.unobserve(en.target);
        var el = en.target, end = parseInt(el.textContent, 10), suffix = el.textContent.replace(/[0-9]/g, ''), t0 = null;
        if (isNaN(end)) return;
        (function step(t){
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / 1200, 1);
          el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suffix;
          if (p < 1) requestAnimationFrame(step);
        })(performance.now());
      });
    }, {threshold: 0.6});
    counters.forEach(function(el){ co.observe(el); });
  }

  // Status „otwarte teraz” wg godzin pracy (czas polski): pn–sob 7:00–18:00
  var status = document.querySelectorAll('.open-status');
  if (status.length) {
    try {
      var parts = new Intl.DateTimeFormat('en-GB', {timeZone: 'Europe/Warsaw', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false}).formatToParts(new Date());
      var get = function(type){ return (parts.filter(function(p){ return p.type === type; })[0] || {}).value; };
      var day = get('weekday'), minutes = parseInt(get('hour'), 10) % 24 * 60 + parseInt(get('minute'), 10);
      var open = day !== 'Sun' && minutes >= 7 * 60 && minutes < 18 * 60;
      status.forEach(function(el){
        el.classList.add(open ? 'is-open' : 'is-closed');
        el.textContent = open ? 'Teraz otwarte' : 'Teraz zamknięte';
      });
    } catch (e) {}
  }

  // Suwak „przed / po”
  function initBA(ba){
    var range = ba.querySelector('.ba__range');
    if (!range || ba.dataset.ready) return;
    ba.dataset.ready = '1';
    var set = function(v){ ba.style.setProperty('--pos', v + '%'); };
    range.addEventListener('input', function(){ set(range.value); });
    set(range.value);
    // Przeciąganie myszą i palcem; pionowy ruch palca nadal przewija stronę (touch-action: pan-y)
    var dragging = false;
    var fromEvent = function(e){
      var r = ba.getBoundingClientRect();
      var v = Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100));
      range.value = v; set(v);
    };
    ba.addEventListener('pointerdown', function(e){
      if (e.button !== undefined && e.button !== 0) return;
      dragging = true; fromEvent(e);
      if (e.pointerType === 'mouse') { ba.setPointerCapture(e.pointerId); e.preventDefault(); }
    });
    ba.addEventListener('pointermove', function(e){ if (dragging) fromEvent(e); });
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(function(t){ ba.addEventListener(t, function(){ dragging = false; }); });
  }
  document.querySelectorAll('.ba').forEach(initBA);

  // Galeria: powiększony podgląd suwaka
  var modal = document.querySelector('.modal');
  if (modal) {
    var items = Array.prototype.slice.call(document.querySelectorAll('.gallery-item'));
    var inner = modal.querySelector('.modal__inner'), count = modal.querySelector('.modal__count');
    var current = 0, lastFocus = null;
    var show = function(i){
      current = (i + items.length) % items.length;
      var src = items[current].querySelector('.ba');
      var clone = src.cloneNode(true);
      delete clone.dataset.ready;
      clone.querySelectorAll('img').forEach(function(img){
        var big = img.getAttribute('data-full');
        img.removeAttribute('srcset'); img.removeAttribute('sizes'); img.loading = 'eager';
        if (big) img.src = big;
        archiveFallback(img);
      });
      inner.innerHTML = '';
      inner.appendChild(clone);
      initBA(clone);
      count.textContent = 'Realizacja ' + (current + 1) + ' z ' + items.length;
    };
    var close = function(){ modal.hidden = true; document.body.style.overflow = ''; inner.innerHTML = ''; if (lastFocus) lastFocus.focus(); };
    items.forEach(function(item, i){
      item.querySelector('.zoom-btn').addEventListener('click', function(){
        lastFocus = this; show(i); modal.hidden = false; document.body.style.overflow = 'hidden';
        modal.querySelector('.modal__close').focus();
      });
    });
    modal.querySelector('.modal__close').addEventListener('click', close);
    modal.querySelector('.modal__prev').addEventListener('click', function(){ show(current - 1); });
    modal.querySelector('.modal__next').addEventListener('click', function(){ show(current + 1); });
    modal.addEventListener('click', function(e){ if (e.target === modal) close(); });
    document.addEventListener('keydown', function(e){
      if (modal.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'PageUp') show(current - 1);
      if (e.key === 'PageDown') show(current + 1);
    });
  }

  // Formularz kontaktowy: strona jest statyczna, więc otwiera program pocztowy z gotową wiadomością
  var form = document.getElementById('contact-form');
  if (form) {
    var note = form.querySelector('.form__note');
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var name = form.elements.name.value.trim(), email = form.elements.email.value.trim(),
          phone = form.elements.phone.value.trim(), msg = form.elements.message.value.trim(), ok = true;
      [[form.elements.email, /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)], [form.elements.message, msg.length > 0]].forEach(function(p){
        p[0].classList.toggle('invalid', !p[1]);
        p[0].setAttribute('aria-invalid', !p[1]);
        if (!p[1]) ok = false;
      });
      if (!ok) { note.textContent = 'Uzupełnij poprawnie adres e-mail i treść wiadomości.'; return; }
      var body = msg + '\n\n—\n' + (name ? name + '\n' : '') + email + (phone ? '\ntel. ' + phone : '');
      window.location.href = 'mailto:kontakt@komfortoweogrody.pl?subject=' +
        encodeURIComponent('Zapytanie ze strony' + (name ? ' – ' + name : '')) + '&body=' + encodeURIComponent(body);
      note.textContent = 'Dziękujemy za kontakt! Otwieramy Twój program pocztowy z gotową wiadomością.';
    });
  }

  // Na podglądzie w github.io strona leży obok aplikacji Król Kufla, której service worker (cache-first)
  // obejmuje cały serwis. Własny, pusty worker o węższym zasięgu sprawia, że ta strona zawsze idzie z sieci.
  if ('serviceWorker' in navigator && location.hostname.indexOf('github.io') !== -1) {
    var root = new URL('../', document.currentScript ? document.currentScript.src : location.href);
    navigator.serviceWorker.register(new URL('sw.js', root).href, {scope: root.pathname}).catch(function(){});
  }
})();
