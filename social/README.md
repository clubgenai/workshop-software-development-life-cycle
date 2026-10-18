# Supports de communication

Supports pour annoncer le workshop « Intégrer l'IA dans son SDLC » et partager la présentation sur LinkedIn.

| Fichier | Format | Usage |
|---|---|---|
| `club-genai-sdlc-carre.mp4` | 1080×1080, 48 s, sans son | Post LinkedIn (carré, s'affiche bien sur ordinateur et mobile) |
| `club-genai-sdlc-portrait.mp4` | 1080×1350, 48 s, sans son | Post LinkedIn (4:5, prend plus de place dans le fil mobile) |
| `club-genai-sdlc-carre.gif` | 540 px, 12 s, en boucle | Commentaires, Slack, e-mail |
| `linkedin.md` | Texte | Brouillons de post : annonce et retour d'expérience |

Les vidéos n'ont pas de piste audio : LinkedIn les lance sans le son, ce sont les bandeaux qui portent le message.

## Régénérer après une modification de la présentation

Prérequis : Python 3, `pip install playwright`, `python -m playwright install chromium`, `ffmpeg`, et les polices `@fontsource` :

```bash
npm install --prefix fonts @fontsource/epilogue @fontsource/ibm-plex-mono
python3 reel.py ../presentation/index.html --storyboard story.json --format square \
  --fonts fonts/node_modules/@fontsource \
  --top "Club GenAI|Intégrer l'IA dans son SDLC" --bottom "Workshop · présentation + TP" \
  --out club-genai-sdlc-carre
```

Remplacer `square` par `portrait` (et le nom de sortie) pour la version 4:5. `story.json` liste les diapos montrées (numérotées à partir de 1) et leur durée ; si des diapos sont ajoutées ou retirées, mettre à jour les numéros.
