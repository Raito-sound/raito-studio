(() => {
  const canvas = document.getElementById('signal');
  const context = canvas?.getContext('2d');
  if (!canvas || !context) return;

  const hero = canvas.closest('.hero');
  const surface = canvas.parentElement;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let width = 0;
  let height = 0;
  let frame = 0;
  let lastFrame = 0;
  let visible = true;
  let pointerX = 0.5;
  let pointerY = 0.5;

  const draw = (time) => {
    context.clearRect(0, 0, width, height);
    const rows = width < 600 ? 13 : 19;
    const points = width < 600 ? 44 : 72;
    const phase = time * 0.00013;
    for (let row = 0; row < rows; row += 1) {
      const depth = row / (rows - 1);
      context.beginPath();
      for (let point = 0; point <= points; point += 1) {
        const x = point / points;
        const envelope = Math.pow(Math.sin(x * Math.PI), 1.4);
        const amplitude = height * (0.05 + depth * 0.08);
        const wave = Math.sin(x * 13 - phase * 2 + row * 0.28);
        const swell = Math.sin(x * 7 + phase + row * 0.13) * 0.4;
        const y = height * (0.35 + depth * 0.5) + (wave + swell) * amplitude * envelope;
        const px = x * width + (pointerX - 0.5) * depth * 14;
        const py = y + (pointerY - 0.5) * depth * 10;
        if (point === 0) context.moveTo(px, py);
        else context.lineTo(px, py);
      }
      const stroke = context.createLinearGradient(0, 0, width, 0);
      const color = row % 4 === 0 ? '191,56,44' : '98,98,93';
      const opacity = row % 4 === 0 ? .46 : .24;
      stroke.addColorStop(0, `rgba(${color},0)`);
      stroke.addColorStop(.18, `rgba(${color},${opacity})`);
      stroke.addColorStop(.88, `rgba(${color},${opacity})`);
      stroke.addColorStop(1, `rgba(${color},0)`);
      context.strokeStyle = stroke;
      context.lineWidth = row % 4 === 0 ? 1 : 0.7;
      context.stroke();
    }
  };

  const tick = (time) => {
    frame = 0;
    if (!visible || document.hidden || motion.matches) return;
    if (time - lastFrame >= 32) {
      draw(time);
      lastFrame = time;
    }
    frame = requestAnimationFrame(tick);
  };
  const sync = () => {
    cancelAnimationFrame(frame);
    frame = 0;
    if (document.hidden) return;
    if (motion.matches) draw(0);
    else if (visible) frame = requestAnimationFrame(tick);
  };
  const resize = () => {
    const bounds = surface.getBoundingClientRect();
    width = bounds.width;
    height = bounds.height;
    const dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw(0);
    sync();
  };

  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(surface);
  else addEventListener('resize', resize, { passive: true });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      sync();
    }).observe(hero);
  }
  hero.addEventListener('pointermove', (event) => {
    const bounds = hero.getBoundingClientRect();
    pointerX = (event.clientX - bounds.left) / Math.max(bounds.width, 1);
    pointerY = (event.clientY - bounds.top) / Math.max(bounds.height, 1);
  }, { passive: true });
  hero.addEventListener('pointerleave', () => { pointerX = pointerY = 0.5; });
  motion.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  resize();
})();
