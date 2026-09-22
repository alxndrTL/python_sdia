import pytest
import numpy as np

from src.lab2_fns import (
    gradient2D
)

class TestGradient2D :
    def test_output_format(self):
        X = np.ones((3, 4))
        X_D, D_X = gradient2D(X)

        assert X_D.shape == X.shape
        assert D_X.shape == X.shape

    def test_square_matrix(self):
        X = np.ones((3, 3))
        X_D, D_X = gradient2D(X)

        assert np.all(X_D == 0)
        assert np.all(D_X == 0)

    def test_non_square_matrix(self):
        X = np.ones((3, 4))
        X_D, D_X = gradient2D(X)

        assert np.all(X_D == 0)
        assert np.all(D_X == 0)

    def test_too_many_dimensions(self):
        X = np.ones((2, 3, 4))

        try:
            gradient2D(X)
            assert False
        except ValueError:
            assert True
