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
      if (form.elements.firma && form.elements.firma.value) { note.textContent = 'Dziękujemy za kontakt!'; return; }
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

  /* =====================================================================
     LEVEL UP – efekty i interakcje
     ===================================================================== */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var desktop = window.matchMedia('(min-width: 881px)');

  // Pasek postępu, chowanie nagłówka, przycisk „do góry”, pływający telefon
  var progress = document.createElement('div');
  progress.className = 'progress';
  document.body.appendChild(progress);
  var totop = document.createElement('button');
  totop.className = 'totop'; totop.type = 'button'; totop.setAttribute('aria-label', 'Wróć na górę strony');
  totop.innerHTML = '<svg class="ring" viewBox="0 0 46 46" aria-hidden="true"><circle cx="23" cy="23" r="21"/></svg><svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m18 15-6-6-6 6"/></svg>';
  document.body.appendChild(totop);
  totop.addEventListener('click', function(){ window.scrollTo({top: 0, behavior: reduce ? 'auto' : 'smooth'}); });
  var ringCircle = totop.querySelector('circle');
  var fab = document.querySelector('.fab');
  var lastY = window.scrollY, ticking = false;
  function onScrollFx(){
    var y = window.scrollY, max = document.documentElement.scrollHeight - innerHeight, p = max > 0 ? y / max : 0;
    progress.style.transform = 'scaleX(' + p + ')';
    ringCircle.style.strokeDashoffset = 132 - 132 * p;
    totop.classList.toggle('show', y > 700);
    if (fab) fab.classList.toggle('show', y > 500);
    if (header && !header.classList.contains('open')) header.classList.toggle('hide', y > 320 && y > lastY + 4);
    if (header && y < lastY - 4) header.classList.remove('hide');
    lastY = y; ticking = false;
    parallax(); processLine(); revealPending();
  }
  window.addEventListener('scroll', function(){ if (!ticking) { ticking = true; requestAnimationFrame(onScrollFx); } }, {passive: true});

  // Przesuwany wskaźnik w menu (komputer)
  var navUl = document.querySelector('.nav ul');
  if (navUl) {
    var ind = document.createElement('span');
    ind.className = 'nav__ind'; navUl.appendChild(ind);
    var cur = navUl.querySelector('[aria-current="page"]');
    var moveInd = function(a){
      if (!a || !desktop.matches) { ind.style.opacity = 0; return; }
      ind.style.opacity = 1; ind.style.width = a.offsetWidth + 'px';
      ind.style.transform = 'translateX(' + a.parentElement.offsetLeft + 'px)';
    };
    var syncMode = function(){ document.documentElement.classList.toggle('no-ind', !desktop.matches); moveInd(cur); };
    navUl.querySelectorAll('a').forEach(function(a){ a.addEventListener('mouseenter', function(){ moveInd(a); }); });
    navUl.addEventListener('mouseleave', function(){ moveInd(cur); });
    window.addEventListener('resize', syncMode);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(syncMode);
    syncMode();
  }

  // Fala po kliknięciu przycisku
  document.addEventListener('pointerdown', function(e){
    var btn = e.target.closest && e.target.closest('.btn');
    if (!btn || reduce) return;
    var r = btn.getBoundingClientRect(), size = Math.max(r.width, r.height) * 2.2, s = document.createElement('span');
    s.className = 'ripple';
    s.style.width = s.style.height = size + 'px';
    s.style.left = (e.clientX - r.left - size / 2) + 'px';
    s.style.top = (e.clientY - r.top - size / 2) + 'px';
    btn.appendChild(s);
    setTimeout(function(){ s.remove(); }, 700);
  });

  if (finePointer && !reduce) {
    // Magnetyczne przyciski
    document.querySelectorAll('.btn--primary, .btn--lime, .btn--white, .fab').forEach(function(el){
      el.classList.add('magnetic');
      el.addEventListener('mousemove', function(e){
        var r = el.getBoundingClientRect();
        el.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.22) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.3) + 'px)';
      });
      el.addEventListener('mouseleave', function(){ el.style.transform = ''; });
    });
    // Karty 3D z podświetleniem za kursorem
    document.querySelectorAll('.tilt').forEach(function(el){
      el.addEventListener('mousemove', function(e){
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        el.style.transform = 'perspective(900px) rotateX(' + ((0.5 - y) * 7) + 'deg) rotateY(' + ((x - 0.5) * 9) + 'deg) translateY(-6px)';
        el.style.setProperty('--mx', x * 100 + '%'); el.style.setProperty('--my', y * 100 + '%');
      });
      el.addEventListener('mouseleave', function(){ el.style.transform = ''; });
    });
  }
  document.querySelectorAll('.spot').forEach(function(el){
    el.addEventListener('pointermove', function(e){
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px'); el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  // Paralaksa tła w hero
  var par = document.querySelector('[data-parallax]');
  function parallax(){
    if (!par || reduce) return;
    var y = window.scrollY;
    if (y < innerHeight * 1.2) par.style.transform = 'translate3d(0,' + (y * 0.35) + 'px,0) scale(1.08)';
  }

  // Kaskadowe pojawianie się elementów + kurtyny na zdjęciach + podkreślenia
  document.querySelectorAll('[data-stagger]').forEach(function(g){
    Array.prototype.forEach.call(g.children, function(c, i){ c.style.setProperty('--d', i); });
  });
  var fx = document.querySelectorAll('[data-stagger], .img-reveal, .mark, .vine, .area__map');
  if ('IntersectionObserver' in window && !reduce) {
    var fio = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add('in'); fio.unobserve(en.target); } });
    }, {threshold: 0.15});
    fx.forEach(function(el){ fio.observe(el); });
  } else fx.forEach(function(el){ el.classList.add('in'); });

  // Zabezpieczenie: przy bardzo szybkim przewijaniu obserwator może „przeskoczyć” element –
  // wtedy odsłaniamy wszystko, co jest już nad dolną krawędzią ekranu.
  function revealPending(){
    document.querySelectorAll('.reveal:not(.in), [data-stagger]:not(.in), .img-reveal:not(.in), .mark:not(.in), .vine:not(.in)').forEach(function(el){
      if (el.getBoundingClientRect().top < innerHeight * 0.92) el.classList.add('in');
    });
  }
  window.addEventListener('resize', revealPending);
  window.addEventListener('load', revealPending);

  // Oś „Jak pracujemy” rysowana przewijaniem
  var proc = document.querySelector('.process');
  var steps = proc ? proc.querySelectorAll('.step') : [];
  function processLine(){
    if (!proc) return;
    var r = proc.getBoundingClientRect(), vh = innerHeight;
    var p = Math.max(0, Math.min(1, (vh * 0.75 - r.top) / (r.height + vh * 0.25)));
    if (reduce) p = 1;
    proc.style.setProperty('--p', p);
    steps.forEach(function(s, i){ s.classList.toggle('on', p >= (i + 0.35) / steps.length || p >= 0.98); });
  }
  onScrollFx();

  // Maszyna do pisania: rotujące czasowniki w hero
  var rot = document.querySelector('[data-rotate]');
  if (rot && !reduce) {
    var words = JSON.parse(rot.getAttribute('data-rotate')), wi = 0, ci = words[0].length, del = false;
    (function tick(){
      var w = words[wi];
      if (!del) { ci++; if (ci > w.length) { del = true; return setTimeout(tick, 1900); } }
      else { ci--; if (ci === 0) { del = false; wi = (wi + 1) % words.length; } }
      rot.textContent = words[wi].slice(0, ci);
      setTimeout(tick, del ? 45 : 85);
    })();
  }

  // Opadające liście w hero (canvas, zatrzymywane poza ekranem)
  var cv = document.querySelector('.leaves');
  if (cv && !reduce && cv.getContext) {
    var ctx = cv.getContext('2d'), leaves = [], running = false, W = 0, H = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
    var colors = ['rgba(84,191,63,.75)', 'rgba(140,210,100,.6)', 'rgba(40,115,25,.7)', 'rgba(200,230,150,.55)'];
    var resize = function(){ W = cv.offsetWidth; H = cv.offsetHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    var spawn = function(top){ return {x: Math.random() * W, y: top ? -20 : Math.random() * H, s: 6 + Math.random() * 10, vy: .35 + Math.random() * .7, sw: Math.random() * 6.28, sp: .008 + Math.random() * .014, r: Math.random() * 6.28, vr: (Math.random() - .5) * .03, c: colors[(Math.random() * colors.length) | 0]}; };
    resize(); window.addEventListener('resize', resize);
    var n = innerWidth < 700 ? 10 : 22;
    for (var li = 0; li < n; li++) leaves.push(spawn(false));
    var draw = function(){
      if (!running) return;
      ctx.clearRect(0, 0, W, H);
      leaves.forEach(function(l, i){
        l.sw += l.sp; l.y += l.vy; l.x += Math.sin(l.sw) * .7; l.r += l.vr;
        if (l.y > H + 20) leaves[i] = spawn(true);
        ctx.save(); ctx.translate(l.x, l.y); ctx.rotate(l.r); ctx.fillStyle = l.c;
        ctx.beginPath(); ctx.moveTo(0, -l.s); ctx.quadraticCurveTo(l.s * .8, 0, 0, l.s); ctx.quadraticCurveTo(-l.s * .8, 0, 0, -l.s); ctx.fill();
        ctx.restore();
      });
      requestAnimationFrame(draw);
    };
    new IntersectionObserver(function(en){ running = en[0].isIntersecting && !document.hidden; if (running) requestAnimationFrame(draw); }).observe(cv);
  }

  // Suwak przed/po sam pokazuje, że da się go przesuwać
  if ('IntersectionObserver' in window && !reduce) {
    var pio = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (!en.isIntersecting) return;
        pio.unobserve(en.target);
        var ba = en.target, range = ba.querySelector('.ba__range'), t0 = null;
        ba.addEventListener('pointerdown', function(){ ba.classList.add('touched'); }, {once: true});
        setTimeout(function(){
          (function anim(t){
            if (ba.classList.contains('touched')) return;
            if (!t0) t0 = t;
            var k = Math.min((t - t0) / 1800, 1), v = 50 + Math.sin(k * Math.PI * 2) * 22 * (1 - k * .2);
            if (k >= 1) v = 50;
            range.value = v; ba.style.setProperty('--pos', v + '%');
            if (k < 1) requestAnimationFrame(anim);
          })(performance.now());
        }, 400);
      });
    }, {threshold: 0.6});
    document.querySelectorAll('main .ba').forEach(function(b){ pio.observe(b); });
  }

  // FAQ: płynne rozwijanie
  document.querySelectorAll('.faq details').forEach(function(d){
    var sum = d.querySelector('summary'), ans = d.querySelector('.ans');
    sum.addEventListener('click', function(e){
      if (reduce || !ans.animate) return;
      e.preventDefault();
      if (d.open) {
        var h = ans.offsetHeight;
        ans.animate([{height: h + 'px', opacity: 1}, {height: '0px', opacity: 0}], {duration: 320, easing: 'ease'}).onfinish = function(){ d.open = false; };
      } else {
        d.open = true;
        var h2 = ans.offsetHeight;
        ans.animate([{height: '0px', opacity: 0}, {height: h2 + 'px', opacity: 1}], {duration: 380, easing: 'cubic-bezier(.2,.7,.2,1)'});
      }
    });
  });

  // Kopiowanie telefonu / e-maila z komunikatem
  var toast;
  function showToast(msg){
    if (!toast) {
      toast = document.createElement('div'); toast.className = 'toast'; toast.setAttribute('role', 'status');
      document.body.appendChild(toast);
    }
    toast.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>' + msg;
    toast.classList.add('show'); clearTimeout(toast._t);
    toast._t = setTimeout(function(){ toast.classList.remove('show'); }, 2200);
  }
  document.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click', function(e){
      e.preventDefault(); e.stopPropagation();
      var text = b.getAttribute('data-copy');
      var done = function(){ showToast('Skopiowano: ' + text); };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, done); else done();
    });
  });

  // Formularz: potrząśnięcie przy błędzie, deszcz liści po wysłaniu
  if (form) {
    form.addEventListener('submit', function(){
      var bad = form.querySelectorAll('.invalid');
      if (bad.length) { form.classList.remove('shake'); void form.offsetWidth; form.classList.add('shake'); return; }
      if (reduce) return;
      var r = form.querySelector('button[type=submit]').getBoundingClientRect();
      for (var i = 0; i < 28; i++) {
        var leaf = document.createElement('span');
        leaf.className = 'burst';
        leaf.style.left = (r.left + r.width / 2) + 'px'; leaf.style.top = (r.top + r.height / 2) + 'px';
        leaf.style.background = ['#54bf3f', '#287319', '#9bd97f', '#f5b301'][i % 4];
        document.body.appendChild(leaf);
        var a = Math.random() * Math.PI * 2, dist = 80 + Math.random() * 160;
        leaf.animate([
          {transform: 'translate(-50%,-50%) rotate(0) scale(1)', opacity: 1},
          {transform: 'translate(' + (Math.cos(a) * dist) + 'px,' + (Math.sin(a) * dist - 60) + 'px) rotate(' + (Math.random() * 720) + 'deg) scale(.6)', opacity: 0}
        ], {duration: 1100 + Math.random() * 600, easing: 'cubic-bezier(.2,.7,.2,1)'}).onfinish = function(){ this.effect.target.remove(); };
      }
    });
  }

  // Rzeźba: podgląd z kilku stron – przeciąganie, strzałki, miniatury, lupa
  var viewer = document.querySelector('.viewer');
  if (viewer) {
    var stage = viewer.querySelector('.viewer__stage'), frames = viewer.querySelectorAll('.viewer__frame'),
        vthumbs = viewer.querySelectorAll('.viewer__thumb'), vcount = viewer.querySelector('.viewer__count'),
        lens = viewer.querySelector('.viewer__lens'), vi = 0;
    var go = function(n){
      vi = (n + frames.length) % frames.length;
      frames.forEach(function(f, k){ f.classList.toggle('is-active', k === vi); });
      vthumbs.forEach(function(t, k){ t.classList.toggle('is-active', k === vi); if (k === vi) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current'); });
      vcount.textContent = (vi + 1) + ' / ' + frames.length;
    };
    vthumbs.forEach(function(t){ t.addEventListener('click', function(){ viewer.classList.add('used'); go(+t.dataset.i); }); });
    stage.addEventListener('keydown', function(e){
      if (e.key === 'ArrowRight') { viewer.classList.add('used'); go(vi + 1); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { viewer.classList.add('used'); go(vi - 1); e.preventDefault(); }
    });
    // przeciąganie: co ~70 px kolejne ujęcie (efekt obracania)
    var sx = null, acc = 0;
    stage.addEventListener('pointerdown', function(e){ sx = e.clientX; acc = 0; if (e.pointerType === 'mouse') stage.setPointerCapture(e.pointerId); });
    stage.addEventListener('pointermove', function(e){
      if (sx === null) return;
      acc += e.clientX - sx; sx = e.clientX;
      if (Math.abs(acc) > 70) { viewer.classList.add('used'); go(vi + (acc < 0 ? 1 : -1)); acc = 0; }
    });
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(function(t){ stage.addEventListener(t, function(){ sx = null; }); });
    // lupa (tylko mysz)
    if (finePointer) {
      stage.addEventListener('mousemove', function(e){
        if (sx !== null) { lens.classList.remove('on'); return; }
        var r = stage.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top, z = 2.4;
        var src = frames[vi].getAttribute('data-full'), img = frames[vi].querySelector('img');
        // rzeczywisty obszar zdjęcia przy object-fit: contain (ujęcia mają różne proporcje)
        var ratio = (img.naturalWidth || img.width) / (img.naturalHeight || img.height), iw = r.width, ih = r.width / ratio;
        if (ih > r.height) { ih = r.height; iw = ih * ratio; }
        var ox = (r.width - iw) / 2, oy = (r.height - ih) / 2;
        lens.style.backgroundImage = 'url("' + src + '")';
        lens.style.backgroundColor = '#fff';
        lens.style.backgroundSize = (iw * z) + 'px ' + (ih * z) + 'px';
        lens.style.backgroundPosition = (-((x - ox) * z - 95)) + 'px ' + (-((y - oy) * z - 95)) + 'px';
        lens.style.left = (x - 95) + 'px'; lens.style.top = (y - 95) + 'px';
        lens.classList.add('on');
      });
      stage.addEventListener('mouseleave', function(){ lens.classList.remove('on'); });
    }
    // krótka autoprezentacja: rzeźba „obraca się” raz po wejściu na stronę
    if (!reduce) {
      var demo = 0, demoT = setInterval(function(){
        if (viewer.classList.contains('used') || demo >= frames.length) { clearInterval(demoT); if (!viewer.classList.contains('used')) go(0); return; }
        demo++; go(demo % frames.length);
      }, 900);
    }
  }

  // Godziny otwarcia: podświetlenie dzisiejszego dnia (czas polski)
  try {
    var todayName = new Intl.DateTimeFormat('en-US', {timeZone: 'Europe/Warsaw', weekday: 'short'}).format(new Date());
    var todayIdx = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(todayName);
    document.querySelectorAll('.hours-table tr[data-days]').forEach(function(tr){
      if (tr.getAttribute('data-days').split(',').indexOf(String(todayIdx)) !== -1) tr.classList.add('today');
    });
  } catch (e) {}

  // Mapa Google ładowana dopiero za zgodą (RODO); zgoda zapamiętana w przeglądarce
  var map = document.querySelector('.map[data-map-src]');
  if (map) {
    var loadMap = function(){
      if (map.classList.contains('loaded')) return;
      var f = document.createElement('iframe');
      f.src = map.getAttribute('data-map-src'); f.title = map.getAttribute('data-map-title');
      f.loading = 'lazy'; f.referrerPolicy = 'no-referrer-when-downgrade'; f.allowFullscreen = true;
      map.appendChild(f);
      var open = document.createElement('a');
      open.className = 'btn btn--primary map__link'; open.target = '_blank'; open.rel = 'noopener';
      open.href = document.querySelector('.map__consent .link-arrow').href; open.textContent = 'Otwórz w Google Maps';
      map.appendChild(open);
      map.classList.add('loaded');
    };
    map.querySelector('[data-map-load]').addEventListener('click', function(){
      try { localStorage.setItem('ko-map-consent', '1'); } catch (e) {}
      loadMap();
    });
    try { if (localStorage.getItem('ko-map-consent') === '1') loadMap(); } catch (e) {}
  }

  // Inteligentny przycisk w hero: w godzinach pracy „Zadzwoń”, po godzinach „Napisz”
  var smart = document.querySelector('[data-smart-cta]');
  if (smart && status.length) {
    var isOpen = status[0].classList.contains('is-open');
    if (!isOpen) { smart.href = smart.getAttribute('data-closed-href'); smart.querySelector('span').textContent = smart.getAttribute('data-closed'); }
  }

  // Kalendarz ogrodnika: zakładki miesięcy, bieżący miesiąc domyślnie
  var cal = document.querySelector('.cal');
  if (cal) {
    var tabs = cal.querySelectorAll('.cal__tab'), panels = cal.querySelectorAll('.cal__panel');
    var month = 0;
    try { month = parseInt(new Intl.DateTimeFormat('en-US', {timeZone: 'Europe/Warsaw', month: 'numeric'}).format(new Date()), 10) - 1; } catch (e) { month = new Date().getMonth(); }
    tabs[month].classList.add('is-now');
    var pick = function(i, focus){
      tabs.forEach(function(t, k){ t.setAttribute('aria-selected', k === i); t.tabIndex = k === i ? 0 : -1; });
      panels.forEach(function(p, k){ p.hidden = k !== i; });
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function(t, i){
      t.addEventListener('click', function(){ pick(i); });
      t.addEventListener('keydown', function(e){
        if (e.key === 'ArrowRight') pick((i + 1) % 12, true);
        if (e.key === 'ArrowLeft') pick((i + 11) % 12, true);
      });
    });
    pick(month);
  }

  // Konfigurator zapytania o wycenę
  var wiz = document.getElementById('wizard');
  if (wiz) {
    var wsteps = wiz.querySelectorAll('.wizard__step'), dots = wiz.querySelectorAll('.wizard__steps li'), bar = wiz.querySelector('.wizard__bar span');
    var prev = wiz.querySelector('[data-prev]'), next = wiz.querySelector('[data-next]'), send = wiz.querySelector('[data-send]'), wnote = wiz.querySelector('.form__note');
    var cur = 0;
    var showStep = function(i){
      cur = i;
      wsteps.forEach(function(s, k){ s.classList.toggle('is-active', k === i); });
      dots.forEach(function(d, k){ d.classList.toggle('is-active', k === i); d.classList.toggle('is-done', k < i); });
      bar.style.width = ((i + 1) / wsteps.length * 100) + '%';
      prev.hidden = i === 0; next.hidden = i === wsteps.length - 1; send.hidden = i !== wsteps.length - 1;
      wnote.textContent = '';
      var first = wsteps[i].querySelector('input:not([type=checkbox]):not([type=radio]):not([type=range]), textarea');
      if (first && finePointer) first.focus({preventScroll: true});
    };
    var val = function(name){
      var els = wiz.querySelectorAll('[name="' + name + '"]');
      if (!els.length) return '';
      if (els[0].type === 'checkbox') return Array.prototype.filter.call(els, function(e){ return e.checked; }).map(function(e){ return e.value; }).join(', ');
      if (els[0].type === 'radio') { var c = Array.prototype.filter.call(els, function(e){ return e.checked; })[0]; return c ? c.value : ''; }
      if (els[0].type === 'range') return els[0].value + ' m²';
      return els[0].value.trim();
    };
    var updateSummary = function(){
      document.querySelectorAll('[data-sum]').forEach(function(dd){
        var v = val(dd.getAttribute('data-sum')) || '–';
        if (dd.textContent !== v) { dd.textContent = v; dd.classList.add('flash'); setTimeout(function(){ dd.classList.remove('flash'); }, 600); }
      });
      var range = wiz.querySelector('#q-area');
      if (range) { range.style.setProperty('--p', ((range.value - range.min) / (range.max - range.min) * 100) + '%'); document.getElementById('q-area-out').textContent = range.value + ' m²'; }
      try { localStorage.setItem('ko-quote', JSON.stringify({zakres: val('zakres'), powierzchnia: wiz.querySelector('#q-area').value, teren: val('teren'), miejscowosc: val('miejscowosc'), termin: val('termin'), uwagi: val('uwagi')})); } catch (e) {}
    };
    wiz.addEventListener('input', updateSummary); wiz.addEventListener('change', updateSummary);
    // przywrócenie niedokończonego zapytania
    try {
      var saved = JSON.parse(localStorage.getItem('ko-quote') || 'null');
      if (saved) {
        (saved.zakres || '').split(', ').forEach(function(v){ var e = wiz.querySelector('[name=zakres][value="' + v + '"]'); if (e) e.checked = true; });
        if (saved.powierzchnia) wiz.querySelector('#q-area').value = saved.powierzchnia;
        ['teren', 'termin'].forEach(function(n){ var e = saved[n] && wiz.querySelector('[name=' + n + '][value="' + saved[n] + '"]'); if (e) e.checked = true; });
        if (saved.miejscowosc) wiz.querySelector('#q-city').value = saved.miejscowosc;
        if (saved.uwagi) wiz.querySelector('#q-notes').value = saved.uwagi;
      }
    } catch (e) {}
    updateSummary();
    var validate = function(i){
      if (i === 0 && !val('zakres')) { wnote.textContent = 'Zaznacz przynajmniej jedną usługę.'; return false; }
      return true;
    };
    next.addEventListener('click', function(){ if (validate(cur)) showStep(cur + 1); });
    prev.addEventListener('click', function(){ showStep(cur - 1); });
    wiz.addEventListener('submit', function(e){
      e.preventDefault();
      if (wiz.elements.firma.value) { wnote.textContent = 'Dziękujemy!'; return; }
      var email = wiz.elements.email, ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
      email.classList.toggle('invalid', !ok);
      if (!ok) { wnote.textContent = 'Podaj poprawny adres e-mail, żebyśmy mogli odpowiedzieć.'; wiz.classList.remove('shake'); void wiz.offsetWidth; wiz.classList.add('shake'); return; }
      var lines = ['Zapytanie o wycenę ze strony komfortoweogrody.pl', '',
        'Zakres: ' + (val('zakres') || '–'), 'Powierzchnia: ' + val('powierzchnia'), 'Teren: ' + (val('teren') || '–'),
        'Miejscowość: ' + (val('miejscowosc') || '–'), 'Termin: ' + (val('termin') || '–'), 'Uwagi: ' + (val('uwagi') || '–'), '',
        'Kontakt: ' + (val('name') || '–'), 'Telefon: ' + (val('phone') || '–'), 'E-mail: ' + email.value.trim()];
      window.location.href = 'mailto:kontakt@komfortoweogrody.pl?subject=' + encodeURIComponent('Zapytanie o wycenę' + (val('name') ? ' – ' + val('name') : '')) + '&body=' + encodeURIComponent(lines.join('\n'));
      wnote.textContent = 'Dziękujemy! Otwieramy Twój program pocztowy z gotowym zapytaniem.';
      try { localStorage.removeItem('ko-quote'); } catch (er) {}
    });
    var copyBtn = document.querySelector('[data-copy-summary]');
    if (copyBtn) copyBtn.addEventListener('click', function(){
      var txt = Array.prototype.map.call(document.querySelectorAll('#summary div'), function(d){ return d.querySelector('dt').textContent + ': ' + d.querySelector('dd').textContent; }).join('\n');
      var done = function(){ showToast('Skopiowano podsumowanie'); };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, done); else done();
    });
    showStep(0);
  }

  // Na podglądzie w github.io strona leży obok aplikacji Król Kufla, której service worker (cache-first)
  // obejmuje cały serwis. Własny, pusty worker o węższym zasięgu sprawia, że ta strona zawsze idzie z sieci.
  if ('serviceWorker' in navigator && location.hostname.indexOf('github.io') !== -1) {
    var root = new URL('../', document.currentScript ? document.currentScript.src : location.href);
    navigator.serviceWorker.register(new URL('sw.js', root).href, {scope: root.pathname}).catch(function(){});
  }
})();
