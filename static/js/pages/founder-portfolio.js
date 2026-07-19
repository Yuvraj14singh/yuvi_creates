(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('[data-fp-reveal]');
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -30px' });
    revealItems.forEach((item) => observer.observe(item));
  }
  document.querySelectorAll('[data-fp-timeline] li').forEach((item) => {
    item.querySelector('button')?.addEventListener('click', () => {
      item.parentElement.querySelectorAll('li').forEach((entry) => entry.classList.remove('is-active'));
      item.classList.add('is-active');
    });
  });
  const visual = document.querySelector('[data-fp-parallax]');
  if (visual && !reducedMotion && window.matchMedia('(pointer: fine)').matches) {
    visual.addEventListener('pointermove', (event) => {
      const box = visual.getBoundingClientRect();
      visual.style.setProperty('--fp-rx', `${((event.clientX - box.left) / box.width - .5) * 3}deg`);
      visual.style.setProperty('--fp-ry', `${((event.clientY - box.top) / box.height - .5) * -3}deg`);
    });
    visual.addEventListener('pointerleave', () => {
      visual.style.setProperty('--fp-rx', '0deg');
      visual.style.setProperty('--fp-ry', '0deg');
    });
  }
})();
