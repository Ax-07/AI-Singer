# Contribuer au projet Ai-Singer

Merci pour votre intérêt à contribuer ! Voici quelques lignes directrices pour faciliter les contributions.

Processus de contribution

- Forkez le dépôt et créez une branche `feature/ma-fonctionnalite` ou `fix/ma-correction`.
- Développez votre fonctionnalité/localement et ajoutez des tests si possible.
- Respectez les conventions de code (PEP8 pour Python). Utilisez `black`/`flake8` si disponibles.
- Faites un commit clair et atomique, puis poussez votre branche.
- Ouvrez une Pull Request décrivant le changement, l'objectif, et les tests effectués.

Tests et vérifications

- Si le projet utilise `pytest`, assurez-vous que les tests locaux passent :

```powershell
python -m pytest
```

- Documentez tout nouvel argument de script ou option de configuration.

Style et bonnes pratiques

- Utilisez des messages de commit clairs : "feat: add X", "fix: correct Y".
- Ajoutez des tests unitaires pour les comportements importants.
- Pour les modifications touchant les modèles ou la data, décrivez l'impact sur les entrées/sorties.

Problèmes connus et reporting

- Ouvrez une issue si vous découvrez un bug; fournissez un minimal repro et l'environnement (OS, Python, versions des packages).

Licence

- En soumettant une PR, vous acceptez que votre contribution sera placée sous la licence du projet (voir `LICENSE`).

Merci !
