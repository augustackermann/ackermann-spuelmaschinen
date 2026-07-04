// Customer-story slider
(function () {
  const slider = document.querySelector('.story-slider');
  if (!slider) return;
  const slides = Array.from(slider.querySelectorAll('.story-slide'));
  const dots = Array.from(document.querySelectorAll('.story-dot'));
  const story = document.querySelector('.story');
  let i = 0, timer;

  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('is-active', k === i));
    dots.forEach((d, k) => d.classList.toggle('is-active', k === i));
  }
  function next() { show(i + 1); }
  function prev() { show(i - 1); }
  function start() { stop(); timer = setInterval(next, 5500); }
  function stop() { if (timer) clearInterval(timer); }

  slider.querySelector('.story-arrow--next').addEventListener('click', () => { next(); start(); });
  slider.querySelector('.story-arrow--prev').addEventListener('click', () => { prev(); start(); });
  dots.forEach((d) => d.addEventListener('click', () => { show(+d.dataset.go); start(); }));
  if (story) { story.addEventListener('mouseenter', stop); story.addEventListener('mouseleave', start); }
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
