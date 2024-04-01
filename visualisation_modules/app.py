from dash import Dash
from dash import dcc
from dash import html


def run_app():
    app = Dash(__name__)

    app.layout = html.Div(
        children = [
            html.H1(children="test"),
            html.P(children="test paragraph")
        ]
    )
    app.run_server(debug=True)