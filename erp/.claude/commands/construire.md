---
description: Temps 2 · Construire tranche par tranche, tests d'abord, avec preuve réelle.
argument-hint: <specs/feature.md>
---

Tu construis la feature décrite dans `$ARGUMENTS`. Rôle : Dev.

Préalable : lis la spec. Si les deux gates « Cadrage » ne sont pas cochés (`- [x]`), refuse de démarrer, dis lequel manque et arrête-toi. Ne les coche jamais toi-même.

1. Crée la branche `feat/<slug>` depuis `main`.
2. Relis `AGENTS.md`, notamment la section « Preuve » : ce sont les commandes de preuve à utiliser.
3. Pour chaque tranche du Plan, dans l'ordre :
   1. traduis ses scénarios en tests Playwright dans `e2e/`, avec l'id du scénario dans le titre (`S1 : …`) ;
   2. lance-les et montre qu'ils échouent, pour la bonne raison ;
   3. implémente le minimum pour les faire passer ;
   4. lance les commandes de preuve d'`AGENTS.md` ;
   5. fais un commit pour la tranche.
4. Colle dans la section « Preuve » de la spec : les commandes lancées, le résumé et la fin de la sortie réelle. Rien de reformulé ni d'inventé.

Règles dures :
- Ne modifie jamais un test existant pour le faire passer. Si un test te semble faux, arrête-toi et demande à l'humain.
- Si un scénario est ambigu ou manquant, arrête-toi et demande : ne le tranche pas seul.
- Reste dans le Plan : toute dérive est signalée, pas silencieusement absorbée.

À la fin : dis de passer la main au Reviewer, qui lance `/relire $ARGUMENTS` dans une nouvelle session (`/clear` ou nouveau terminal).
