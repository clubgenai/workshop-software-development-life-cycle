# Workshop — Le SDLC à l'ère des agents

**Durée : 2 h (120 min) · Format : théorie + hands-on · Public : mixte tech / non-tech**

---

## 1. Cadre du workshop

### Promesse

À la fin des 2 h, chaque participant a livré une fonctionnalité de bout en bout avec un agent de code — spec, tests, implémentation, revue, commit — et sait **où poser sa main** dans la boucle.

### Message clé (fil rouge de toute la session)

> L'IA est un **amplificateur** : elle multiplie vos bonnes pratiques comme vos mauvaises.
> Le filet déterministe décide lesquelles.

Deuxième thèse, énoncée en partie 0 et rappelée à chaque partie :

> L'IA est un **levier** : plus l'erreur entre tôt dans la boucle, plus son rayon de souffle est grand.

### Objectifs pédagogiques

| # | À la fin, le participant sait… |
|---|---|
| 1 | Nommer les 5 phases du SDLC et dire ce que l'agent change dans chacune |
| 2 | Séparer *explorer → planifier → coder* au lieu de tout demander d'un coup |
| 3 | Écrire une spec avec critères d'acceptation qu'un agent peut exécuter |
| 4 | Placer une gate déterministe (test, lint, CI) sous la boucle de l'agent |
| 5 | Faire relire un diff par un vérificateur indépendant, en contexte frais |
| 6 | Encoder un miss dans `CLAUDE.md` ou un Skill pour qu'il ne se répète pas |
| 7 | Distinguer les 4 gates humaines et ce que chacune protège |

### Public & organisation de la salle

Public **mixte tech / non-tech** (devs, PO, QA, managers). Contrainte principale : le hands-on doit rester accessible sans savoir coder.

**Réponse retenue : binômes mixtes.**

- 1 binôme = 1 profil tech + 1 profil non-tech, **une seule machine**.
- Rôles tournants, annoncés au début de chaque partie :
  - **Porteur de vision** — tape le prompt, décide, tient les gates. *De préférence le non-tech.*
  - **Orchestrateur** — pilote le terminal, lit la sortie, interrompt sur dérive. *De préférence le tech.*
- Les deux rôles s'échangent entre la partie 2 et la partie 3.

Ce dispositif n'est pas un pis-aller : c'est exactement la répartition de rôles enseignée en partie 0. Le format *est* le contenu.

### Prérequis (à envoyer 48 h avant, pas de temps en séance)

- [ ] Claude Code installé et authentifié : `curl -fsSL https://claude.ai/install.sh | bash` puis `claude`
- [ ] Git + Python 3.11+ (ou Node, selon le repo retenu)
- [ ] Repo fil rouge cloné et `pytest` vert au premier lancement
- [ ] Commande de vérification fournie : `./check-setup.sh` → doit afficher `SETUP OK`
- [ ] Un canal (Slack/Teams) ouvert pour le support setup la veille

> **Plan B setup** : prévoir 2 machines de secours préconfigurées + un GitHub Codespace / devcontainer partagé. Un binôme bloqué en partie 1 est perdu pour les 4 parties.

---

## 2. Déroulé minuté

| Créneau | Bloc | Durée | Théorie | Pratique |
|---|---|---|---|---|
| 0:00 – 0:08 | **Introduction** — équipe, société, sommaire | 8 min | — | — |
| 0:08 – 0:18 | **Partie 0** — Le SDLC, c'est quoi ? | 10 min | 10 | — |
| 0:18 – 0:40 | **Partie 1** — Cadrer & Spécifier | 22 min | 8 | 14 |
| 0:40 – 1:03 | **Partie 2** — Construire | 23 min | 7 | 16 |
| 1:03 – 1:25 | **Partie 3** — Vérifier | 22 min | 8 | 14 |
| 1:25 – 1:47 | **Partie 4** — Livrer & Capitaliser | 22 min | 8 | 14 |
| 1:47 – 2:00 | **Conclusion + Q&A** | 13 min | — | — |
| | **Total** | **120 min** | **41** | **58** |

**Règle de timing** : chaque bloc pratique a un **cœur** (non négociable) et un **bonus** (coupable sans préavis). Les temps « bonus » sont marqués ⏱️ dans les fiches ci-dessous. Si vous avez 5 min de retard cumulé à 1:03, coupez tous les bonus restants.

---

## 3. Introduction — 8 min

