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
import numpy as np
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
            ### EOSC 325: The Thiem Equation
            ----------
            '''),
    ], style={'width': '100%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
            id='plot',
            config={
                'staticPlot': False,  # True, False
                'scrollZoom': False,  # True, False
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
                    **y-axis variable:**
                '''),
        dcc.RadioItems(
            id='y_var',
            options=[
                {'label': 'well discharge (Q)', 'value': 'Q'},
                {'label': 'aquifer transmissivity (T)', 'value': 'T'},
                {'label': 'head at inner radius (h1)', 'value': 'h1'},
                {'label': 'head at outer radius (h2)', 'value': 'h2'},
            ],
            value='Q',
            style={'margin-bottom': '30px'}
        ),
        html.Div(
            id='Q_container',
            children=[
                dcc.Markdown('''
                    **Well Discharge (Q) (m3/d):**
                '''),
                dcc.Slider(
                    id='Q',
                    min=0,
                    max=500,
                    step=1,
                    value=272.83,
                ),
        ]),

        html.Div(
            id='T_container',
            children=[
                dcc.Markdown('''
                        **Aquifer Transmissivity (T) (m2/d):**
                    '''),
                dcc.Slider(
                    id='T',
                    min=0,
                    max=50,
                    step=1,
                    value=8,
                ),
        ]),


        html.Div(
            id='h1_container',
            children=[
                dcc.Markdown('''
                            **Head at Inner Radius (h1) (m):**
                        '''),
                dcc.Slider(
                    id='h1',
                    min=0,
                    max=100,
                    step=1,
                    value=50,
                ),
        ]),

        html.Div(
            id='h2_container',
            children=[
                dcc.Markdown('''
                            **Head at Outer Radius (h2) (m):**
                        '''),
                dcc.Slider(
                    id='h2',
                    min=0,
                    max=100,
                    step=1,
                    value=100,
                ),
        ]),

        html.Div(
            id='r1_container',
            children=[
                dcc.Markdown('''
                            **Inner Radius (r1) (m):**
                        '''),
                dcc.Slider(
                    id='r1',
                    min=0,
                    max=2,
                    step=0.01,
                    value=0.1
                ),
        ]),

        html.Div(
            id='r2_container',
            children=[
                dcc.Markdown('''
                            **Outer Radius (r2) (m):**
                        '''),
                dcc.Slider(
                    id='r2',
                    min=10,
                    max=1000,
                    step=1,
                    value=1000,
                ),
        ]),

    ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'middle'}),


], style={'width': '1000px'})


#updating visibility:
@app.callback(
    Output(component_id='Q_container', component_property='style'),
    Input('y_var', 'value'),
)
def update_slider_visibility(y_var):
    if y_var == 'Q':
        return {'display':'none'}
    else:
        return {'display':'inline'}

@app.callback(
    Output(component_id='T_container', component_property='style'),
    Input('y_var', 'value'),
)
def update_slider_visibility(y_var):
    if y_var == 'T':
        return {'display':'none'}
    else:
        return {'display':'inline'}

@app.callback(
    Output(component_id='h1_container', component_property='style'),
    Input('y_var', 'value'),
)
def update_slider_visibility(y_var):
    if y_var == 'h1':
        return {'display':'none'}
    else:
        return {'display':'inline'}

@app.callback(
    Output(component_id='h2_container', component_property='style'),
    Input('y_var', 'value'),
)
def update_slider_visibility(y_var):
    if y_var == 'h2':
        return {'display':'none'}
    else:
        return {'display':'inline'}

#update plot

@app.callback(
    Output(component_id='plot', component_property='figure'),
    Input(component_id='y_var', component_property='value'),
    Input(component_id='Q', component_property='value'),
    Input(component_id='T', component_property='value'),
    Input(component_id='h1', component_property='value'),
    Input(component_id='h2', component_property='value'),
    Input(component_id='r1', component_property='value'),
    Input(component_id='r2', component_property='value'),
)
def update_plot(y_var, Q, T, h1, h2, r1, r2):

    x = np.linspace(r1, r2, 1000)

    if y_var == 'Q':
        y = calc.Q(T, h1, h2, r1, x)
    elif y_var == 'T':
        y = calc.T(Q, h1, h2, r1, x)
    elif y_var == 'h1':
        y = calc.h1(Q, T, h2, r1, x)
    elif y_var == 'h2':
        y = calc.h2(Q, T, h1, r1, x)

    fig = go.Figure(go.Scatter(x=x, y=y, mode='lines'))
    fig.update_layout(xaxis_title='r(m)', yaxis_title=y_var)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
