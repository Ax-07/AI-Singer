import numpy as np
import soundfile as sf
from pathlib import Path

# Racine du projet = dossier au-dessus de app/
BASE_DIR = Path(__file__).resolve().parent.parent
GENERATED_DIR = BASE_DIR / "generated"
GENERATED_DIR.mkdir(exist_ok=True)


def save_wave(audio: np.ndarray, sample_rate: int, filename: str) -> str:
    """
    Sauvegarde un tableau numpy 1D ou 2D (mono/stéréo) en WAV
    dans le dossier generated/.
    Retourne le chemin absolu sous forme de string.
    """
    path = GENERATED_DIR / filename
    sf.write(path, audio, sample_rate)
    return str(path)
