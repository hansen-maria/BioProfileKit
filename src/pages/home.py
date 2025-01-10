import dash_bootstrap_components as dbc
import pandas as pd
from dash import html

list_style = {
    'listStyleType': 'disc',
    'padding': '10px',
    'font-size': '14px',
    'margin-left': '40px'
}
list_item_style = {
    'color': 'black',
    'margin-left': '40px'
}


def create_layout(df: pd.DataFrame):
    layout = html.Div([
        html.H1('Overview', style={'font-size': '28px', 'margin-left': '40px'}),
        dbc.Container([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.P(f"DataFrame has following shape {df.shape}.",
                           style={'font-size': '16px', 'margin-left': '40px'}),
                    html.P(f"DataFrame contains following columns ",
                           style={'font-size': '16px', 'margin-left': '40px'}),
                    html.Ul([html.Li(item, style=list_item_style) for item in df.columns.to_list()],
                            style=list_style),
                    html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line'}),
                ]),
                dbc.Col([
                    html.P("Hello World!")
                ])
            ])
        ]),

    ])
    return layout