1. **Qui parle** (2 min) — l'équipe, une phrase par personne, ce qu'elle fait au quotidien avec un agent.
2. **La société** (2 min) — bref, une slide.
3. **Sommaire & contrat de session** (3 min) — les 4 parties, la promesse, le fait que c'est hands-on en binômes.
4. **Sondage à main levée** (1 min) — *« Qui a déjà mergé du code écrit par une IA ? »* (a) souvent (b) une fois (c) pas encore (d) jamais de la vie.
   Sert à calibrer le niveau de friction des exercices et à ouvrir sur la partie 0.

**Annonce des binômes** : faites-les former pendant que la slide « société » est à l'écran, pas après.

---

## 4. Partie 0 — Le SDLC, c'est quoi ? (10 min · 100 % théorie)

### Objectif

Poser le vocabulaire commun tech / non-tech et le canevas sur lequel les 4 parties suivantes vont raisonner.

### Contenu

**a) La définition (2 min)**

> Le développement logiciel, c'est aller d'un **besoin utilisateur** à une **solution qui tourne**.

```
Besoin utilisateur
      ↓
Comprendre → Spécifier → Construire → Vérifier → Opérer
   problème    comportement   le code    conforme ?   déployer
   & "fini"      attendu                              observer
      ↓
Une solution qui tourne
```

Insister : ces 5 phases existaient avant l'IA. Waterfall, agile, DevOps — ce sont des façons différentes de parcourir cette boucle, pas des boucles différentes.

**b) Ce qui ne change pas (1 min)**

Les conventions, la Definition of Done, la suite de tests, la revue de code. Rien de neuf.
Ce qui manquait, c'était **l'application constante** : les règles vivaient dans les têtes, un wiki périmé, des commentaires de PR.

**c) Ce qui change (2 min)**

L'agent lit un fichier avant chaque tâche. Donc on encode la règle **une fois**, dans `CLAUDE.md` / `AGENTS.md`, et elle s'applique à **chaque** changement.

| Avant — implicite | Maintenant — écrit |
|---|---|
| Standards dans les têtes, wiki périmé | Un fichier chargé à chaque session |
| Appliqué en revue, si quelqu'un y pense | Appliqué pendant l'écriture, sur chaque change |

**d) Les deux thèses (3 min)**

*Amplificateur* — fondations solides ×10 = la bonne chose plus vite ; fondations faibles ×10 = la mauvaise chose plus vite, aussi confiante.
La friction qui ralentissait une mauvaise idée assez longtemps pour que quelqu'un la remarque était un mécanisme de sécurité accidentel. **On doit la réintroduire volontairement.**

*Levier* — même erreur, injectée à des phases différentes :

```
Comprendre  ████████████████████  ×5
Spécifier   ████████████████      ×4
Construire  ████████████          ×3
Vérifier    ████████              ×2
Opérer      ████                  ×1
```

Corollaire opérationnel : **on garde les gates humaines aux deux extrémités, on délègue le milieu.**

**e) Vos deux rôles (2 min)**

| 🧭 Porteur de vision | 🎛️ Orchestrateur |
|---|---|
| Possède Comprendre + Spécifier | Possède Vérifier + Opérer + la boucle |
| « Savoir quoi demander » | « Garder l'agent sur les rails » |
| L'agent construit votre demande **littérale**, pas votre intention | Sait comment les agents échouent : hallucination confiante, dérive de scope, lettre vs esprit |
| Le vrai travail : hypothèses, cas limites, critères d'acceptation | Place les points de vérification pour qu'une erreur précoce ne se propage pas |

> **Transition vers la partie 1** : « On va faire les cinq phases, dans l'ordre, en binôme. On commence par celle où l'amplification est la plus forte — et la moins chère. »

---

## 5. Partie 1 — Cadrer & Spécifier (22 min)

**Phases SDLC : Comprendre + Spécifier · Rôle en avant : 🧭 Porteur de vision**

### 5.1 Théorie — 8 min

**1. Explorer → Planifier → Coder, dans cet ordre.**
Laisser l'agent coder directement produit du code qui résout le mauvais problème. Le **plan mode** (`Shift+Tab` jusqu'à `⏸ plan mode on`) sépare l'exploration de l'exécution : lecture seule, aucun fichier modifié.

**2. Le prompt est une ancre sémantique.**
Quelques mots portent des pages d'intention. *« Fais-moi un Tetris »* ≈ 100 pages de spec — que l'agent va inventer si vous ne les écrivez pas. Le génie exauce vos mots, pas vos vœux.

**3. Faites-vous interviewer.**
Pour une feature non triviale, le meilleur prompt initial est minimal :

```
Je veux construire [description courte]. Interviewe-moi en détail.
Pose des questions sur l'implémentation technique, l'UX, les cas limites,
les inquiétudes et les arbitrages. Ne pose pas de questions évidentes,
creuse les points durs auxquels je n'ai pas pensé.
Continue jusqu'à ce qu'on ait tout couvert, puis écris une spec complète
dans SPEC.md.
```

