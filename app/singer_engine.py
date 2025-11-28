import numpy as np
import torch
from pathlib import Path

from .models import RenderRequest


###############################################
# 1. UTILITAIRES DE BASE
###############################################

def midi_to_freq(midi: int) -> float:
    """
    Convertit une note MIDI en fréquence (Hz).
    """
    return 440.0 * (2 ** ((midi - 69) / 12))


###############################################
# 2. MOTEUR FAKE (sinus)
###############################################

def render_singer_fake(req: RenderRequest) -> np.ndarray:
    """
    Génère un signal audio simple basé sur des sinusoïdes,
    en utilisant uniquement les notes MIDI.
    Sert pour tester la pipeline sans IA.
    """
    sr = req.sample_rate

    # Aucun son si pas de notes
    if not req.notes:
        return np.zeros(int(sr * 1), dtype=np.float32)

    # Durée totale = fin de la dernière note
    total_duration = max(n.start_time + n.duration for n in req.notes)
    total_samples = int(total_duration * sr)

    # Buffer audio final
    audio = np.zeros(total_samples, dtype=np.float32)

    # Construire la piste à partir de sinusoïdes simples
    for note in req.notes:
        start_sample = int(note.start_time * sr)
        end_sample = int((note.start_time + note.duration) * sr)

        if end_sample > total_samples:
            end_sample = total_samples

        # Temps local pour la note
        duration = (end_sample - start_sample) / sr
        t = np.linspace(0, duration, end_sample - start_sample, endpoint=False)

        # Hauteur = fréquence convertie du MIDI
        freq = midi_to_freq(note.pitch_midi)

        # Onde simple (harmonique pure)
        tone = 0.2 * np.sin(2 * np.pi * freq * t).astype(np.float32)

        audio[start_sample:end_sample] += tone

    # Normalisation / évite clipping
    max_val = np.max(np.abs(audio))
    if max_val > 1e-6:
        audio = audio / max(1.0, max_val)

    return audio


###############################################
# 3. PLACEHOLDER IA (sera rempli après training)
###############################################

_acoustic_model = None
_vocoder = None
_models_loaded = False


def load_models():
    """
    Charge les modèles IA (acoustic + vocoder).
    À modifier quand tu auras entraîné les modèles.
    """
    global _acoustic_model, _vocoder, _models_loaded

    if _models_loaded:
        return

    MODEL_DIR = Path("models/exported")

    # POINT D’ENTRÉE À MODIFIER APRÈS TRAINING
    acoustic_path = MODEL_DIR / "acoustic.pt"
    vocoder_path = MODEL_DIR / "vocoder.pt"

    if acoustic_path.exists():
        _acoustic_model = torch.load(acoustic_path, map_location="cpu")
        _acoustic_model.eval()
    else:
        print("[INFO] Aucun modèle acoustique trouvé. Mode IA indisponible.")

    if vocoder_path.exists():
        _vocoder = torch.load(vocoder_path, map_location="cpu")
        _vocoder.eval()
    else:
        print("[INFO] Aucun vocodeur trouvé. Mode IA indisponible.")

    _models_loaded = True


def prepare_inputs(req: RenderRequest):
    """
    Convertit les notes + paroles en format compatible IA.
    Le contenu exact dépendra de ton modèle.
    Ici on met juste des placeholders.

    À compléter quand le modèle IA sera entraîné :
    - tokenizer phonétique
    - F0 par frame
    - durées phonémiques
    """
    raise NotImplementedError(
        "prepare_inputs(req) doit être implémenté lorsque le modèle IA "
        "sera prêt."
    )


def render_singer_ai(req: RenderRequest) -> np.ndarray:
    """
    Version IA de la génération vocale.
    Utilise :
    - un modèle acoustique
    - un vocodeur
    pour produire du chant réaliste.
    """
    load_models()

    if _acoustic_model is None or _vocoder is None:
        raise RuntimeError(
            "Les modèles IA ne sont pas chargés. "
            "Assure-toi d'avoir exporté acoustic.pt et vocoder.pt "
            "dans models/exported/"
        )

    # Données d'entrée pour le modèle (phonèmes, F0, durées)
    phonemes, f0_curve, durations = prepare_inputs(req)

    # Inférence modèle acoustique → mel-spectrogramme
    with torch.no_grad():
        mel = _acoustic_model(phonemes, f0_curve, durations)

    # Inférence vocodeur → waveform audio
    with torch.no_grad():
        audio = _vocoder(mel)

    # Conversion Tensor → Numpy
    audio_np = audio.cpu().numpy().astype("float32").flatten()
    return audio_np


###############################################
# 4. DISPATCH (choisir fake ou IA)
###############################################

def render_singer(req: RenderRequest, mode: str = "fake") -> np.ndarray:
    """
    Appelle soit :
    - render_singer_fake (sinus)
    - render_singer_ai (IA)
    """
    if mode == "fake":
        return render_singer_fake(req)

    elif mode == "ai":
        return render_singer_ai(req)

    else:
        raise ValueError(f"Mode inconnu: {mode}")
