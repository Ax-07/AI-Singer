from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

RAW_DIR = Path("data/raw")
PROC_DIR = Path("data/processed/wav")
PROC_DIR.mkdir(parents=True, exist_ok=True)

TARGET_SR = 22050  # tu peux mettre 44100 si tu préfères


def main():
    wav_files = sorted(RAW_DIR.glob("*.wav"))
    if not wav_files:
        print("Aucun fichier .wav trouvé dans data/raw/")
        return

    for wav_path in wav_files:
        print("Traitement :", wav_path.name)

        # charge audio avec librosa
        audio, sr = librosa.load(wav_path, sr=None, mono=True)

        # resample
        if sr != TARGET_SR:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)
            sr = TARGET_SR

        # normalisation simple (optionnelle)
        max_val = np.max(np.abs(audio))
        if max_val > 1e-6:
            audio = audio / max_val * 0.99

        out_path = PROC_DIR / wav_path.name
        sf.write(out_path, audio.astype("float32"), sr)
        print(" -> Sauvé :", out_path)

    print("Préprocessing terminé.")


if __name__ == "__main__":
    main()
