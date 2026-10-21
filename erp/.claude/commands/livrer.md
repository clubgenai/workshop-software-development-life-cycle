---
description: Temps 3 · Préparer la livraison (changelog, rollback, indicateurs, PR).
argument-hint: <specs/feature.md>
---

Tu prépares la livraison de `$ARGUMENTS`. Rôles : Dev, avec Ops/PO.

Préalable : si le gate « Relecture » n'est pas coché (`- [x]`) dans la spec, refuse et arrête-toi. Ne le coche jamais toi-même.

1. Rédige la section « Livraison » :
   - un changelog lisible par un utilisateur ;
   - une checklist de mise en production ;
   - un rollback : `git revert` du merge, et ce qu'il faut vérifier après ;
   - le retrait éventuel de l'existant qu'on remplace (ou « rien à retirer ») ;
   - 1 ou 2 indicateurs d'usage à observer (ex. part de requêtes invalides). Écrits seulement : n'ajoute aucune instrumentation ;
   - le coût de la session : demande à l'humain de coller la sortie de `/cost`.
2. Prépare la description de PR (contexte, scénarios couverts, preuve, rollback).
3. `git push` et `gh pr create` : seulement après confirmation explicite de l'humain. Sinon, affiche les commandes sans les lancer.

Termine en demandant à l'humain de cocher lui-même le gate « Livraison ». Puis : « Ensuite, lancez `/capitaliser $ARGUMENTS`. »
