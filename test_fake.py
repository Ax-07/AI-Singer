import sys
from pathlib import Path

# Ajoute la racine du projet au PYTHONPATH
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.models import Note, RenderRequest
from app.singer_engine import render_singer
from app.audio_utils import save_wave


def main():
    notes = [
        Note(start_time=0.0, duration=0.5, pitch_midi=60),
        Note(start_time=0.5, duration=0.5, pitch_midi=62),
        Note(start_time=1.0, duration=0.5, pitch_midi=64),
        Note(start_time=1.5, duration=1.0, pitch_midi=67),
    ]

    req = RenderRequest(
        sample_rate=44100,
        bpm=120,
        notes=notes,
        lyrics="la la la",
    )

    audio = render_singer(req, mode="fake")
    out_path = save_wave(audio, req.sample_rate, "test_fake.wav")
    print("Fichier généré :", out_path)


if __name__ == "__main__":
    main()
