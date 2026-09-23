import numpy as np

def brownianMotion(niter: int, x: np.ndarray, step: float, rng):
    """
    Simule une marche aléatoire brownienne dans la boule unité.

    La marche s'arrête dès que le processus sort de la boule unité ou que le
    nombre maximum d'itérations est atteint. Le point d'intersection exact avec
    la sphère unité est ensuite calculé par interpolation linéaire entre les
    deux derniers points.

    Parameters
    ----------
    niter : int
        Nombre maximum de pas de la marche.
    x : np.ndarray
        Point de départ, doit être strictement à l'intérieur de la boule unité
        (i.e. ||x|| <= 1).
    step : float
        Pas de temps dt > 0. L'incrément brownien est de variance dt, donc
        d'écart-type sqrt(dt).
    rng : np.random.Generator
        Générateur de nombres aléatoires numpy (e.g. np.random.default_rng()).

    Returns
    -------
    walk : list of np.ndarray
        Liste des positions successives de la marche, incluant le point de
        départ.
    inter : np.ndarray
        Point d'intersection interpolé entre le dernier point intérieur et le
        premier point extérieur à la sphère unité.

    Raises
    ------
    ValueError
        Si le point de départ est en dehors de la boule unité, si step <= 0,
        ou si aucune racine valide n'est trouvée lors de l'interpolation.

    Examples
    --------
    >>> rng = np.random.default_rng(42)
    >>> walk, inter = brownianMotion(1000, np.array([0.0, 0.0]), 0.01, rng)
    >>> np.linalg.norm(inter)  # doit être proche de 1
    """
    if np.linalg.norm(x) > 1 or step <= 0:
        raise ValueError("x must be inside the unit ball and step must be greater than 0")

    walk = [x.copy()]
    n = 0

    while np.linalg.norm(x) <= 1 and n <= niter:
        x = x + np.sqrt(step) * rng.normal(loc=0, scale=1, size=x.shape)
        walk.append(x.copy())
        n += 1

    A = walk[-2]
    B = walk[-1]
    d = A - B

    # Coefficients du polynôme tels que développés ci-dessus
    a_coef = np.dot(d, d)
    b_coef = 2 * np.dot(B, d)
    c_coef = np.dot(B, B) - 1

    roots = np.roots([a_coef, b_coef, c_coef])
    real_roots = roots[np.isreal(roots)].real        # racines réelles
    valid = real_roots[(real_roots >= 0) & (real_roots <= 1)]  # dans [0, 1]

    if len(valid) == 0:
        raise ValueError("Aucune racine valide trouvée pour l'interpolation des deux derniers points")

    alpha = valid[0]
    inter = (1 - alpha) * A + alpha * B

    return walk, inter
