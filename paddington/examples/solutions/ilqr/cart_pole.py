import math

import jax.numpy as np
import plotly.graph_objects as go

from paddington.examples.models.nonlinear.cart_pole import CartPole
from paddington.solvers.ilqr import iLQR
from paddington.tools.controls_tools import (diagonalize,
                                             quadratic_cost_function)

dt = 0.1
plant = CartPole(dt)

g_xx = diagonalize(np.array([0.1, 0.0, 0.2, 0.0]))
g_uu = np.array([[0.01]])
g_xu = np.zeros([4, 1])
g_ux = np.zeros([1, 4])
g_x = np.array([[0.0, 0.0, 0.0, 0.0]])
g_u = np.array([[0.0]])
cost_function = quadratic_cost_function(g_xx=g_xx, g_xu=g_xu, g_ux=g_ux, g_uu=g_uu, g_x=g_x, g_u=g_u)


solver = iLQR(plant=plant, cost_function=cost_function)

states_initial = np.array([[5.0], [0.0], [math.pi/4], [0.0]])
time_total = 40

xs, us = solver.solve(states_initial, time_total)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        y=[x[2, 0] for x in xs],
        name='angular position'
    )
)

fig.add_trace(
    go.Scatter(
        y=[x[0, 0] for x in xs],
        name='linear position'
    )
)

fig.add_trace(
    go.Scatter(
        y=[u[0, 0] for u in us],
        name='control'
    )
)

fig.show()