Une bonne spec est **auto-portante** : elle nomme les fichiers et interfaces concernés, dit ce qui est **hors scope**, et se termine par une **vérification bout-en-bout** qui prouve que ça marche.

**4. Vos deux gates ici.**

| Gate | Question | Sortie |
|---|---|---|
| **Gate 1 — le problème** | « Oui, c'est bien le vrai problème qu'on résout » | Le besoin, en une phrase, validé |
| **Gate 2 — la spec** | « Les critères d'acceptation sont-ils nets et vérifiables ? » | `SPEC.md` accepté ou renvoyé |

**5. Le contexte est la ressource rare.**
La fenêtre de contexte se remplit vite et la qualité se dégrade quand elle se remplit. Une exploration non bornée (« investigue ce projet ») lit 200 fichiers et brûle la session. → borner, ou déléguer à un **sous-agent** qui explore dans son propre contexte et ne rend qu'un résumé.

**Sondage (30 s)** : *Vous donnez à l'agent une spec vague d'une ligne ; il construit exactement ça — et c'est faux. À qui la faute ?*
(a) à vous — l'agent construit la demande littérale ; resserrez la Gate 2 · (b) à l'agent · (c) à personne, Vérifier le rattrapera · (d) au modèle
→ **(a)**.

### 5.2 Pratique — 14 min

**Setup** : le porteur de vision tape, l'orchestrateur pilote le terminal.

| Étape | Durée | Consigne |
|---|---|---|
| **1. Explorer** | 4 min | `claude --permission-mode plan` puis : *« Donne-moi une vue d'ensemble de ce projet. Comment le statut d'une tâche est-il représenté et validé aujourd'hui ? Cite les fichiers. »* → noter **une** hypothèse que vous aviez et que le code contredit. |
| **2. Se faire interviewer** | 7 min | Coller le prompt d'interview ci-dessus avec la feature fil rouge (§9.3). Répondre honnêtement. L'agent écrit `SPEC.md`. |
| **3. Passe de gate croisée** ⏱️ | 3 min | Chaque binôme lit la `SPEC.md` du binôme voisin et doit trouver **un** trou : un cas limite non couvert, un critère non vérifiable, un scope non fermé. |

**Livrable** : `SPEC.md` versionné, avec au minimum — comportement attendu, 3 critères d'acceptation testables, une section « hors scope », une commande de vérification bout-en-bout.

**Critère de réussite** : la spec contient au moins une contrainte que le binôme n'avait **pas** en tête avant l'interview.

**Pièges du formateur**
- Un binôme qui répond « peu importe » à toutes les questions de l'agent → il aura une spec creuse ; c'est *l'occasion pédagogique*, ne la sauvez pas, montrez-la en partie 3.
- Ne laissez pas l'exploration déborder : à 4 min, `Esc`, on passe.
- Fournir une `SPEC.md` de secours dans le repo (`SPEC.reference.md`) pour que personne ne soit bloqué en partie 2.

---

## 6. Partie 2 — Construire (23 min)

**Phases SDLC : Construire (coder → vérifier → auto-corriger) · Rôle en avant : 🎛️ Orchestrateur**

### 6.1 Théorie — 7 min

**1. Donnez à l'agent un moyen de vérifier son travail.**
L'agent s'arrête quand le travail *a l'air* fini. Sans contrôle exécutable, « a l'air fini » est le seul signal disponible — et **vous** devenez la boucle de vérification. Donnez-lui quelque chose qui rend un pass/fail (suite de tests, code de sortie du build, linter, screenshot comparé) et la boucle se referme toute seule.

Quatre niveaux de dureté de la gate, par ordre de coût de mise en place :

| Niveau | Mécanisme | Ce que ça garantit |
|---|---|---|
| Dans le prompt | *« lance les tests et itère »* | Marche aujourd'hui, sur n'importe quelle tâche |
| Sur la session | `/goal` — un évaluateur re-vérifie à chaque tour | L'agent continue jusqu'à résolution |
| Déterministe | **Hook `Stop`** — un script bloque la fin du tour | Non contournable |
| Second avis | Sous-agent vérificateur en contexte frais | Le producteur ne se note pas lui-même |

**2. TDD orchestré : RED → GREEN → REFACTOR, chaque phase a un stop-gate observable.**
Retour de terrain : laissé libre, l'agent écrit les tests **à partir du code qu'il vient de générer**, pas à partir de la spec. Résultat : des trous dans les tests, et potentiellement dans le code.
Forcer l'ordre test-puis-code n'est pas du dogme TDD, c'est une **contrainte anti-complaisance**.

