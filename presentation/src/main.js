import Reveal from 'reveal.js';
import RevealNotes from 'reveal.js/plugin/notes';
import 'reveal.js/reveal.css';
import './styles.css';

const slides = [...document.querySelectorAll('.reveal .slides > section')];
const N = slides.length;
const pad2 = n => String(n).padStart(2, '0');

// Pied de page : partie + numéro (toutes les diapos sauf l'accueil)
slides.forEach((s, i) => {
  if (i === 0) return;
  let f = s.querySelector('.foot');
  if (!f) {
    f = document.createElement('div');
    f.className = 'foot';
    f.innerHTML = '<span>Club GenAI · Intégrer l\'IA dans son SDLC</span><span class="pn"></span>';
    s.appendChild(f);
  }
  const pn = f.querySelector('.pn');
  if (pn) pn.innerHTML = '<b>' + (s.dataset.part || '') + '</b> · ' + pad2(i + 1) + ' / ' + N;
});

Reveal.initialize({
  // Scène 16:9 fixe, mise à l'échelle de la fenêtre
  width: 1920,
  height: 1080,
  margin: 0,
  minScale: 0.05,
  maxScale: 4,
  center: false,
  // Pas de surcouche de contrôles : seule la barre de progression reste affichée
  controls: false,
  progress: true,
  slideNumber: false,
  hash: true,
  transition: 'sfeir',
  backgroundTransition: 'none',
  keyboard: {
    8: 'prev', // Retour arrière
    13: () => (Reveal.isOverview() ? Reveal.toggleOverview(false) : Reveal.next()), // Entrée
    78: () => Reveal.getPlugin('notes').open(), // N : vue orateur, comme S
  },
  plugins: [RevealNotes],
}).then(() => {
  // Clic sur la diapo : quart gauche = retour, reste = avance (les liens restent cliquables)
  const el = Reveal.getSlidesElement();
  el.addEventListener('click', e => {
    if (e.defaultPrevented || e.target.closest('a')) return;
    const r = el.getBoundingClientRect();
    if (e.clientX - r.left < r.width * 0.25) Reveal.prev();
    else Reveal.next();
  });
});
