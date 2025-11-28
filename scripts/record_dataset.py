import sys
from pathlib import Path
import time

import numpy as np
import sounddevice as sd
import soundfile as sf

# Répertoires
ROOT = Path(__file__).resolve().parent.parent
META_DIR = ROOT / "data" / "metadata"
RAW_DIR = ROOT / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

# Paramètres audio
SAMPLE_RATE = 44100   # 44100 ou 48000
CHANNELS = 1          # mono pour l'IA
DEFAULT_DURATION = 6  # durée d'enregistrement par phrase (en secondes)


def record_audio(duration: float) -> np.ndarray:
    """
    Enregistre 'duration' secondes depuis le micro par défaut
    et retourne un tableau numpy (mono).
    """
    print(f"\n[REC] Enregistrement pendant {duration} secondes...")
    sd.default.samplerate = SAMPLE_RATE
    sd.default.channels = CHANNELS

    frames = int(duration * SAMPLE_RATE)
    audio = sd.rec(frames, dtype="float32")
    sd.wait()
    print("[REC] Terminé.")
    return audio.squeeze()  # (N, 1) -> (N,)


def get_target_txt_files(target_id: str | None):
    """
    Renvoie la liste de fichiers .txt à traiter.
    - si target_id est None -> tous les .txt (sauf sentences.txt)
    - sinon -> uniquement le .txt correspondant à l'ID donné
    """
    if not META_DIR.exists():
        print(f"[ERREUR] Dossier metadata introuvable : {META_DIR}")
        sys.exit(1)

    if target_id is None:
        txt_files = sorted(
            p for p in META_DIR.glob("*.txt")
            if p.name != "sentences.txt"
        )
        return txt_files

    # mode ciblé
    tid = target_id.zfill(4)  # "17" -> "0017"
    txt_path = META_DIR / f"{tid}.txt"
    if not txt_path.exists():
        print(f"[ERREUR] Fichier texte inexistant pour ID {tid}: {txt_path}")
        sys.exit(1)
    return [txt_path]


def main():
    # Optionnel : ID spécifique passé en argument
    target_id = sys.argv[1] if len(sys.argv) > 1 else None

    txt_files = get_target_txt_files(target_id)

    if not txt_files:
        print("[INFO] Aucun fichier .txt trouvé dans data/metadata/")
        print("Tu peux générer 0001.txt ... 0070.txt avec "
              "scripts/generate_text_files.py")
        sys.exit(0)

    print("=== Enregistreur dataset voix ===")
    print(f"Dossier metadata : {META_DIR}")
    print(f"Dossier raw      : {RAW_DIR}")
    print(f"Sample rate      : {SAMPLE_RATE} Hz")
    print(f"Durée par phrase : {DEFAULT_DURATION} s")
    if target_id:
        print(f"Mode ciblé sur l'ID : {target_id.zfill(4)}")
    print("=================================\n")

    for txt_path in txt_files:
        wid = txt_path.stem  # ex: "0001"
        wav_path = RAW_DIR / f"{wid}.wav"
        text = txt_path.read_text(encoding="utf-8").strip()

        print("\n---------------------------------")
        print(f"ID     : {wid}")
        print(f"Texte  : {text}")
        print("---------------------------------")

        # Si mode global (pas d'ID spécifique) et que le wav existe, on skip
        if target_id is None and wav_path.exists():
            print(f"[SKIP] {wav_path.name} existe déjà, je passe.")
            continue

        # Si mode ciblé et que le wav existe, on demande confirmation
        if target_id is not None and wav_path.exists():
            print(f"[ATTENTION] {wav_path.name} existe déjà.")
            ans = input("Le réenregistrer ? (o/N) ").strip().lower()
            if ans != "o":
                print("[SKIP] Réenregistrement annulé.")
                continue

        print("Options :")
        print("  [Entrée]  -> enregistrer")
        print("  [s]       -> passer cette phrase")
        print("  [q]       -> quitter")
        choice = input("> ").strip().lower()

        if choice == "q":
            print("Sortie demandée, arrêt.")
            break
        if choice == "s":
            print("[SKIP] Phrase ignorée.")
            continue

        # Enregistrement
        print("Prépare-toi... Enregistrement dans 2 secondes.")
        time.sleep(2)

        audio = record_audio(DEFAULT_DURATION)

        sf.write(wav_path, audio, SAMPLE_RATE)
        print(f"[OK] Sauvegardé dans : {wav_path}")

        # Si on est en mode ciblé pour une seule phrase, on peut sortir après
        if target_id is not None:
            print("Mode ciblé : enregistrement terminé pour cet ID.")
            break

    print("\n=== Fin de l’enregistrement dataset ===")


if __name__ == "__main__":
    main()
