def is_unique_entity_in_set(
        seen_set: set,
        key: str,
) -> bool:
    """
    Agrega entity si key no existe. Retorna True si se agregó.
    """
    if not key:
        return False
    if key in seen_set:
        return False
    return True