**3. Une seule gate humaine ici : le plan.**
Vous validez le plan (bons fichiers, pas de nouvelle dépendance, aucun garde-fou supprimé) — puis vous **pilotez sans valider chaque étape**. Regarder le stream, `Esc` sur dérive. Pas de gate obligatoire sur la boucle vérifier → auto-corriger : c'est précisément le bloc qu'on délègue, donc le filet en dessous doit être réel.

**4. Cappez le thrash.**
Deux comportements à interdire explicitement dans `CLAUDE.md` :
- retry infini sur un test rouge ;
- « j'ai modifié le test pour qu'il passe ».

**5. Les curseurs.** Modèle (`/model`) · effort (`/effort`) · autonomie (`Shift+Tab`) · contexte (`CLAUDE.md`). Objectif *correction* → modèle ↑, effort ↑, autonomie ↓, contexte ↑. Objectif *vitesse* → l'inverse.

**Quiz (30 s)** : *Votre agent dit « Terminé, j'ai lancé les tests, tout passe. » Est-ce une gate ?*
(a) oui · (b) oui si le modèle est assez puissant · (c) non, la gate est le rapport de test observable, pas la phrase · (d) non, seul un humain peut être une gate
→ **(c)**. La phrase est une *revendication*. La gate est l'artefact qu'elle produit, que vous **lisez** au lieu de le refaire.

### 6.2 Pratique — 16 min

**Bascule de rôles** : l'orchestrateur prend le clavier.

| Étape | Durée | Consigne |
|---|---|---|
| **1. Poser le filet** | 3 min | Ajouter au `CLAUDE.md` du repo le contrat fourni (§9.4) : ordre test-puis-code, `pytest` vert obligatoire après chaque change, interdiction de modifier un test pour le faire passer. Vérifier le chargement avec `/context`. |
| **2. Faire produire le plan, et le valider** | 3 min | *« Depuis SPEC.md, propose un plan d'implémentation : quels fichiers, quel ordre, quels tests d'abord. N'écris aucun code. »* → **la gate** : bons fichiers ? nouvelle dépendance ? garde-fou supprimé ? Approuver ou renvoyer. |
| **3. Lâcher la boucle** | 8 min | Sortir du plan mode, *« implémente le plan »*. **Consigne au binôme : ne pas intervenir tant que l'agent ne dérive pas.** Observer le RED → GREEN. |
| **4. Débrief éclair** ⏱️ | 2 min | Deux mains levées : « qui a vu l'agent tenter de contourner un test rouge ? » Lire la sortie à voix haute. |

**Livrable** : la feature implémentée, `pytest` vert, la sortie de test conservée comme preuve.

**Critère de réussite** : le binôme peut montrer un test qui a **échoué avant** de passer. Un GREEN sans RED préalable = le contrat n'a pas été respecté (c'est un excellent cas à exposer).

**Pièges du formateur**
- Le repo doit contenir un **bug volontaire** (§9.2) que la feature va révéler — sinon la partie 3 n'a rien à mordre.
- Un binôme qui approuve le plan sans le lire : c'est le cas d'école, notez-le pour la conclusion.
- Prévoir un temps mort : pendant les 8 min d'exécution, circulez, ne commentez pas depuis l'estrade.

---

## 7. Partie 3 — Vérifier (22 min)

