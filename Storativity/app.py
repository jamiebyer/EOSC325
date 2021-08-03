# -*- coding: utf-8 -*-

# Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/
# based on ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# mouse-over or 'hover' behavior is based on https://dash.plotly.com/interactive-graphing
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line
# Mapmaking code initially learned from https://plotly.com/python/mapbox-layers/.


from flask import Flask
from os import environ

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import calculations as calc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)


app.layout = html.Div([

    html.Div([
        dcc.Markdown('''
            ### EOSC 325: Storativity
            ----------
            '''),
    ], style={'width': '100%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
            id='plot',
            config={
                'staticPlot': True,  # True, False
                # 'scrollZoom': True,  # True, False
                'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,  # True, False
                'displayModeBar': False,  # True, False, 'hover'
                'watermark': True,
                'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d'],
            },
        ),
    ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([
        dcc.Markdown('''
            **Alpha:**
        '''),
        dcc.RadioItems(
            id='alpha',
            options=[
                {'label': 'min', 'value': 'min'},
                {'label': 'avg', 'value': 'avg'},
                {'label': 'max', 'value': 'max'}
            ],
            value='avg',
            labelStyle={'display': 'inline-block'},
            style={'margin-bottom': '30px'}
        ),

        dcc.Markdown('''
            **Porosity:**
        '''),
        dcc.RadioItems(
            id='porosity',
            options=[
                {'label': 'min', 'value': 'min'},
                {'label': 'middle', 'value': 'mid'},
                {'label': 'max', 'value': 'max'}
            ],
            value='mid',
            labelStyle={'display': 'inline-block'},
            style={'margin-bottom': '30px'}
        ),

        dcc.Markdown('''
            **Water Density:**
        '''),
        dcc.RadioItems(
            id='density',
            options=[
                {'label': 'potable', 'value': 'potable'},
                {'label': 'sea water', 'value': 'sea_water'},
                {'label': 'brine', 'value': 'brine'}
            ],
            value='sea_water',
            labelStyle={'display': 'inline-block'},
            style={'margin-bottom': '30px'}
        ),

        dcc.Markdown('''
            **Aquifer Thickness (m):**
        '''),
        dcc.Slider(
            id='thickness',
            min=1,
            max=30,
            step=None,
            marks={
                1: '1',
                2: '2',
                4: '4',
                8: '8',
                15: '15',
                30: '30'
            },
            value=15,
        )
    ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'middle'}),


], style={'width': '1000px'})


@app.callback(
    Output(component_id='plot', component_property='figure'),
    Input(component_id='alpha', component_property='value'),
    Input(component_id='porosity', component_property='value'),
    Input(component_id='density', component_property='value'),
    Input(component_id='thickness', component_property='value'),
)
def update_plot(inp_alpha, inp_porosity, inp_density, inp_thickness):
    materials = ['Clay', 'Sand', 'Gravel', 'Jointed Rock', 'Sound Rock']

    alpha, porosity, density, thickness = calc.alpha(inp_alpha), calc.porosity(inp_porosity), calc.density(inp_density), inp_thickness

    fig = go.Figure([go.Bar(x=materials, y=calc.storativity(alpha, porosity, density, thickness))])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
