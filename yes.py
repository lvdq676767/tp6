def compter_mots(phrase):
    """
    Compte le nombre de mots dans une chaîne de caractères.

    Args:
        phrase (str): La chaîne de caractères à analyser.

    Returns:
        int: Le nombre exact de mots.
    """
    mots = phrase.split()
    nombre_de_mots = len(mots)
    return nombre_de_mots

# Exemples d'utilisation
phrase1 = "bienvenu au cours de creatic"
print(f"La phrase '{phrase1}' contient {compter_mots(phrase1)} mots.")

phrase2 = "tic tac toc"
print(f"La phrase '{phrase2}' contient {compter_mots(phrase2)} mots.")