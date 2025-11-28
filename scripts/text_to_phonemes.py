from pathlib import Path
META = Path("data/metadata")
OUT = META / "metadata.csv"


def simple_text_to_phonemes(text):
    text = text.lower().replace(",", "").replace(".", "")
    return " ".join(list(text.replace(" ", "|")))


def main():
    lines = []
    for txt in META.glob("*.txt"):
        if txt.name == "sentences.txt":
            continue
        wid = txt.stem
        wav_path = f"data/processed/wav/{wid}.wav"
        text = txt.read_text().strip()
        phons = simple_text_to_phonemes(text)
        lines.append(f"{wid}|{wav_path}|{text}|{phons}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("Écrit :", OUT)


if __name__ == "__main__":
    main()
