import numpy as np

def markov(rho, A, nmax, rng):
    assert A.ndim == 2 and (A.shape[0] == A.shape[1])       # A stochastique (taille de A : N x N)
    assert np.all(A >= 0)                                   # A stochastique (éléments >= 0)
    assert np.allclose(A.sum(axis=1), 1)                    # A stochastique (somme des lignes = 1)
    assert np.all(rho >= 0) and np.isclose(rho.sum(), 1)    # rho est une loi de prob.
    assert rho.shape == (A.shape[0],)                       # la taille de rho est cohérente avec A

    N = A.shape[0] # nombre d'états
    states = np.arange(N) # états possibles
    X = np.empty(nmax + 1, dtype=int)

    # premier état
    X[0] = rng.choice(states, p=rho)

    for q in range(nmax):
        # on échantillonne le prochain état via la distribution de proba
        # donnée par la ligne de la matrice A correspondant à l'état courant X
        X[q+1] = rng.choice(states, p=A[X[q]])

    return X