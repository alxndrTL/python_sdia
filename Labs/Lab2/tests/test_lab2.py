import unittest
import numpy as np

from src.lab2 import gradient2D, tv, gradient2D_adjoint

# tests unitaires des fonctions de l'exercice 3

class TestGradient2D(unittest.TestCase):

    def test_format_sortie(self):
        # la sortie doit être de taille (M, N, 2), pour une matrice carrée et non carrée
        rng = np.random.default_rng(0)
        for shape in [(4, 4), (3, 5)]:
            with self.subTest(shape=shape):
                X = rng.standard_normal(shape)
                G = gradient2D(X)
                self.assertEqual(G.shape, shape + (2,))

    def test_matrice_constante(self):
        # le gradient d'une matrice constante est nul partout
        for shape in [(4, 4), (3, 5)]:
            with self.subTest(shape=shape):
                X = 7 * np.ones(shape)
                np.testing.assert_array_equal(gradient2D(X), np.zeros(shape + (2,)))

    def test_valeurs_connues(self):
        # rampe X[m, n] = N*m + n : différences horizontales = 1, verticales = N
        M, N = 3, 4
        X = np.arange(M * N).reshape(M, N)
        G = gradient2D(X)

        Dh_attendu = np.ones((M, N))
        Dh_attendu[:, -1] = 0
        Dv_attendu = N * np.ones((M, N))
        Dv_attendu[-1, :] = 0

        np.testing.assert_array_equal(G[:, :, 0], Dh_attendu)
        np.testing.assert_array_equal(G[:, :, 1], Dv_attendu)

    def test_erreur_dimension(self):
        # une entrée à 3 dimensions doit déclencher une AssertionError
        with self.assertRaises(AssertionError):
            gradient2D(np.ones((2, 3, 4)))

class TestTV(unittest.TestCase):
 
    def test_matrice_constante(self):
        # la TV d'une matrice constante est nulle
        for shape in [(4, 4), (3, 5)]:
            with self.subTest(shape=shape):
                X = 7 * np.ones(shape)
                self.assertEqual(tv(X), 0)
 
    def test_valeur_connue(self):
        # cf matrice test dans le notebook
        X = np.array([[0, 3], [4, 3]])
        self.assertAlmostEqual(tv(X), 6)
 
    def test_matrice_complexe(self):
        # multiplier par i ne change pas les modules, donc TV(iX) = TV(X) = 6
        X = 1j * np.array([[0, 3], [4, 3]])
        self.assertAlmostEqual(tv(X), 6)
 
    def test_erreur_dimension(self):
        # une entrée à 3 dimensions doit déclencher une AssertionError
        with self.assertRaises(AssertionError):
            tv(np.ones((2, 3, 4)))

def produit_scalaire(U, V):
    # produit scalaire complexe: somme des conj(u)*v sur tous les éléments
    return np.sum(np.conj(U)*V)
 
class TestGradient2DAdjoint(unittest.TestCase):
 
    def setUp(self):
        # va être appelée avant chaque lancement de test
        self.rng = np.random.default_rng(0)
 
    def matrice_complexe_aleatoire(self, shape):
        return self.rng.standard_normal(shape) + 1j * self.rng.standard_normal(shape)
 
    def test_format_sortie(self):
        # la sortie doit être de taille (M, N) pour n'importe quelle matrice
        for M, N in [(4, 4), (3, 5)]:
            with self.subTest(shape=(M, N)):
                Y = self.matrice_complexe_aleatoire((M, N, 2))
                self.assertEqual(gradient2D_adjoint(Y).shape, (M, N))
 
    def test_valeurs_connues(self):
        # exemple calculé à la main avec Y_h et Y_v remplies de 1 (cf cellule du notebook)
        Y = np.ones((3, 3, 2))
        sortie = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])
        np.testing.assert_array_equal(gradient2D_adjoint(Y), sortie)
 
    def test_adjoint(self):
        # <D(X), Y> = <X, D*(Y)> pour X et Y complexes tirés aléatoirement
        for M, N in [(4, 4), (3, 5)]:
            with self.subTest(shape=(M, N)):
                X = self.matrice_complexe_aleatoire((M, N))
                Y = self.matrice_complexe_aleatoire((M, N, 2))
                gauche = produit_scalaire(gradient2D(X), Y)
                droite = produit_scalaire(X, gradient2D_adjoint(Y))
                self.assertAlmostEqual(gauche, droite)
 
    def test_erreur_format(self):
        # une entrée qui n'est pas de taille (M, N, 2) doit déclencher une erreur
        for shape in [(3, 3), (3, 3, 3)]:
            with self.subTest(shape=shape):
                with self.assertRaises(AssertionError):
                    gradient2D_adjoint(np.ones(shape))
 