**Phase SDLC : Vérifier · Rôle en avant : 🎛️ Orchestrateur (gate de revue + gate d'apprentissage)**

### 7.1 Théorie — 8 min

**1. Vert ≠ correct.**
Les tests verts sont **nécessaires, pas suffisants**. L'agent a prouvé que les tests passent ; seul vous pouvez juger qu'il a construit la **bonne chose**. La gate humaine revient ici, et elle est obligatoire.

Ce que le vert ne vous dit pas : scope qui a dérivé, garde-fou supprimé, spec respectée à la lettre mais pas dans l'esprit, dette ajoutée, dépendance introduite.

**2. Le producteur ne note pas sa copie.**
Un relecteur qui tourne dans un **contexte frais** (sous-agent) ne voit que le diff et vos critères — pas le raisonnement qui a produit le changement. Il évalue le résultat pour lui-même.

```
Utilise un sous-agent pour relire le diff par rapport à SPEC.md.
Vérifie que chaque exigence est implémentée, que les cas limites listés
ont un test, et que rien hors du scope de la tâche n'a changé.
Signale les écarts, pas les préférences de style.
```

**3. Attention au biais du relecteur.**
Un relecteur à qui on demande de trouver des trous en trouvera — même si le travail est sain. Chasser chaque remarque mène à la sur-ingénierie : couches d'abstraction inutiles, code défensif, tests pour des cas impossibles.
→ **Demandez-lui de ne signaler que ce qui affecte la correction ou une exigence explicite.** Le reste est optionnel.

**4. Consultatif vs déterministe.**

| | `CLAUDE.md` | Hook |
|---|---|---|
| Nature | Consultatif — l'agent *devrait* | Déterministe — le script *s'exécute* |
| Contournable | Oui, surtout si le fichier est long | Non |
| Pour quoi | Conventions, style, préférences | Ce qui doit arriver à chaque fois, sans exception |

**5. La gate d'apprentissage.**
Chaque écart trouvé ici est une information gratuite. Si vous ne l'encodez pas, vous le repayerez à chaque session. → transition vers la partie 4.

### 7.2 Pratique — 14 min

**Bascule de rôles** : le porteur de vision reprend le clavier pour la lecture du diff.

| Étape | Durée | Consigne |
|---|---|---|
| **1. Revue humaine d'abord** | 5 min | `git diff` **à la main**, sans agent. Objectif : trouver **un** écart avec `SPEC.md`. L'ordre compte — on veut que chacun ait sa propre liste avant de voir celle de la machine. |
| **2. Revue par sous-agent** | 6 min | Lancer le prompt de revue ci-dessus (ou `/code-review`). Comparer sa liste à la vôtre : qu'a-t-il vu que vous n'aviez pas ? Qu'avez-vous vu qu'il n'a pas ? |
| **3. Tri & vote** ⏱️ | 3 min | Classer chaque écart : **correction** (bloquant) / **exigence** (bloquant) / **style** (optionnel). Vote à main levée sur le nombre d'écarts *bloquants* trouvés par la machine seule vs par l'humain seul. |

**Livrable** : une liste d'écarts triée, avec au moins un écart classé « correction ».

**Critère de réussite** : le binôme identifie **au moins un écart que le sous-agent a raté** — c'est la démonstration en direct que la gate humaine n'est pas décorative.

**Pièges du formateur**
- Le bug volontaire du repo doit être du type que les tests ne détectent pas (§9.2). S'il est détecté par `pytest`, l'exercice perd son sens.
- Si un binôme n'a rien à relire (retard en partie 2), fournir une branche `demo/step-2-done` prête à relire.

---

## 8. Partie 4 — Livrer & Capitaliser (22 min)

**Phases SDLC : Opérer + le retour de boucle · Rôle : 🎛️ Orchestrateur**

### 8.1 Théorie — 8 min

**1. La gate humaine de commit.**
L'agent rédige, la CD livre — mais **vous restez responsable du code**. Rien n'atteint `main` sans une décision humaine. Corollaire opérationnel : ne mergez jamais du code que vous ne pouvez pas expliquer.

**2. Le miss devient une règle.**
L'écart trouvé en partie 3 a trois destins possibles :

| Destin | Quand | Coût |
|---|---|---|
| **`CLAUDE.md`** | Convention brève, applicable partout, à chaque session | Chargé à chaque session → coûte du contexte |
| **Skill** (`.claude/skills/`) | Savoir de domaine ou workflow qui ne sert que parfois | Chargé à la demande → gratuit le reste du temps |
| **Hook** | Ça doit arriver à chaque fois, sans exception | Déterministe, hors du LLM |

**3. `CLAUDE.md` n'est pas un fourre-tout.**
Test pour chaque ligne : *« est-ce que la retirer ferait faire une erreur à l'agent ? »* Si non, coupez.
Un fichier trop long **fait ignorer les règles importantes**, noyées dans le bruit. Si l'agent continue à faire une chose que vous avez interdite, le problème n'est pas la règle : c'est la longueur du fichier.

| ✅ Mettre | ❌ Ne pas mettre |
|---|---|
| Commandes bash non devinables | Ce que l'agent trouve en lisant le code |
| Conventions qui diffèrent du défaut | Conventions standard du langage |
| Instructions de test, runner préféré | Doc d'API détaillée (mettre un lien) |
| Étiquette du repo (branches, PR) | Info qui change souvent |
| Décisions d'archi du projet | « écrire du code propre » |

**4. Un Skill, c'est un workflow qu'on publie.**
Trois lignes de frontmatter + une procédure. `/review-task` tourne pour vous **et pour tous ceux qui pull le repo**. C'est le passage du prompt jetable à **l'actif d'équipe**.

**5. La logique vit dans le Markdown, pas dans l'outil.**
Un workflow écrit dans un `.md` versionné survit au changement de CLI. Le fichier CLI (`.claude/skills/x/SKILL.md`) n'est qu'un adaptateur mince qui pointe vers la procédure de référence. Portabilité par construction.

**6. Le contexte est du capital d'équipe.**
Versionné dans git, diffable, relu en PR — pas un setup personnel sur une machine. C'est ce qui fait qu'un nouvel arrivant, **humain ou agent**, démarre du même point.

### 8.2 Pratique — 14 min

| Étape | Durée | Consigne |
|---|---|---|
| **1. Commit & PR** | 4 min | *« Commite avec un message descriptif et ouvre une PR. »* Puis **relire le message avant de valider** : décrit-il le *pourquoi* ou juste le *quoi* ? Corriger si besoin. C'est la gate. |
| **2. Encoder le miss** | 6 min | Prendre l'écart classé « correction » en partie 3 et le transformer, au choix : une règle de 1-2 lignes dans `CLAUDE.md`, **ou** un Skill `/review-task` (squelette fourni §9.5). Choisir en justifiant avec le tableau ci-dessus. |
| **3. Test de non-régression du contexte** ⏱️ | 4 min | `/clear` pour repartir d'un contexte vierge, puis lancer une tâche voisine (§9.3, variante). **L'agent respecte-t-il la nouvelle règle sans qu'on la lui rappelle ?** Si oui, vous venez de capitaliser. Si non, la règle est mal écrite ou le fichier est trop long. |

**Livrable** : une PR ouverte + un `CLAUDE.md` (ou un Skill) enrichi d'une règle issue d'un vrai miss.

**Critère de réussite** : à l'étape 3, la règle tient sans rappel. Un échec ici est un **excellent** résultat pédagogique — il prouve la thèse « `CLAUDE.md` se traite comme du code : on le relit, on l'élague, on teste que le comportement bouge vraiment ».

**Pièges du formateur**
- Interdire les règles vagues du type « faire attention aux cas limites ». Exiger une formulation testable.
- L'étape 3 est le vrai moment « aha » de la session. Si vous devez couper quelque chose ailleurs, protégez ces 4 minutes.

---

## 9. Le repo fil rouge — cahier des charges

### 9.1 Choix du projet

**`taskboard-workshop`** — une petite API de gestion de tâches.

Justification pour un public mixte : le domaine est compris par tout le monde en 10 secondes (une tâche a un titre et un statut), donc **le non-tech peut tenir la Gate 2 sans aide**. Le débat porte sur les règles métier, pas sur la syntaxe.

### 9.2 Contenu attendu

```
taskboard-workshop/
├── README.md                 # 15 lignes max : lancer, tester
├── CLAUDE.md                 # volontairement MINIMAL (voir §9.4)
├── SPEC.reference.md         # spec de secours pour les binômes en retard
├── check-setup.sh            # affiche "SETUP OK" ou le problème exact
├── src/
│   └── taskboard/
│       ├── models.py         # Task : id, title, status, assignee
│       ├── store.py          # persistance en mémoire
│       └── api.py            # FastAPI : GET /tasks, POST /tasks, GET /tasks/{id}
├── tests/
│   ├── test_api.py           # ~12 tests, tous verts au clone
│   └── test_store.py
└── .github/workflows/ci.yml  # pytest + ruff
```

**Contraintes de conception :**

| # | Contrainte | Pourquoi |
|---|---|---|
| 1 | ~300 lignes de code max, ~200 de tests | Lisible en 4 min à l'étape « Explorer » |
| 2 | `pytest` **vert** au clone, en < 5 secondes | Aucune friction au démarrage ; feedback loop rapide en partie 2 |
| 3 | Aucune dépendance externe hors `fastapi`, `pytest`, `ruff` | Installation offline possible |
| 4 | Le statut est une `str` libre, **pas** un `Enum` | C'est **le bug volontaire** — voir ci-dessous |
| 5 | `CLAUDE.md` fourni ne contient **que** les commandes de build/test | La partie 2 consiste précisément à l'enrichir |
| 6 | Une branche `demo/step-2-done` avec la feature implémentée | Filet de sécurité pour la partie 3 |

**Le bug volontaire (contrainte 4)** — `store.py` accepte n'importe quelle chaîne comme statut. Il existe déjà une tâche de seed avec le statut `"Done"` (majuscule) alors que le reste du code compare à `"done"`. Aucun test ne couvre ce cas.

Propriétés recherchées :
- ✅ Invisible dans les tests verts → prouve « vert ≠ correct » en partie 3 ;
- ✅ Trouvable par lecture attentive du diff en 5 min ;
- ✅ Souvent raté par un sous-agent relecteur focalisé sur le diff → permet le critère de réussite de la partie 3 ;
- ✅ Se corrige en une règle `CLAUDE.md` de 2 lignes en partie 4 : *« Les statuts valides sont exactement `todo` / `doing` / `done`, en minuscules. Toute valeur hors de cet ensemble est un bug, pas une donnée à supporter. »*

### 9.3 La feature fil rouge

> **Énoncé donné aux participants (partie 1)**
>
> *Aujourd'hui, on peut créer une tâche et la lire. On ne peut pas faire avancer une tâche dans le board. Ajoutez la possibilité de changer le statut d'une tâche — avec des règles : on ne saute pas d'étape, et une tâche terminée ne revient pas en arrière.*

Volontairement **sous-spécifié**. C'est le point : les questions que l'agent va poser pendant l'interview (que faire d'un statut inconnu ? d'une transition interdite ? quel code HTTP ? faut-il tracer qui a changé le statut ?) sont exactement les décisions que la Gate 2 doit produire.

**Variante pour la partie 4, étape 3** (contexte vierge) :
> *Ajoutez un endpoint qui renvoie le nombre de tâches par statut.*
L'agent va devoir manipuler l'ensemble des statuts valides — donc appliquer, ou non, la règle qu'on vient d'encoder.

### 9.4 Le `CLAUDE.md` — état initial et contrat à ajouter

**Fourni au clone (minimal, volontairement) :**

```markdown
# taskboard-workshop

## Commandes
- Tests : `pytest -q`
- Lint : `ruff check src tests`
- Lancer l'API : `uvicorn taskboard.api:app --reload`
```

**Le contrat à ajouter en partie 2, étape 1 (fourni sur slide, à copier) :**

```markdown
## Workflow
- Écris le test AVANT le code. Le test doit échouer, et tu dois montrer
  cet échec, avant d'écrire l'implémentation.
- Après toute modification, lance `pytest -q`. Ne considère pas la tâche
  finie tant que la suite n'est pas verte.
- IMPORTANT : ne modifie JAMAIS un test pour le faire passer. Si un test
  échoue, le code est faux — ou le test est faux et tu me le signales.
- Après 3 tentatives infructueuses sur le même échec, arrête-toi et
  explique ce que tu as essayé.
```

Faire remarquer en séance : **4 lignes**, chacune passe le test « est-ce que la retirer ferait faire une erreur à l'agent ? ».

### 9.5 Squelette de Skill (partie 4, étape 2)

```markdown
---
name: review-task
description: Relit un diff sur taskboard par rapport à SPEC.md et aux règles métier du board
---

Relis le diff courant.

1. Chaque critère d'acceptation de SPEC.md est-il implémenté ET testé ?
2. Les statuts manipulés sont-ils tous dans l'ensemble valide ?
3. Un garde-fou existant a-t-il été supprimé ou affaibli ?
4. Quelque chose hors du scope de la tâche a-t-il changé ?

Signale uniquement ce qui affecte la correction ou une exigence explicite.
Ne signale pas de préférences de style. Cite les fichiers et les lignes.
```

---

## 10. Conclusion & Q&A — 13 min

### 10.1 Récapitulatif : la carte des gates (3 min)

Une seule slide, celle qu'on emporte :

```
 Comprendre & Spécifier      Construire           Vérifier          Livrer
    Explorer · Planifier   Coder·Vérifier·Corriger  Relire le diff   Commit · CD

  🤖 propose et challenge    🤖 planifie et code   🤖 lance les checks  🤖 rédige
  🧑 répond et décide        🧑 valide le plan     🧑 lit le diff       🧑 décide

  🔒 Gate 1 : le problème    🔒 Gate 3 : le plan   🔒 Gate 4 : la revue  🔒 Gate 5 : le commit
  🔒 Gate 2 : la spec                              ↩︎ et on encode le miss
```

> Gardez l'avant (là où l'amplification est maximale) et l'arrière (avant que ça touche `main`). Au milieu, laissez tourner — c'est là qu'est la vitesse.

