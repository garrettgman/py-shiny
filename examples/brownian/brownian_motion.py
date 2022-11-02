import numpy as np
from plotly import graph_objects as go
from shinywidgets import output_widget, register_widget
from shiny import ui

# Code taken from https://plotly.com/python/3d-line-plots/
# * `brownian_motion()` is a function that generates a random walk
# * `brownian_widget()` uses restructured plotting code given in article

rs = np.random.RandomState()

# https://plotly.com/python/3d-line-plots/
def brownian_motion(T=1, N=100, mu=0.1, sigma=0.01, S0=20):
    dt = float(T) / N
    t = np.linspace(0, T, N)
    W = rs.standard_normal(size=N)
    W = np.cumsum(W) * np.sqrt(dt)  # standard brownian motion
    X = (mu - 0.5 * sigma**2) * t + sigma * W
    S = S0 * np.exp(X)  # geometric brownian motion
    return S


def brownian_data(n=100, mu=(0.0, 0.00), sigma=(0.1, 0.1), S0=(1.0, 1.0)):
    return {
        "x": brownian_motion(T=1, N=n, mu=mu[0], sigma=sigma[0], S0=S0[0]),
        "y": brownian_motion(T=1, N=n, mu=mu[1], sigma=sigma[1], S0=S0[1]),
        "z": [i for i in range(n)],
    }


def brownian_ui(name, **kwargs):
    return ui.TagList(
        output_widget(name, **kwargs),
    )


def brownian_widget(name, data):
    x = data["x"]
    y = data["y"]
    z = data["z"]
    widget = go.FigureWidget(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                marker=dict(
                    size=4,
                    color=z,
                    colorscale="Viridis",
                ),
                line=dict(color="darkblue", width=2),
            )
        ],
        layout={"showlegend": False},
    )

    register_widget(name, widget)
    return widget
