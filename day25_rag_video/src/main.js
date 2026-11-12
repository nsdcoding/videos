// Build everything, then expose renderAt(t) to the renderer.
(function () {
  buildHUD();
  const scenes = window.SCENES || [];
  for (const s of scenes) s();
  // background blobs drift with the camera (parallax) and breathe slowly
  const b1 = document.getElementById('blob1'), b2 = document.getElementById('blob2'), b3 = document.getElementById('blob3');
  everyFrame((t, c) => {
    const px = -c.x * .06, py = -c.y * .06;
    b1.style.transform = `translate(${px + Math.sin(t * .11) * 120}px,${py + Math.cos(t * .09) * 80}px) scale(${1 + .15 * Math.sin(t * .07)})`;
    b2.style.transform = `translate(${px * .7 + Math.cos(t * .08) * 140}px,${py * .7 + Math.sin(t * .1) * 90}px)`;
    b3.style.transform = `translate(${px * 1.3 + Math.sin(t * .06 + 2) * 160}px,${py * 1.3}px)`;
  });
  // cull boards that are far off-screen (big speed-up when capturing frames)
  const cull = Object.keys(BOARDS).map(id => ({ el: document.getElementById(id === 'VSB' ? 'vsc' : id), b: BOARDS[id], on: true }));
  everyFrame((t, c) => {
    const hw = 960 / c.z + 700, hh = 540 / c.z + 700;
    for (const k of cull) {
      const vis = k.b.x + 1920 > c.x - hw && k.b.x < c.x + hw && k.b.y + 1080 > c.y - hh && k.b.y < c.y + hh;
      if (vis !== k.on) { k.on = vis; k.el.style.display = vis ? '' : 'none'; }
    }
  });
  window.READY = true;
})();