### 10.2 Les trois questions boussole (2 min)

| Question | Réponse de la session |
|---|---|
| **Par où je commence ?** | Lundi matin : `/init` sur un repo, et j'y écris **une** règle issue d'un vrai miss. |
| **Quel est mon rôle ?** | Porteur de vision à l'avant, orchestrateur à l'arrière. Pas auteur de prompts. |
| **Qu'est-ce qui change concrètement ?** | J'écris les critères d'acceptation avant le code, et je ne merge rien que je ne peux pas expliquer. |

### 10.3 L'engagement (2 min)

Chaque participant écrit **une** action, dans le chat ou sur un post-it :
*« Cette semaine, j'ajoute ______ à mon `CLAUDE.md` / je pose ______ comme gate déterministe. »*

Effet mesurable, pas de badge. Relancer à 2 semaines.

### 10.4 Pour aller plus loin (1 min)

- Orchestration multi-agents et sous-agents spécialisés
- Sessions parallèles (worktrees), pattern Writer/Reviewer
- MCP : connecter l'agent au SI (Jira → PR)
- Le mur du contexte : `context rot`, compaction, quand découper
- Gouvernance : plugins, Skills partagés, politique d'équipe versionnée

### 10.5 Q&A — 5 min

**Questions à préparer (elles tombent presque toujours) :**

