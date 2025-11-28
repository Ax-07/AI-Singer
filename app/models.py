from pydantic import BaseModel
from typing import List, Optional


class Note(BaseModel):
    """
    Une note MIDI avec timing en secondes.
    """
    start_time: float  # début en secondes
    duration: float    # durée en secondes
    pitch_midi: int    # 60 = C4, 69 = A4 = 440 Hz


class RenderRequest(BaseModel):
    """
    Requête de rendu de chant :
    - notes : séquence de notes
    - lyrics : texte/ paroles (optionnel)
    - voice_id : plus tard si tu as plusieurs voix
    """
    sample_rate: int = 44100
    bpm: float = 120.0
    notes: List[Note]
    lyrics: Optional[str] = None
    voice_id: Optional[str] = "default"


class RenderResult(BaseModel):
    """
    Structure logique pour documenter le résultat.
    Pas utilisée directement dans les scripts,
    mais pratique si tu fais une API plus tard.
    """
    sample_rate: int
    duration: float
