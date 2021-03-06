import unittest
from collections import namedtuple

import jax
import jax.numpy as np
from genty import genty, genty_dataset

from simdynamics.solvers.controls_tools import quadratic_cost_function


@ genty
class TestQuadraticCost(unittest.TestCase):

    states = [
        np.array([[-1.0], [0.0], [0.0], [0.0]]),
        np.array([[-1.0], [-1.0], [0.0], [0.0]]),
        np.array([[-1.0], [-1.0], [-1.0], [0.0]]),
        np.array([[-1.0], [-1.0], [-1.0], [-1.0]]),
        np.array([[-2.0], [-3.0], [-4.0], [-5.0]]),
    ]

    controls = [
        np.array([[0.0]]),
        np.array([[-1.0]]),
        np.array([[-2.0]]),
    ]

    Case = namedtuple('Case', 'states controls')

    cases = []
    for state in states:
        for control in controls:
            cases.append(Case(state, control,))

    def setUp(self):
        g_xx = np.diag(np.array([0.1, 0.0, 2.0, 0.0]))
        g_xu = np.zeros([4, 1])
        g_ux = np.zeros([1, 4])
        g_uu = np.array([[0.1]])
        g_x = np.array([[0.0, 0.0, 0.0, 0.0]])
        g_u = np.array([[0.0]])
        self.cost_function = quadratic_cost_function(g_xx=g_xx, g_xu=g_xu, g_ux=g_ux, g_uu=g_uu, g_x=g_x, g_u=g_u)

    @genty_dataset(
        *cases
    )
    def test_jacobian(self, states, controls):

        auto_jacobian = jax.jacfwd(self.cost_function.calculate_cost, [0, 1])(states[:, 0], controls[:, 0])

        g_u = self.cost_function.calculate_g_u(x=states, u=controls)
        g_x = self.cost_function.calculate_g_x(x=states, u=controls)

        [self.assertAlmostEqual(l, n, places=4) for l, n in zip(auto_jacobian[1].tolist(), g_u.tolist())]
        [self.assertAlmostEqual(l, n, places=4) for l, n in zip(auto_jacobian[0].tolist(), g_x.tolist())]


if __name__ == "__main__":
    unittest.main(verbosity=2)