| Question | Angle de réponse |
|---|---|
| « Ça coûte combien ? » | Le coût est dominé par le contexte. Lire une preuve coûte moins cher que refaire le travail. Le caching et le routage de modèle avant tout le reste. |
| « Est-ce que ça remplace les devs ? » | La partie 3 d'aujourd'hui a montré le contraire : l'écart bloquant a été trouvé par un humain. Ce qui se déplace, c'est la valeur — vers les deux extrémités de la boucle. |
| « Et le code propriétaire / la conformité ? » | Sujet à part entière : résidence des données, périmètre des outils, ce qui sort du réseau. À traiter avec votre politique interne, pas en Q&A. |
| « On fait comment sur un monorepo de 2 M de lignes ? » | Hiérarchie de fichiers de contexte, exploration déléguée à des sous-agents, indexation structurelle. C'est le sujet d'une session dédiée. |
| « Et si l'agent se trompe en prod ? » | La question de la gate, encore : rien n'atteint `main` sans décision humaine, et le filet déterministe tourne en CI, pas dans le LLM. |

---

## 11. Checklist formateur

### J-7
- [ ] Repo `taskboard-workshop` créé, `pytest` vert, `check-setup.sh` testé sur macOS/Windows/Linux
- [ ] Branche `demo/step-2-done` poussée
- [ ] `SPEC.reference.md` rédigée
- [ ] Bug volontaire vérifié : invisible aux tests, trouvable à l'œil

