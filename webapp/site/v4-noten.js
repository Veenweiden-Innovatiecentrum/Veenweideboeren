/* Bron-fiches (ⓘ-noten) — klik om te openen, klik elders of ESC om te sluiten.
   Overgenomen uit de brondocumenten; werkt via event-delegatie, dus ook op
   content die React later rendert. */
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.fiche-btn');
  const wrap = btn ? btn.parentElement : null;
  document.querySelectorAll('.fiche-wrap.open').forEach(function (w) {
    if (w !== wrap) w.classList.remove('open');
  });
  if (wrap) {
    wrap.classList.toggle('open');
    e.stopPropagation();
  }
});
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.fiche-wrap.open').forEach(function (w) { w.classList.remove('open'); });
  }
});
