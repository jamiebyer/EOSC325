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

import  plotting as plot


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)

#initial parameter values
initial_h1 = 20
initial_h2 = 10
initial_K = 50
initial_W = 0.1
initial_L = 1000


app.layout = html.Div([

    html.Div([
        dcc.Markdown('''
            ### EOSC 325

            #### Unconfined Flow with Recharge

            ----------
            '''),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 30, 'margin-right': 50, 'margin-left': 20}),
    html.Div([
            dcc.Markdown(''' **_h1_ (m):** '''),
            dcc.Slider(
                id='h1', min=1, max=50, step=0.5, value=initial_h1,
                marks={1:'1', 50:'50'},
                tooltip={'always_visible':True, 'placement':'topLeft'}
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
            dcc.Markdown(''' **_h2_ (m):** '''),
            dcc.Slider(
                id='h2', min=1, max=50, step=0.5, value=initial_h2,
                marks={1:'1', 50:'50'},
                tooltip={'always_visible':True, 'placement':'topLeft'}
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
            dcc.Markdown(''' **_K_ (m/day):** '''),
            dcc.Slider(
                id='K', min=1, max=100, step=1, value=initial_K,
                marks={1:'1', 100:'100'},
                tooltip={'always_visible':True, 'placement':'topLeft'}
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
            dcc.Markdown(''' **_W_ (m/day):** '''),
            dcc.Slider(
                id='W', min=0.01, max=1, step=0.001, value=initial_W,
                marks={0.01:'0.01', 1:'1'},
                tooltip={'always_visible':True, 'placement':'topLeft'}
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
            dcc.Markdown(''' **_L_ (m):** '''),
            dcc.Slider(
                id='L', min=100, max=1000, step=5, value=initial_L,
                marks={100:'100', 1000:'1000'},
                tooltip={'always_visible':True, 'placement':'topLeft'}
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(
            id='elevation_plot',
            config={
                'staticPlot': True,  # True, False
                #'scrollZoom': True,  # True, False
                'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,  # True, False
                'displayModeBar': False,  # True, False, 'hover'
                'watermark': True,
                'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d'],
            },
        ),
    dcc.Graph(
            id='q_plot',
            config={
                'staticPlot': True,  # True, False
                #'scrollZoom': True,  # True, False
                'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,  # True, False
                'displayModeBar': False,  # True, False, 'hover'
                'watermark': True,
                'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d'],
            },
        )
    ], style={'width': '100%', 'display': 'inline-block'}),


], style={'width': '1000px'})



#initialize plots
elevation_plot = plot.initialize_elevation_plot(initial_h1, initial_h2, initial_K, initial_W, initial_L)
q_plot = plot.initialize_q_plot(initial_h1, initial_h2, initial_K, initial_W, initial_L)


@app.callback(
    Output(component_id='elevation_plot', component_property='figure'),
    Input(component_id='h1', component_property='value'),
    Input(component_id='h2', component_property='value'),
    Input(component_id='K', component_property='value'),
    Input(component_id='W', component_property='value'),
    Input(component_id='L', component_property='value')
)
def update_elevation_plot(h1, h2, K, W, L):
    fig = plot.update_elevation_plot(h1, h2, K, W, L, elevation_plot)
    return fig


@app.callback(
    Output(component_id='q_plot', component_property='figure'),
    Input(component_id='h1', component_property='value'),
    Input(component_id='h2', component_property='value'),
    Input(component_id='K', component_property='value'),
    Input(component_id='W', component_property='value'),
    Input(component_id='L', component_property='value')
)
def update_q_plot(h1, h2, K, W, L):
    fig = plot.update_q_plot(h1, h2, K, W, L, q_plot)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
