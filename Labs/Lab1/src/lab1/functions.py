"""Fonctions développées dans le notebook lab1.ipynb.

Ces fonctions ont été reproduites pour les tester (avec pytest) et les documenter (avec sphinx).
"""


def is_unique(x):
    """Indique si une liste ne contient aucun doublon.

    Args:
        x (list): liste d'éléments (entiers, chaînes, etc.).

    Returns:
        bool: ``True`` si tous les éléments de ``x`` sont distincts,
        ``False`` s'il existe au moins un doublon.

    Example:
        >>> is_unique([1, 2, 3])
        True
        >>> is_unique([1, 2, 1])
        False
    """
    return len(set(x)) == len(x)


def triangle_shape(height):
    """Construit un triangle isocèle de caractères.

    Args:
        height (int): hauteur du triangle, entier positif ou nul.

    Returns:
        str: la chaîne représentant le triangle, ``""`` si ``height`` vaut 0.

    Example:
        >>> print(triangle_shape(3))
          x
         xxx
        xxxxx
    """
    result = ""
    for i in range(height):
        spaces = " " * (height - 1 - i)
        result += spaces + "x" * (2 * i + 1) + spaces
        if i < height - 1:
            result += "\n"
    return result
