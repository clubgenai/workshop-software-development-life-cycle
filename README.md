# workshop-software-development-life-cycle

Workshop du Club GenAI : **Intégrer l'IA dans son SDLC**.

- Présentation en ligne : https://clubgenai.github.io/workshop-software-development-life-cycle/
- Sources de la présentation ([Reveal.js](https://revealjs.com/), construite avec Vite) : [`presentation/`](presentation/)
  - diapos et notes de l'orateur : [`presentation/index.html`](presentation/index.html)
  - charte et animations : [`presentation/src/styles.css`](presentation/src/styles.css)
  - configuration Reveal.js : [`presentation/src/main.js`](presentation/src/main.js)

La présentation est construite puis publiée automatiquement sur GitHub Pages à chaque push sur `main` qui modifie `presentation/`
(voir [`.github/workflows/pages.yml`](.github/workflows/pages.yml)).

## Lancer la présentation en local

```bash
cd presentation && npm install && npm run dev
```

`npm run build` produit la version statique dans `presentation/dist/`.

## Présenter

Flèches, espace ou clic pour avancer, `F` pour le plein écran, `S` (ou `N`) pour ouvrir la vue orateur avec les notes,
`Échap` pour la vue d'ensemble.

## TP

```bash
git clone https://github.com/clubgenai/workshop-software-development-life-cycle.git
git checkout tp
```
