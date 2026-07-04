// Customer-story slider: one frame, images cross-fade, caption updates
(function () {
  const story = document.querySelector('.story');
  if (!story) return;
  const photos = Array.from(story.querySelectorAll('.story-photo'));
  const dots = Array.from(story.querySelectorAll('.story-dot'));
  const quote = story.querySelector('#story-quote');
  const person = story.querySelector('#story-person');
  const firm = story.querySelector('#story-firm');
  const link = story.querySelector('#story-link');
  if (photos.length < 2) return;
  let i = 0, timer;

  function show(n) {
    i = (n + photos.length) % photos.length;
    photos.forEach((p, k) => p.classList.toggle('is-active', k === i));
    dots.forEach((d, k) => d.classList.toggle('is-active', k === i));
    const p = photos[i].dataset;
    if (quote) quote.textContent = '„' + p.quote + '“';
    if (person) person.textContent = p.person;
    if (firm) firm.textContent = p.firm;
    if (link) link.href = p.url;
  }
  function next() { show(i + 1); }
  function prev() { show(i - 1); }
  function start() { stop(); timer = setInterval(next, 5500); }
  function stop() { if (timer) clearInterval(timer); }

  story.querySelector('.story-arrow--next').addEventListener('click', () => { next(); start(); });
  story.querySelector('.story-arrow--prev').addEventListener('click', () => { prev(); start(); });
  dots.forEach((d) => d.addEventListener('click', () => { show(+d.dataset.go); start(); }));
  story.addEventListener('mouseenter', stop);
  story.addEventListener('mouseleave', start);
  start();
})();

// Mobile navigation toggle
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav');

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}
