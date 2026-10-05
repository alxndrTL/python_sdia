import numpy as np
import pytest
from src.lab3_fns import brownian_motion, ideal_lowpass_filter

@pytest.fixture
def rng():
    return np.random.default_rng(42)

def make_rng(seed=42):
    return np.random.default_rng(seed)

class TestInputValidation:

    def test_start_outside_ball_raises(self):
        rng = make_rng()
        with pytest.raises(ValueError, match="unit ball"):
            brownian_motion(100, np.array([1.5, 0.0]), 0.01, rng)

    def test_start_on_boundary_accepted(self):
        # ||x0|| = 1 exactement : accepté par le code (boucle <= 1)
        rng = make_rng(0)
        walk, inter = brownian_motion(100, np.array([1.0, 0.0]), 0.01, rng)
        assert np.linalg.norm(inter) == pytest.approx(1.0, abs=1e-8)

    def test_negative_step_raises(self):
        rng = make_rng()
        with pytest.raises(ValueError, match="greater than 0"):
            brownian_motion(100, np.array([0.2, 0.4]), -0.1, rng)

    def test_zero_step_raises(self):
        rng = make_rng()
        with pytest.raises(ValueError, match="greater than 0"):
            brownian_motion(100, np.array([0.2, 0.4]), 0.0, rng)

class TestOutputStructure:

    def test_walk_contains_start_point(self):
        rng = make_rng()
        x0 = np.array([0.2, 0.4])
        walk, _ = brownian_motion(1000, x0, 0.01, rng)
        assert np.array_equal(walk[0], x0)

    def test_input_x_not_mutated(self):
        rng = make_rng()
        x0 = np.array([0.2, 0.4])
        x0_copy = x0.copy()
        brownian_motion(1000, x0, 0.01, rng)
        assert np.array_equal(x0, x0_copy)

    def test_walk_is_2d_array(self):
        rng = make_rng()
        walk, _ = brownian_motion(1000, np.array([0.2, 0.4]), 0.01, rng)
        assert isinstance(walk, np.ndarray)
        assert walk.ndim == 2
        assert walk.shape[1] == 2

    def test_last_point_outside_ball(self):
        rng = make_rng()
        walk, _ = brownian_motion(1000, np.array([0.2, 0.4]), 0.01, rng)
        assert np.linalg.norm(walk[-1]) > 1

    def test_second_to_last_point_inside_or_on_ball(self):
        rng = make_rng()
        walk, _ = brownian_motion(1000, np.array([0.2, 0.4]), 0.01, rng)
        assert np.linalg.norm(walk[-2]) <= 1 + 1e-12

    def test_walk_length_bounded(self):
        rng = make_rng()
        walk, _ = brownian_motion(1000, np.array([0.2, 0.4]), 0.01, rng)
        assert 2 <= len(walk) <= 1002 # x0 + au plus niter pas

    def test_works_in_3d(self):
        rng = make_rng()
        walk, inter = brownian_motion(1000, np.array([0.2, 0.4, 0.1]), 0.01, rng)
        assert walk.shape[1] == 3
        assert np.linalg.norm(inter) == pytest.approx(1.0, abs=1e-8)


class TestIntersectionOnSphere:

    @pytest.mark.parametrize("seed", range(20))
    def test_norm_inter_is_one(self, seed):
        rng = make_rng(seed)
        walk, inter = brownian_motion(1000, np.array([0.0, 0.0]), 0.01, rng)
        assert np.linalg.norm(inter) == pytest.approx(1.0, abs=1e-8)

    def test_inter_on_segment(self):
        # l'intersection doit être convexe entre les deux derniers points
        rng = make_rng(7)
        walk, inter = brownian_motion(1000, np.array([0.2, 0.4]), 0.01, rng)
        A, B = walk[-1], walk[-2]
        # inter = (1-a) B + a A avec a dans [0,1] => solution du petit système
        diff = A - B
        alpha = np.dot(inter - B, diff) / np.dot(diff, diff)
        assert 0.0 <= alpha <= 1.0
        assert np.allclose(inter, B + alpha * diff)


class TestIdealLowpassFilter:

    def test_output_shapes_and_types(self):
        X = make_rng().standard_normal((32, 40))
        X_filt, F_filt = ideal_lowpass_filter(X, (5, 5))
        assert X_filt.shape == X.shape
        assert F_filt.shape == X.shape
        assert np.isrealobj(X_filt)
        assert np.iscomplexobj(F_filt)

    def test_input_not_mutated(self):
        X = make_rng().standard_normal((32, 32))
        X_copy = X.copy()
        ideal_lowpass_filter(X, (5, 5))
        assert np.array_equal(X, X_copy)

    def test_zero_cutoff_gives_mean(self):
        # fc = (0, 0) : on ne garde que la fréquence nulle => image constante égale à la moyenne
        X = make_rng().standard_normal((32, 32))
        X_filt, _ = ideal_lowpass_filter(X, (0, 0))
        assert np.allclose(X_filt, X.mean())

    @pytest.mark.parametrize("shape", [(32, 32), (32, 40)])
    def test_full_cutoff_gives_identity(self, shape):
        # on garde toutes les fréquences => l'image n'est pas modifiée
        X = make_rng().standard_normal(shape)
        X_filt, _ = ideal_lowpass_filter(X, (shape[0] // 2, shape[1] // 2))
        assert np.allclose(X_filt, X)

    def test_constant_image_unchanged(self):
        # une image constante n'a que la fréquence nulle
        X = 3.0 * np.ones((32, 32))
        X_filt, _ = ideal_lowpass_filter(X, (2, 2))
        assert np.allclose(X_filt, X)

    def test_spectrum_zero_outside_mask(self):
        M, N = 32, 32
        fc_y, fc_x = 3, 5
        X = make_rng().standard_normal((M, N))
        _, F_filt = ideal_lowpass_filter(X, (fc_y, fc_x))
        mask = np.zeros((M, N), dtype=bool)
        mask[M // 2 - fc_y : M // 2 + fc_y + 1, N // 2 - fc_x : N // 2 + fc_x + 1] = True
        assert np.all(F_filt[~mask] == 0)

    def test_low_frequency_kept_high_frequency_removed(self):
        # cosinus horizontal de fréquence k : conservé si fc_x >= k, supprimé sinon
        M, N = 32, 32
        n = np.arange(N)
        low = np.tile(np.cos(2 * np.pi * 2 * n / N), (M, 1))    # k = 2
        high = np.tile(np.cos(2 * np.pi * 10 * n / N), (M, 1))  # k = 10
        X_filt, _ = ideal_lowpass_filter(low + high, (0, 5))
        assert np.allclose(X_filt, low)
