import unittest

import numpy as np
import plotly.graph_objects as go
import torch

from paddington.plants.nonlinear_model import InvertedPendulum


class TestZeroLinearization(unittest.TestCase):
    
    def setUp(self):

        self.problem = InvertedPendulum()
        
        states = torch.tensor([
            0.0,
            0.0,
            0.0,
            0.0
        ], requires_grad=True)

        control = torch.tensor([
            0.0
        ], requires_grad=True)

        
        d = self.problem.derivatives(states, control)

        # Linearisation
        dt = 0.01
        self.jac = self.problem.jacobian(states, control, dt)

    def test_angle(self):

        linear = torch.matmul(
            self.jac[0], 
            torch.tensor([0.0, 0.0, 1e-3, 0.0])
        )

        nonlinear = self.problem.derivatives(
            torch.tensor([0.0, 0.0, 1e-3, 0.0]), 
            torch.tensor([0.0])
        )

        [self.assertAlmostEqual(l, n) for l, n in zip(linear.tolist(), nonlinear.tolist())]

if __name__ == "__main__":
    unittest.main(verbosity=2)
