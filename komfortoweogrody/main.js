// Zdjęcia są hostowane na serwerze kreatora Zyro/Hostinger; jeśli przestaną tam działać,
// strona sięga po ich kopię z Internet Archive (zrzut z 23.05.2025).
document.querySelectorAll('img[src^="https://assets.zyrosite.com/"]').forEach(function(img){
  img.addEventListener('error', function onErr(){
    img.removeEventListener('error', onErr);
    img.src = 'https://web.archive.org/web/20250523233057im_/' + img.getAttribute('src');
  });
});

// Menu mobilne
(function(){
  var header = document.querySelector('.header');
  var burger = header.querySelector('.burger');
  burger.addEventListener('click', function(){
    var open = header.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  header.querySelectorAll('.nav a').forEach(function(a){
    a.addEventListener('click', function(){ header.classList.remove('open'); burger.setAttribute('aria-expanded', false); });
  });
})();

// Animacja pojawiania się sekcji
(function(){
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { els.forEach(function(e){ e.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, {threshold: 0.12});
  els.forEach(function(e){ io.observe(e); });
})();

// Galeria: podgląd zdjęć na pełnym ekranie
(function(){
  var box = document.querySelector('.lightbox');
  if (!box) return;
  var links = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  var img = box.querySelector('img'), current = 0;
  function show(i){
    current = (i + links.length) % links.length;
    img.src = links[current].href;
    img.alt = links[current].querySelector('img').alt;
  }
  function close(){ box.hidden = true; document.body.style.overflow = ''; }
  links.forEach(function(a, i){
    a.addEventListener('click', function(e){
      e.preventDefault(); show(i); box.hidden = false; document.body.style.overflow = 'hidden';
    });
  });
  img.addEventListener('error', function(){
    if (img.src.indexOf('web.archive.org') === -1) img.src = 'https://web.archive.org/web/20250524012056im_/' + links[current].querySelector('img').getAttribute('src');
  });
  box.querySelector('.lightbox__close').addEventListener('click', close);
  box.querySelector('.lightbox__prev').addEventListener('click', function(){ show(current - 1); });
  box.querySelector('.lightbox__next').addEventListener('click', function(){ show(current + 1); });
  box.addEventListener('click', function(e){ if (e.target === box) close(); });
  document.addEventListener('keydown', function(e){
    if (box.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(current - 1);
    if (e.key === 'ArrowRight') show(current + 1);
  });
})();

// Kontakt: strona jest statyczna, więc formularz otwiera program pocztowy z gotową wiadomością
(function(){
  var form = document.getElementById('contact-form');
  if (!form) return;
  var note = form.querySelector('.form__note');
  form.addEventListener('submit', function(e){
    e.preventDefault();
    var name = form.name.value.trim(), email = form.email.value.trim(), msg = form.message.value.trim();
    var ok = true;
    [[form.email, /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)], [form.message, msg.length > 0]].forEach(function(p){
      p[0].classList.toggle('invalid', !p[1]); if (!p[1]) ok = false;
    });
    if (!ok) { note.textContent = 'Uzupełnij poprawnie adres e-mail i wiadomość.'; return; }
    var body = msg + '\n\n' + (name ? name + '\n' : '') + email;
    window.location.href = 'mailto:kontakt@komfortoweogrody.pl?subject=' +
      encodeURIComponent('Zapytanie ze strony' + (name ? ' – ' + name : '')) + '&body=' + encodeURIComponent(body);
    note.textContent = 'Dziękujemy za kontakt! Otwieramy Twój program pocztowy z gotową wiadomością.';
  });
})();

// Strona Król Kufla w katalogu głównym ma service workera (cache-first) o zasięgu "/".
// Własny, pusty worker o węższym zasięgu sprawia, że ta podstrona zawsze idzie z sieci.
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js', {scope: './'}).catch(function(){});
}
