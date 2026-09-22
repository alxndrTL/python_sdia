import pytest
import numpy as np

from src.lab2_fns import (
    gradient2D,
    tv,
    gradient2D_adjoint
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

class TestTV:

    def test_zero_matrix(self):
        X = np.zeros((4, 4))
        assert tv(X) == 0.0

    def test_constant_matrix(self):
        X = np.ones((4, 4)) * 42
        assert tv(X) == 0.0

    def test_horizontal_step(self):
        X = np.array([[0, 1],
                      [0, 1],
                      [0, 1]])
        assert np.isclose(tv(X), 3.0)

    def test_vertical_step(self):
        X = np.array([[0, 0, 0],
                      [1, 1, 1]])
        assert np.isclose(tv(X), 3.0)

    def test_diagonal_step(self):
        X = np.array([[0, 0],
                    [0, 1]])
        assert np.isclose(tv(X), 2.0)

    def test_non_negative(self):
        X = np.random.randn(10, 10)
        assert tv(X) >= 0.0

    def test_scale_linearity(self):
        X = np.random.rand(5, 5)
        k = 3.0
        assert np.isclose(tv(k * X), k * tv(X))

    def test_1d_row_vector(self):
        X = np.array([[0, 1, 2, 3]])
        assert np.isclose(tv(X), 3.0)

    def test_1d_column_vector(self):
        X = np.array([[0], [1], [2], [3]])
        assert np.isclose(tv(X), 3.0)

    def test_single_element(self):
        X = np.array([[5.0]])
        assert tv(X) == 0.0

    def test_3d_raises(self):
        X = np.ones((3, 3, 3))
        with pytest.raises(ValueError):
            tv(X)


class TestGradient2DAdjoint:

    def test_output_shape(self):
        M, N = 5, 7
        Y = np.random.randn(2, M, N)
        result = gradient2D_adjoint(Y)
        assert result.shape == (M, N)

    def test_wrong_first_dim_raises(self):
        Y = np.random.randn(3, 4, 4)
        with pytest.raises(ValueError):
            gradient2D_adjoint(Y)

    def test_1d_raises(self):
        Y = np.random.randn(4, 4)
        with pytest.raises(ValueError):
            gradient2D_adjoint(Y)

    def test_zero_input(self):
        Y = np.zeros((2, 4, 4))
        assert np.allclose(gradient2D_adjoint(Y), 0.0)

    def test_adjoint_relationship_real(self):
        """
        Check <D(X), Y> == <X, D*(Y)> for random real matrices.
        """
        rng = np.random.default_rng(42)  # fixed seed for reproducibility
        M, N = 6, 8

        X = rng.standard_normal((M, N))
        Y = rng.standard_normal((2, M, N))

        # Compute D(X)
        X_D, D_X = gradient2D(X)
        DX = np.stack([X_D, D_X])           # shape (2, M, N)

        # Left-hand side:  <D(X), Y>_{2xMxN}
        lhs = np.sum(np.conj(DX) * Y)

        # Right-hand side: <X, D*(Y)>_{MxN}
        rhs = np.sum(np.conj(X) * gradient2D_adjoint(Y))

        assert np.isclose(lhs, rhs), f"Adjoint check failed: lhs={lhs:.6f}, rhs={rhs:.6f}"

    def test_adjoint_relationship_complex(self):
        """
        Check <D(X), Y> == <X, D*(Y)> for random complex matrices.
        """
        rng = np.random.default_rng(42)
        M, N = 6, 8

        X = rng.standard_normal((M, N)) + 1j * rng.standard_normal((M, N))
        Y = rng.standard_normal((2, M, N)) + 1j * rng.standard_normal((2, M, N))

        X_D, D_X = gradient2D(X)
        DX = np.stack([X_D, D_X])

        lhs = np.sum(np.conj(DX) * Y)
        rhs = np.sum(np.conj(X) * gradient2D_adjoint(Y))

        assert np.isclose(lhs, rhs), f"Adjoint check failed: lhs={lhs:.6f}, rhs={rhs:.6f}"

    def test_adjoint_relationship_multiple_random(self):
        """Repeat the adjoint check over several random instances for robustness."""
        rng = np.random.default_rng(0)
        M, N = 10, 10

        for _ in range(20):
            X = rng.standard_normal((M, N))
            Y = rng.standard_normal((2, M, N))

            X_D, D_X = gradient2D(X)
            DX = np.stack([X_D, D_X])

            lhs = np.sum(np.conj(DX) * Y)
            rhs = np.sum(np.conj(X) * gradient2D_adjoint(Y))

            assert np.isclose(lhs, rhs)
