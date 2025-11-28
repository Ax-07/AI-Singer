import json
import sys
from types import SimpleNamespace

try:
    from app.singer_engine import render_singer_fake
    from app.audio_utils import save_wave
except Exception as e:
    print(json.dumps({"error": "import_failed", "message": str(e)}))
    sys.exit(1)

# Test payload
notes = [
    SimpleNamespace(start_time=0.0, duration=0.5, pitch_midi=60),
    SimpleNamespace(start_time=0.5, duration=0.5, pitch_midi=62),
    SimpleNamespace(start_time=1.0, duration=0.5, pitch_midi=64),
    SimpleNamespace(start_time=1.5, duration=1.0, pitch_midi=67),
]

req = SimpleNamespace(sample_rate=44100, bpm=120.0, notes=notes, lyrics="la la la")

try:
    audio = render_singer_fake(req)
except Exception as e:
    print(json.dumps({"error": "render_failed", "message": str(e)}))
    sys.exit(1)

filename = "rendered_clip_test.wav"

# Try the project's save_wave first, fallback to a simple writer if needed
rel_path = None
try:
    rel_path = save_wave(audio, req.sample_rate, filename)
except Exception as e:
    # fallback: try using wave + struct (requires numpy for fast conversion)
    try:
        import wave
        import struct
        import numpy as np

        ints = (audio * 32767).astype(np.int16)
        out_path = filename
        with wave.open(out_path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(req.sample_rate)
            wf.writeframes(ints.tobytes())
        rel_path = out_path
    except Exception as e2:
        print(
            json.dumps(
                {"error": "save_failed", "message": str(e), "fallback_error": str(e2)}
            )
        )
        sys.exit(1)

duration = len(audio) / req.sample_rate
print(json.dumps({"audio_url": rel_path, "duration": duration}))
