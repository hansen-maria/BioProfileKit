#! usr/bin/env Python3
import pathlib

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

from pages import home
from utils.file_reader import read_file


def main():
    app = create_app()
    app.run()


def create_app():
    file = '/Users/yuki/PycharmProjects/BioProfileKit/test_data/iedb.tsv'
    df = read_file(file)
    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], use_pages=True,pages_folder="pages",
               suppress_callback_exceptions=True)
    dash.register_page("home", layout=home.create_layout(df.head(10)), path="/", theme=[dbc.themes.FLATLY], )
    app.layout = html.Div([
        html.H1("BioProfileKit", style={'text-align': 'left', 'font-size': '24px'}),
        dash.page_container
    ])
    return app

if __name__ == '__main__':
    main()