import numpy as np

def brownian_motion(niter : int, x: np.array, step : float, rng) -> tuple[list[np.ndarray], np.ndarray]:
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
    inter : np.ndarray or None
        Point d'intersection interpolé entre le dernier point intérieur et le
        premier point extérieur à la sphère unité. None si la marche n'est pas
        sortie de la boule en niter pas.

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

    walk = [x.copy()] #on initialise la marche avec le point de départ
    n = 0
    if np.linalg.norm(x) > 1 or step <= 0 :
        raise ValueError("x must be inside the unit ball and step must be greater than 0")

    while np.linalg.norm(x) <= 1 and n <= niter:
        x = x + np.sqrt(step)*rng.normal(loc = 0, scale = 1, size = x.shape)
        walk.append(x)
        n += 1

    # si la marche n'est pas sortie de la boule en niter pas, il n'y a pas d'intersection
    if np.linalg.norm(x) <= 1:
        return np.array(walk), None

    A = walk[-1]
    B = walk[-2]
    d = A-B

    #on calcule les coefficients du polynôme tels que développés ci-dessus :
    a_coef = np.dot(d,d)
    b_coef = 2 * np.dot(B,d)
    c_coef = np.dot(B,B) -1

    roots = np.roots([a_coef, b_coef, c_coef])
    real_roots = roots[np.isreal(roots)].real #on prend les racines réelles
    valid = real_roots[(real_roots >=0 ) & (real_roots <= 1)] #on prend les racines qui sont entre 0 et 1.

    if len(valid) == 0:
        raise ValueError("Aucune Racine valide trouvée pour l'interpolation des deux derniers points")

    alpha = valid[0]
    inter = (1-alpha)*B + alpha*A

    walk = np.array(walk)

    return walk, inter


def ideal_lowpass_filter(X, fc):
    """Filtre passe-bas idéal 2D.

    Paramètres
    ----------
    X : np.ndarray, shape (M1, N1)
        Image en niveaux de gris.
    fc : tuple (fc_y, fc_x)
        Nombre de fréquences conservées de part et d'autre de la fréquence
        nulle, selon chaque direction.

    Retours
    -------
    X_filt : np.ndarray, shape (M1, N1)
        Image filtrée (réelle).
    F_filt : np.ndarray, shape (M1, N1), complexe
        Spectre filtré centré (utile pour l'affichage).
    """

    M1, N1 = X.shape
    fc_y, fc_x = fc

    # passage dans le domaine fréquentiel
    # cf question précédente: fréquence nulle en (M1//2, N1//2)
    F = np.fft.fftshift(np.fft.fft2(X))

    # masque rectangulaire autour du centre
    cy, cx = M1//2, N1//2
    mask = np.zeros((M1, N1), dtype=float) # matrice remplie de 0
    mask[cy - fc_y : cy + fc_y + 1, cx - fc_x : cx + fc_x + 1] = 1.0 # on met 1 dans la zone du filtre

    # application du masque
    # dans le domaine spatial, on doit faire une convolution
    # mais dans le domaine fréquentiel, on fait juste un produit
    F_filt = F * mask

    # retour dans le domaine spatial
    X_filt = np.fft.ifft2(np.fft.ifftshift(F_filt))
    return X_filt.real, F_filt
