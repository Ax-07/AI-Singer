
# Ai-Singer

[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE) [![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

## Description

Ai-Singer est une application Python pour la synthèse et l'entraînement d'une voix chantée (projet de type « AI singer »). Le dépôt contient des utilitaires de prétraitement audio, des scripts d'entraînement pour le modèle acoustique et le vocodeur, ainsi qu'un moteur d'inférence pour générer des fichiers audio.

## Prérequis

- Python 3.8 ou plus récent
- Un environnement virtuel (`venv`) recommandé
- Dépendances listées dans `requirements.txt`

## Installation rapide

1. Cloner le dépôt:

```powershell
git clone [<repo-url>](https://github.com/Ax-07/AI-Singer.git)
cd Ai-Singer
```

1. Créer et activer un environnement virtuel (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

1. Installer les dépendances:

```powershell
pip install -r requirements.txt
```

## Utilisation (exemples)

- Lancer l'application principale (pour tests rapides):

```powershell
python -m app.main
```

- Prétraiter le dataset (exemple):

```powershell
python scripts/preprocess_audio.py --input-dir data/raw --output-dir data/processed
```

- Extraire les caractéristiques audio:

```powershell
python scripts/build_features.py --data-dir data/processed --out features/
```

- Entraîner le modèle acoustique:

```powershell
python scripts/train_acoustic_model.py --config configs/acoustic.yml
```

- Entraîner le vocodeur:

```powershell
python scripts/train_vocoder.py --config configs/vocoder.yml
```

- Inférence locale (générer un fichier WAV à partir d'un texte):

```powershell
python scripts/infer_local.py --input "Ma phrase à chanter" --out generated/output.wav
```

## Structure du dépôt (résumé)

- `app/` : code principal
  - `app/main.py` : point d'entrée pour tests/usage rapide
  - `app/singer_engine.py` : moteur d'inférence
  - `app/audio_utils.py` : utilitaires audio
  - `app/models.py` : définitions de modèles (si présentes)
- `data/` : données et métadonnées (voir `data/metadata/`)
- `generated/` : sorties (audio, checkpoints)
- `scripts/` : scripts utiles (`preprocess_audio.py`, `build_features.py`, `train_acoustic_model.py`, `train_vocoder.py`, `infer_local.py`, ...)
- fichiers racine : `requirements.txt`, `GUIDE.md`, `ROADMAP.md`, `test_fake.py`, `test_request.py`

## Workflows conseillés

1. Préparer et valider les métadonnées dans `data/metadata/`.
1. Prétraiter les WAVs avec `scripts/preprocess_audio.py`.
1. Extraire les features via `scripts/build_features.py`.
1. Entraîner le modèle acoustique puis le vocodeur.
1. Faire de l'inférence locale avec `scripts/infer_local.py`.

## Tests

Lancer les tests disponibles (si `pytest` est installé):

```powershell
python -m pytest
```

ou exécuter les scripts de test présents:

```powershell
python test_fake.py
python test_request.py
```

## Contribuer

Merci pour l'intérêt ! Pour contribuer :

1. Forker le dépôt et créer une branche `feature/xxx`.
1. Ajouter des commits clairs et tests si possible.
1. S'assurer que les scripts et le code suivent la même convention (PEP8 pour Python).
1. Ouvrir une Pull Request décrivant les changements.

Voir `CONTRIBUTING.md` pour plus de détails.

## Licence

Ce projet est distribué sous licence MIT — voir le fichier `LICENSE`.

## Contact / Support

Ouvrez une issue pour signaler un bug ou demander une fonctionnalité. Pour aide directe, mentionnez le module concerné (`app/singer_engine.py`, `scripts/*`, etc.).

## Remarques finales

- Adaptez les chemins et arguments des scripts selon votre configuration locale.
- Les données audio sont volumineuses — prévoir suffisamment d'espace disque et (si entraînement) un GPU.
- Remplacez les badges avec les URLs réelles du dépôt (`<OWNER>/<REPO>`).
