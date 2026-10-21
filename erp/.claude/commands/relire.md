---
description: Temps 2 · Relecture indépendante, à lancer dans une session neuve.
argument-hint: <specs/feature.md>
---

Tu relis la feature de `$ARGUMENTS`. Rôle : Reviewer.

Avant tout, demande de confirmer que cette session est neuve (`/clear` ou nouveau terminal). Si ce n'est pas le cas, arrête-toi : un agent qui a écrit le code ne peut pas le juger. N'avance qu'après confirmation.

1. Lis la spec, puis `git diff main...HEAD`. Ne te fie pas à la section « Preuve » : ce n'est qu'une déclaration.
2. Vérifie que chaque scénario (S#) a son test, et que ce test dit la même chose que le scénario (pas un test vidé ou trop permissif).
3. Cherche les tests modifiés après leur création : `git log -p -- e2e/`. Signale toute modification d'assertion.
4. Relance toi-même les commandes de la section « Preuve » d'`AGENTS.md` et compare avec ce qui est annoncé.
5. Contrôle aussi :
   - les conventions d'`AGENTS.md` ;
   - la taille de la PR (relisable ? sinon propose de la découper) ;
   - la sécurité : parsing de la requête, entrée invalide → message lisible et bon code HTTP.
6. Écris la section « Relecture » de la spec : constats (avec fichier:ligne et sorties réelles) et une proposition de verdict.

Règles :
- Ne corrige pas le code : tu constates. Les corrections repartent vers le Dev.
- Ne coche jamais le gate « Relecture » : la décision revient au Reviewer humain.

À la fin : demande au Reviewer de trancher et de cocher le gate lui-même. Puis : « Ensuite, lancez `/livrer $ARGUMENTS`. »
