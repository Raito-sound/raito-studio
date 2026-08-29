(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const header = document.querySelector('.site-header');
  const revealItems = document.querySelectorAll('.reveal');

  const setHeader = () => header?.classList.toggle('scrolled', window.scrollY > 24);
  setHeader();
  window.addEventListener('scroll', setHeader, { passive: true });

  if (reduced || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('in'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    revealItems.forEach((item) => observer.observe(item));
  }

  if (reduced) return;
  const canvas = document.getElementById('signal');
  const ctx = canvas?.getContext('2d');
  if (!canvas || !ctx) return;

  let width = 0;
  let height = 0;
  let dpr = 1;
  let pointerX = 0.5;
  let pointerY = 0.5;

  const resize = () => {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };

  const draw = (time) => {
    ctx.clearRect(0, 0, width, height);
    const rows = width < 700 ? 11 : 17;
    const points = width < 700 ? 38 : 68;
    const horizon = height * (0.34 + (pointerY - 0.5) * 0.035);
    const phase = time * 0.00034;

    for (let row = 0; row < rows; row += 1) {
      const depth = row / Math.max(rows - 1, 1);
      const yBase = horizon + Math.pow(depth, 1.75) * height * 0.76;
      ctx.beginPath();
      for (let point = 0; point <= points; point += 1) {
        const ratio = point / points;
        const centered = ratio - 0.5;
        const amplitude = 8 + depth * 38;
        const wave = Math.sin(centered * 15 + phase * 4 + row * 0.48) * amplitude;
        const swell = Math.sin(centered * 5 - phase * 2.2 + row * 0.18) * amplitude * 0.55;
        const x = ratio * width + (pointerX - 0.5) * depth * 34;
        const y = yBase + wave + swell;
        if (point === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = row % 4 === 0 ? 'rgba(225,59,48,0.16)' : 'rgba(17,19,24,0.09)';
      ctx.lineWidth = row % 4 === 0 ? 1.15 : 0.75;
      ctx.stroke();
    }
    window.requestAnimationFrame(draw);
  };

  window.addEventListener('pointermove', (event) => {
    pointerX = event.clientX / Math.max(window.innerWidth, 1);
    pointerY = event.clientY / Math.max(window.innerHeight, 1);
  }, { passive: true });
  window.addEventListener('resize', resize, { passive: true });
  resize();
  window.requestAnimationFrame(draw);
})();
