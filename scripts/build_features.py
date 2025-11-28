from pathlib import Path

import librosa
import numpy as np
import pandas as pd

PROC_WAV_DIR = Path("data/processed/wav")
META_DIR = Path("data/metadata")
FEATURE_DIR = Path("data/processed/features")
FEATURE_DIR.mkdir(parents=True, exist_ok=True)

TARGET_SR = 22050
N_MELS = 80
N_FFT = 1024
HOP_LENGTH = 256


def compute_mel_and_f0(wav_path: Path):
    """
    Calcule un mel-spectrogramme et une courbe F0 approximative
    pour un fichier audio.
    """
    y, sr = librosa.load(wav_path, sr=TARGET_SR, mono=True)

    # mel-spectrogramme
    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=1.0,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)

    # F0 approximative avec pyin 
    # (simple, pas parfait mais suffisant pour un proto)
    f0, voiced_flag, _ = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7"),
        frame_length=N_FFT,
        hop_length=HOP_LENGTH,
    )
    # Remplace les NaN (non voisées) par 0
    f0 = np.nan_to_num(f0)

    return mel_db.astype("float32"), f0.astype("float32")


def main():
    # On suppose que tu as déjà généré 0001.txt -> 0070.txt
    txt_files = sorted((META_DIR).glob("*.txt"))
    rows = []

    for txt_path in txt_files:
        if txt_path.name == "sentences.txt":
            continue

        wid = txt_path.stem  # ex: "0001"
        wav_path = PROC_WAV_DIR / f"{wid}.wav"
        if not wav_path.exists():
            print(f"[WARN] Pas de wav pour {wid} ({wav_path})")
            continue

        text = txt_path.read_text(encoding="utf-8").strip()

        print("Features pour :", wid)
        mel, f0 = compute_mel_and_f0(wav_path)

        # Sauvegarde des features
        mel_path = FEATURE_DIR / f"{wid}_mel.npy"
        f0_path = FEATURE_DIR / f"{wid}_f0.npy"
        np.save(mel_path, mel)
        np.save(f0_path, f0)

        rows.append(
            {
                "id": wid,
                "wav_path": str(wav_path),
                "text": text,
                "mel_path": str(mel_path),
                "f0_path": str(f0_path),
            }
        )

    if rows:
        df = pd.DataFrame(rows)
        out_csv = META_DIR / "metadata_features.csv"
        df.to_csv(out_csv, index=False, encoding="utf-8")
        print("Écrit :", out_csv)
    else:
        print("Aucune ligne de metadata générée.")


if __name__ == "__main__":
    main()
