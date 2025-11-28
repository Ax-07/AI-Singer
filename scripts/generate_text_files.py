from pathlib import Path

# Dossier où seront créés les .txt
META_DIR = Path("data/metadata")
META_DIR.mkdir(parents=True, exist_ok=True)

sentences = [
    "La vie est belle.",
    "Tu es là.",
    "Il pleut encore.",
    "Tout va bien.",
    "Je suis prêt.",
    "Rien ne bouge.",
    "Ça commence.",
    "J’arrive tout de suite.",
    "On continue.",
    "Je t’écoute.",

    "Anna admire une belle mélodie.",
    "Léo lit une lettre lumineuse.",
    "La lune illumine la nuit.",
    "Élise répète une chanson étrange.",
    "Le vent souffle sur la vallée.",
    "Nous rêvons d’un avenir meilleur.",

    "Viens avec moi, on va tout changer !",
    "Je veux sentir la liberté !",
    "On avance, encore et encore !",
    "Rien ne pourra m’arrêter !",
    "Je brille comme une étoile !",

    "Sous le soleil doré, je marche sans me presser.",
    "Quand la nuit tombe, mon cœur se met à rêver.",
    "Je vole, je plane, je touche les nuages.",
    "Dans ce monde fragile, je cherche mon chemin.",
    "Un souffle, une voix, une lumière dans le noir.",
    "Je danse dans la pluie, je chante sous les étoiles.",

    "Parfois le silence en dit plus que mille mots.",
    "Je voudrais comprendre ce qui nous lie tous ensemble.",
    "Chaque jour est une nouvelle chance de réussir.",
    "Tout commence par un rêve, puis par un premier pas.",
    "Il suffit d’une idée pour changer une vie entière.",

    "Je suis tellement heureux aujourd’hui.",
    "Je me sens un peu fatigué, mais motivé.",
    "Cette histoire me touche profondément.",
    "J’ai un peu peur, mais je continue.",
    "Ça me fait rire, vraiment beaucoup !",

    "Ceci est une ligne d’entraînement vocal.",
    "Je parle calmement pour enregistrer ma voix.",
    "C’est un exemple simple pour le modèle IA.",
    "Je continue la lecture pour fournir des données.",
    "Chaque fichier doit être clair et propre.",

    "Dans le vent du matin, je respire la vie.",
    "Je glisse entre les ombres et les éclats de lumière.",
    "Les couleurs du ciel m’emportent loin d’ici.",
    "Je cherche un rêve qui pourrait me guider.",
    "La mer murmure des secrets à mon âme.",
    "Je suis une étincelle dans la nuit profonde.",

    "La la la la la.",
    "Ma ma ma.",
    "Na na na.",
    "Pa pa pa.",
    "Da da da.",
    "Ta ta ta.",
    "Ra ra ra.",
    "Fa fa fa.",
    "Uu uu uu.",
    "Oo oo oo.",
    "Éé éé éé.",
    "Aa aa aa.",
    "Li li li.",
    "Lu lu lu.",
    "Lo lo lo.",
    "Mi mi mi.",
    "Mo mo mo.",

    "Ahhh, comme une montée douce.",
    "Ooooh, qui s’ouvre lentement.",
    "Mmmmh, qui glisse vers le grave.",
    "Heeey, comme un appel.",
    "Aaah, vers le haut puis vers le bas.",
]


def main():
    if len(sentences) != 70:
        print(
            f"Attention : {len(sentences)} phrases dans la liste, attendu 70."
        )
    for i, sentence in enumerate(sentences, start=1):
        filename = f"{i:04d}.txt"  # 0001.txt, 0002.txt, ...
        path = META_DIR / filename
        path.write_text(sentence, encoding="utf-8")
        print("Écrit :", path)


if __name__ == "__main__":
    main()
