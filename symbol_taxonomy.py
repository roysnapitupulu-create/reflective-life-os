# symbol_taxonomy.py

SYMBOL_TAXONOMY = {
    "urban_survival": {
        "angkot": [
            "angkot",
            "mobil angkot",
            "penumpang",
            "mengejar penumpang",
        ],
        "ojol": [
            "ojol",
            "gojek",
            "grab",
            "driver online",
            "order",
            "menunggu order",
        ],
        "warung": [
            "warung",
            "warteg",
            "kedai",
            "lapak",
        ],
        "gerobak": [
            "gerobak",
            "pedagang keliling",
            "jualan keliling",
        ],
        "lampu_merah": [
            "lampu merah",
            "traffic light",
            "perempatan",
        ],
        "halte": [
            "halte",
            "terminal",
            "menunggu bus",
        ],
    },

    "tree": {
        "tree": [
            "pohon",
            "mangga",
            "keteduhan",
            "teduh",
            "daun",
            "akar",
        ],
    },

    "thinkpad": {
        "thinkpad": [
            "thinkpad",
            "laptop",
            "keyboard",
            "layar",
            "komputer",
        ],
    },

    "spiritual": {
        "spiritual": [
            "tuhan",
            "doa",
            "iman",
            "rahmat",
            "syukur",
            "gereja",
            "masjid",
            "berkat",
            "kasih",
        ],
    },
}


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def detect_symbols(text: str) -> tuple[list[str], list[str]]:
    text_lower = str(text or "").lower()

    themes: list[str] = []
    symbols: list[str] = []

    for theme, symbol_map in SYMBOL_TAXONOMY.items():
        for symbol, keywords in symbol_map.items():
            if contains_any(text_lower, keywords):
                if theme not in themes:
                    themes.append(theme)
                if symbol not in symbols:
                    symbols.append(symbol)

    return themes, symbols