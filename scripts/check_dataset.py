from pathlib import Path

import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
META_DIR = ROOT / "data" / "metadata"
RAW_DIR = ROOT / "data" / "raw"

MIN_DURATION = 1.5  # secondes : en dessous = suspect


def main():
    if not META_DIR.exists():
        print(f"[ERREUR] Dossier metadata introuvable : {META_DIR}")
        return

    txt_files = sorted(
        p for p in META_DIR.glob("*.txt")
        if p.name != "sentences.txt"
    )

    if not txt_files:
        print("[INFO] Aucun .txt trouvé dans data/metadata/")
        return

    missing = []
    too_short = []

    total = len(txt_files)

    print("=== Vérification du dataset voix ===")
    print(f"Textes trouvés : {total}")
    print(f"Dossier raw    : {RAW_DIR}")
    print("====================================\n")

    for txt_path in txt_files:
        wid = txt_path.stem  # ex: "0001"
        wav_path = RAW_DIR / f"{wid}.wav"

        if not wav_path.exists():
            print(f"[MANQUANT] {wav_path.name} n'existe pas.")
            missing.append(wid)
            continue

        try:
            data, sr = sf.read(wav_path)
        except Exception as e:
            print(f"[ERREUR] Impossible de lire {wav_path.name} : {e}")
            too_short.append(wid)
            continue

        if data.ndim > 1:
            length_samples = data.shape[0]
        else:
            length_samples = len(data)

        duration = length_samples / sr

        if duration < MIN_DURATION:
            print(
                f"[COURT] {wav_path.name} ({duration:.2f} s) "
                f"< {MIN_DURATION}s"
            )
            too_short.append(wid)

    print("\n=== RÉSUMÉ ===")
    print(f"Total phrases texte : {total}")
    print(f"Fichiers manquants  : {len(missing)}")
    print(f"Fichiers trop courts: {len(too_short)}")

    if missing:
        print("\nIDs manquants :")
        print(", ".join(missing))

    if too_short:
        print("\nIDs à réenregistrer (trop courts) :")
        print(", ".join(too_short))

    print("\nAstuce : pour réenregistrer un ID, utilise :")
    print("  python scripts/record_dataset.py 0017")


if __name__ == "__main__":
    main()
