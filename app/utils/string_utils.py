import unicodedata


def normalize_header(text: str) -> str:
    return (
        text.strip()
        .upper()
        .replace(" ", "_")
        .replace("/", "_")
    )


def get_acronimo(string: str) -> str:
    return "".join(
            p[0].lower() for p in string.split() if len(p) > 2
        )


def get_abreviatura(string: str) -> str:
    return "".join(
            p[0:2].lower() for p in string.split() if len(p) > 2
        )


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text
