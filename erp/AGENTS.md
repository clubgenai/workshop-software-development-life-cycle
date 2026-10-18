# Règles pour les agents

Ce fichier est lu par les agents de code (Claude Code, Codex, Cursor…). Complétez-le pendant le TP : chaque leçon apprise devient une règle ici.

## Projet

- Next.js (App Router) et TypeScript strict, dans `src/`.
- La base est le fichier `data/cvs.json` ; les PDF sont dans `data/cvs/`. Pas de base de données.
- L'accès aux données passe uniquement par `src/lib/cvs.ts`.
- Le front appelle l'API (`/api/cvs…`), il ne lit jamais le disque.

## Conventions

- Interface et messages en français.
- Les couleurs viennent des variables CSS de `src/app/globals.css`, jamais de valeurs en dur. Vérifier les deux thèmes.
- Toute nouvelle route d'API renvoie un message d'erreur lisible avec le bon code HTTP.

## Preuve

- Un changement n'est terminé que si `npm run typecheck`, `npm run build` et `npm run test:e2e` passent, sorties à l'appui.
- Les tests partent des scénarios d'acceptation écrits avant le code. Ne jamais modifier un test pour le faire passer sans accord humain.

## Leçons du TP

<!-- Exemple : « Les requêtes ignorent la casse et les accents (Saint-Étienne = saint-etienne). » -->