### J-2
- [ ] Mail de prérequis envoyé (installation + clone + `SETUP OK`)
- [ ] Canal de support setup ouvert
- [ ] Slides prêtes ; les 4 prompts à copier sont sur des slides **dédiées et lisibles au fond de la salle**

### J-0, avant la session
- [ ] Répétition à blanc du parcours complet chronométré (le vrai risque, c'est la partie 2)
- [ ] 2 machines de secours préconfigurées
- [ ] Codespace / devcontainer de secours en ligne
- [ ] Prompts copiables aussi dans un gist / doc partagé (le copier-coller depuis une slide ne marche pas)
- [ ] Quotas / accès API vérifiés pour le nombre de binômes attendus

### Pendant
- [ ] Binômes formés pendant la slide « société », pas après
- [ ] Un chronomètre visible de tous
- [ ] Circuler pendant les blocs pratiques, ne pas commenter depuis l'estrade
- [ ] Noter 2-3 anecdotes de salle à réutiliser en conclusion (elles valent mieux que n'importe quelle slide)

---

## 12. Sources

### Documentation Anthropic
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) — vérification, explore/plan/code, `CLAUDE.md`, sous-agents, revue adversariale
- [Common workflows](https://code.claude.com/docs/en/common-workflows) — recettes de prompts, plan mode, worktrees
- [Claude Code overview](https://code.claude.com/docs/en/overview) — surfaces, installation, capacités
- [CLAUDE.md / memory](https://code.claude.com/docs/en/memory) · [Skills](https://code.claude.com/docs/en/skills) · [Hooks](https://code.claude.com/docs/en/hooks) · [Subagents](https://code.claude.com/docs/en/sub-agents) · [Permission modes](https://code.claude.com/docs/en/permission-modes)

### Documentation interne (`docs/`)
- *AI Foundations · Module 3 — Complete Agentic Workflow* : le canevas 5 phases, les thèses amplificateur/levier, les deux rôles, la carte délégation/gates
- *AI Foundations · Module 2* : les 4 curseurs (modèle, effort, autonomie, contexte)
- *AI Foundations · Module 1* : limites des LLM (perroquet, cerveau sans mains, Memento), boucle ReAct
- *AI Foundations · Module 4* : pratique responsable, HITL vs auto-pilot
- *AI Fluent 1 · Modules 1, 2, 4* : contexte versionné, `AGENTS.md`/`CLAUDE.md`, Skills et profils agentiques
- *AI Fluent 2 · Module 1* : Planner / Executor / Verifier, le vérificateur indépendant, la gate déterministe
- *AI Fluent 2 · Module 5* : TDD orchestré en Markdown, stop-gates observables, `context rot`, portabilité multi-CLI
