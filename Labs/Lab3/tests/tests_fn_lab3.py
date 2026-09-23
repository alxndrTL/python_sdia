import numpy as np
import pytest
from src.lab3_fns import brownianMotion   # adaptez le nom du module


@pytest.fixture
def rng():
    return np.random.default_rng(42)


def make_rng(seed=42):
    return np.random.default_rng(seed)



class TestInputValidation:

    def test_start_outside_ball_raises(self):
        rng = make_rng()
        with pytest.raises(ValueError, match="unit ball"):
            brownianMotion(100, np.array([1.5, 0.0]), 0.01, rng)

    def test_start_on_boundary_accepted(self):
        # ||x0|| = 1 exactement : accepté par le code (boucle <= 1)
        rng = make_rng(0)
        walk, inter = brownianMotion(100, np.array([1.0, 0.0]), 0.01, rng)
        assert np.linalg.norm(inter) == pytest.approx(1.0, abs=1e-8)

    def test_negative_step_raises(self):
        rng = make_rng()
        with pytest.raises(ValueError, match="greater than 0"):
            brownianMotion(100, np.array([0.2, 0.4]), -0.1, rng)

    def test_zero_step_raises(self):
        rng = make_rng()
        with pytest.raises(ValueError, match="greater than 0"):
            brownianMotion(100, np.array([0.2, 0.4]), 0.0, rng)

class TestOutputStructure:

    def test_walk_contains_start_point(self):
        rng = make_rng()
        x0 = np.array([0.2, 0.4])
        walk, _ = brownianMotion(1000, x0, 0.01, rng)
        assert np.array_equal(walk[0], x0)

    def test_input_x_not_mutated(self):
        rng = make_rng()
        x0 = np.array([0.2, 0.4])
        x0_copy = x0.copy()
        brownianMotion(1000, x0, 0.01, rng)
        assert np.array_equal(x0, x0_copy)

    def test_walk_is_2d_array(self):
        rng = make_rng()
        walk, _ = brownianMotion(1000, np.array([0.2, 0.4]), 0.01, rng)
        assert isinstance(walk, np.ndarray)
        assert walk.ndim == 2
        assert walk.shape[1] == 2

    def test_last_point_outside_ball(self):
        rng = make_rng()
        walk, _ = brownianMotion(1000, np.array([0.2, 0.4]), 0.01, rng)
        assert np.linalg.norm(walk[-1]) > 1

    def test_second_to_last_point_inside_or_on_ball(self):
        rng = make_rng()
        walk, _ = brownianMotion(1000, np.array([0.2, 0.4]), 0.01, rng)
        assert np.linalg.norm(walk[-2]) <= 1 + 1e-12

    def test_walk_length_bounded(self):
        rng = make_rng()
        walk, _ = brownianMotion(1000, np.array([0.2, 0.4]), 0.01, rng)
        assert 2 <= len(walk) <= 1002   # x0 + au plus niter pas

    def test_works_in_3d(self):
        rng = make_rng()
        walk, inter = brownianMotion(1000, np.array([0.2, 0.4, 0.1]), 0.01, rng)
        assert walk.shape[1] == 3
        assert np.linalg.norm(inter) == pytest.approx(1.0, abs=1e-8)


class TestIntersectionOnSphere:

    @pytest.mark.parametrize("seed", range(20))
    def test_norm_inter_is_one(self, seed):
        rng = make_rng(seed)
        walk, inter = brownianMotion(1000, np.array([0.0, 0.0]), 0.01, rng)
        assert np.linalg.norm(inter) == pytest.approx(1.0, abs=1e-8)

    def test_inter_on_segment(self):
        # l'intersection doit être convexe entre les deux derniers points
        rng = make_rng(7)
        walk, inter = brownianMotion(1000, np.array([0.2, 0.4]), 0.01, rng)
        A, B = walk[-1], walk[-2]
        # inter = (1-a) B + a A avec a dans [0,1] => solution du petit système
        diff = A - B
        alpha = np.dot(inter - B, diff) / np.dot(diff, diff)
        assert 0.0 <= alpha <= 1.0
        assert np.allclose(inter, B + alpha * diff)
