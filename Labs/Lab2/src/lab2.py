import numpy as np

# fonctions du lab2 de l'exercice 3

def gradient2D(X):
    """Calcule le gradient discret 2D d'une matrice.
 
    Paramètres
    ----------
    X : numpy.ndarray, de taille (M, N)
        Matrice d'entrée
 
    Retour
    ------
    numpy.ndarray, de taille (M, N, 2)
        [:, :, 0] : différences horizontales X D_h,
        [:, :, 1] : différences verticales D_v X.
        Les différences valent 0 sur la dernière colonne / dernière ligne.
 
    Erreurs
    -------
    AssertionError
        Si X n'est pas un tableau à 2 dimensions.
    """

    assert X.ndim == 2, "gradient2D attend une matrice 2D"
 
    # differences horizontales (x[m, n+1] - x[m, n]) avec np.diff selon axis=1
    diff_horizontales = np.diff(X, axis=1) # renvoie une matrice (M, N-1)
    zeros = np.zeros((X.shape[0], 1)) # on ajoute une colonne de zéros pour revenir à (M, N)
    Dh = np.c_[diff_horizontales, zeros]

    # differences verticales (x[m+1, n] - x[m, n]) avec np.diff selon axis=0
    diff_verticales = np.diff(X, axis=0) # matrice (M-1, N)
    zeros = np.zeros((1, X.shape[1])) # on ajoute une ligne de zéros pour revenir à (M, N)
    Dv = np.r_[diff_verticales, zeros]
 
    return np.stack((Dh, Dv), axis=-1) # (M, N, 2)

def tv(X):
    """Calcule la variation totale (TV) isotrope discrète d'une matrice.

    Références
        ----------
        .. [1] Condat, L. (2017). Discrete Total Variation: New Definition and
               Minimization. *SIAM Journal on Imaging Sciences*, 10(3), 1258–1290.
               https://hal.archives-ouvertes.fr/hal-01309685

    Paramètres
    ----------
    X : numpy.ndarray, de taille (M, N)
        Matrice d'entrée

    Retour
    ------
    float
        Variation totale de X (réel positif ou nul).

    Erreurs
    -------
    AssertionError
        Si X n'est pas un tableau à 2 dimensions (levée par gradient2D).

    Notes
    -----
    Pour une matrice complexe, on utilise le module au carré |z|^2
    """

    assert X.ndim == 2, "tv attend une matrice 2D"

    G = gradient2D(X) # taille (M, N, 2)

    # norme euclidienne selon le dernier axe, puis somme sur tous les coefs
    # on retrouve bien TV(X) = somme_(m,n) de sqrt(|[X D_h]_{m,n}|^2 + |[D_v X]_{m,n}|^2)
    return np.sum(np.linalg.norm(G, axis=-1))

def gradient2D_adjoint(Y):
    """Calcule l'adjoint D* du gradient discret 2D.

    Paramètres
    ----------
    Y : numpy.ndarray, de taille (M, N, 2)
        [:, :, 0] : composante horizontale Y_h,
        [:, :, 1] : composante verticale Y_v

    Retour
    ------
    numpy.ndarray, de taille (M, N)
        D*(Y) = Y_h D_h* + D_v* Y_v.

    Erreurs
    -------
    AssertionError
        Si Y n'est pas un tableau de taille (M, N, 2).
    """

    assert Y.ndim == 3 and Y.shape[2] == 2, "gradient2D_adjoint attend un tableau (M, N, 2)"

    Yh = Y[:, :, 0]
    Yv = Y[:, :, 1]

    # partie horizontale Y_h D_h*

    # on raisonne colonne par colonne, étant donné la définition de Y_h D_h* donnée en consigne:
    # - 1re colonne : -y_{h,1}
    # - colonnes 2 à N-1 : -(y_{h,n} - y_{h,n-1}), obtenues avec np.diff sur axis=1
    # - dernière colonne : y_{h,N-1}
    YhDh = np.c_[-Yh[:, :1], -np.diff(Yh[:, :-1], axis=1), Yh[:, -2:-1]]

    # partie verticale D_v* Y_v
    # similaire à précédemment mais en inversant les axes
    DvYv = np.r_[-Yv[:1, :], -np.diff(Yv[:-1, :], axis=0), Yv[-2:-1, :]]

    return YhDh + DvYv # (M, N)
