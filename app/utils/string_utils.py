def normalize_header(text: str) -> str:
    return (
        text.strip()
        .upper()
        .replace(" ", "_")
        .replace("/", "_")
    )
