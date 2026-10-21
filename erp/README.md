# CVthèque · ERP RH du TP

Application Next.js utilisée pendant le TP du workshop Club GenAI « Intégrer l'IA dans son SDLC ».
Elle tourne en local, sans authentification, sur des données fictives.

## Démarrer

Prérequis : Node.js 20.9 ou plus récent.

```bash
cd erp
npm install
npm run dev
```

Puis ouvrir http://localhost:3000.

## Ce que fait l'application

- **`/`** : la liste de tous les profils.
- **`/cvs/[id]`** : la fiche d'un profil, avec son CV en PDF.
- Thème clair ou sombre selon le réglage du système, avec un bouton pour changer (le choix est mémorisé dans le navigateur).

## API

| Méthode et route | Réponse |
|---|---|
| `GET /api/cvs` | `{ total, cvs: Cv[] }`, tous les profils |
| `GET /api/cvs/:id` | un profil, ou `404` |
| `GET /api/cvs/:id/cv` | le CV au format PDF, ou `404` |

## Données

La base est un simple fichier : [`data/cvs.json`](data/cvs.json). Chaque profil pointe vers son PDF dans [`data/cvs/`](data/cvs).

```json
{
  "id": "cv-001",
  "prenom": "Léa",
  "nom": "Martin",
  "localisation": "Bordeaux",
  "metier": "Développeuse Full-stack",
  "remuneration": 48000,
  "cv": "cvs/cv-001-lea-martin.pdf"
}
```

- `remuneration` est un salaire annuel brut, en euros.
- `cv` est relatif au dossier `data/`. L'API refuse tout chemin qui sortirait de `data/cvs/`.
- Le fichier est relu à chaque requête : une modification est visible sans redémarrer le serveur.

Les 24 profils et leurs CV sont fictifs. Quelques valeurs servent de cas limites : un nom avec apostrophe (N'Diaye), un nom composé (Le Gall), un prénom composé (Anne-Sophie), une ville avec tiret et accent (Saint-Étienne), des métiers proches (Data Engineer, Data Scientist).

## Tests

```bash
npx playwright install chromium   # une seule fois
npm run test:e2e
```

Les tests de [`e2e/cvtheque.spec.ts`](e2e/cvtheque.spec.ts) décrivent le comportement actuel. Le serveur de développement démarre tout seul s'il ne tourne pas déjà.

## Le sujet du TP

Ajouter un **filtre par requêtes booléennes**, côté front et côté back, par exemple :

```
(métier:DevOps OR métier:SRE) AND NOT localisation:Paris
```

Avant de lancer un agent, passez par le premier temps du cycle : écrivez la spec et les scénarios d'acceptation (syntaxe acceptée, priorité des opérateurs, champs, comparaisons sur la rémunération, accents et casse, requête invalide).

### Le fil du TP : cinq commandes

Lancez `claude` depuis `erp/`. Chaque commande s'arrête sur une décision humaine : la suivante refuse de démarrer tant que le gate précédent n'est pas coché, à la main, dans `specs/<feature>.md`.

| Temps | Commande | Qui | Gate humain | Livrable |
|---|---|---|---|---|
| 1 · Cadrer | `/cadrer <besoin>` | PO + Dev | Intention et plan validés | `specs/<feature>.md` |
| 2 · Construire et prouver | `/construire specs/<feature>.md` | Dev | — | Branche `feat/…`, tests `S#`, section Preuve |
| 2 · Relire | `/relire specs/<feature>.md` | Reviewer, **session neuve** | PR acceptée | Section Relecture |
| 3 · Livrer et observer | `/livrer specs/<feature>.md` | Dev + Ops/PO | Livraison validée | Changelog, rollback, indicateurs, PR |
| 4 · Capitaliser | `/capitaliser specs/<feature>.md` | Toute l'équipe | Règles choisies | Section « Leçons du TP » d'`AGENTS.md` |

Projet perso : copiez `erp/.claude/commands/` dans votre dépôt et adaptez la section « Preuve » de votre `AGENTS.md`/`CLAUDE.md` (les commandes n'y codent ni stack ni script).

Pour régénérer les CV PDF : `python3 scripts/make_cvs.py data` (nécessite `reportlab`).
