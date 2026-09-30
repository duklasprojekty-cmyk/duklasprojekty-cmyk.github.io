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

// Strona Król Kufla w katalogu głównym ma service workera (cache-first) o zasięgu "/".
// Własny, pusty worker o węższym zasięgu sprawia, że ta podstrona zawsze idzie z sieci.
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js', {scope: './'}).catch(function(){});
}
