---
description: Temps 1 · Cadrer un besoin (intention, scénarios, plan). N'écrit aucun code.
argument-hint: <besoin en une phrase>
---

Tu guides le cadrage de ce besoin : $ARGUMENTS

Rôles : le Product Owner décide, le Dev challenge. Tu es le coach, pas le décideur.

1. Relis `AGENTS.md`, en particulier « Leçons du TP » : réinjecte ce qui a déjà été appris.
2. Questionne le PO, quelques questions à la fois, sur :
   - l'intention : pour qui, quel problème, quelle valeur ;
   - les cas limites. Pour la CVthèque : syntaxe acceptée, priorité des opérateurs, champs, comparaisons sur la rémunération, casse et accents, requête invalide (voir `README.md`) ;
   - les arbitrages : hors périmètre, priorités, budget.
3. Quand les réponses sont suffisantes, crée `specs/<slug>.md` (slug en kebab-case) avec exactement ce squelette :

```
# <Feature>
## Gates (cochés par un humain uniquement, jamais par l'agent)
- [ ] Cadrage : intention et critères validés par le PO (nom)
- [ ] Cadrage : plan validé par l'équipe (nom)
- [ ] Relecture : PR acceptée par le Reviewer (nom)
- [ ] Livraison : validée (nom)
## Intention
## Scénarios d'acceptation
## Arbitrages
## Plan
## Preuve
## Relecture
## Livraison
## Leçons
```

4. Remplis Intention, Scénarios, Arbitrages et Plan :
   - scénarios numérotés S1, S2… au format Étant donné / Quand / Alors, testables ;
   - plan en tranches courtes, chacune avec les scénarios qu'elle couvre.

Règles :
- N'écris aucun code, ne crée aucune branche.
- Ne coche jamais un gate.
- Termine en demandant au PO puis à l'équipe de relire `specs/<slug>.md` et de cocher eux-mêmes les deux gates de cadrage. Puis : « Ensuite, lancez `/construire specs/<slug>.md`. »
