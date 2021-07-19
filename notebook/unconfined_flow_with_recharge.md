---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# EOSC 325
# Unconfined Flow with Recharge

+++

![diagram.png](attachment:diagram.png)

```{code-cell} ipython3
#calculations
import numpy as np

def calc_d(h1, h2, K, W, L):
    d = (L/2)-(K/W)*((h1**2-h2**2)/(2*L))
    return d

def calc_h(h1, h2, K, W, L, x):
    h = np.sqrt((h1**2)-(((h1**2-h2**2)*x)/L)+((W/K)*(L-x)*x))
    return h

def calc_h_max(h1, h2, K, W, L):
    d = calc_d(h1, h2, K, W, L)
    h = np.sqrt((h1**2)-(((h1**2-h2**2)*d)/L)+((W/K)*(L-d)*d))
    return h

def calc_q(h1, h2, K, W, L, x):
    q = ((K*(h1**2-h2**2))/(2*L))-(W*((L/2)-x))
    return q
```

```{code-cell} ipython3
#graphing
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


def remove_mesh_points(X, Y, h1, h2, K, W, L):
    h = calc_h(h1, h2, K, W, L, X[0])
    
    for i in range(len(X)):
        for j in range(len(X[0])):
            if Y[i][j] > h[j]:
                X[i][j] = None
                Y[i][j] = None
                
    return [X, Y]



def update_graphs(h1, h2, K, W, L):
    x = np.linspace(0, L, 1000)
    h = calc_h(h1, h2, K, W, L, x)
    q = calc_q(h1, h2, K, W, L, x)
    d = calc_d(h1, h2, K, W, L)
    
    with elevation_plot.batch_update():
        # Updating specific traces using their index in plot.data
        #elevation plot
        elevation_plot.data[0].x = x
        elevation_plot.data[0].y = h
        
        index = min(range(len(x)), key=lambda i: abs(x[i]-d))
        elevation_plot.data[1].x = [d, d]
        elevation_plot.data[1].y = [0, h[index]]
        
        elevation_plot.update_xaxes(range=[0, L])
        
        
        
        #quiver plot
        x_quiver = np.linspace(L/8, L-(L/8), 8)
        y_quiver = np.linspace(0, (5/6)*calc_h_max(h1, h2, K, W, L), 5) #go to max y value
        X, Y = np.meshgrid(x_quiver, y_quiver)
        X, Y = remove_mesh_points(X, Y, h1, h2, K, W, L)
        u = calc_q(h1, h2, K, W, L, X)*20
        v = Y*0
        quiver_plot = ff.create_quiver(X, Y, u, v, arrow_scale=0.3, angle=np.pi/(9*16))
        
        elevation_plot.data[2].x = quiver_plot.data[0].x
        elevation_plot.data[2].y = quiver_plot.data[0].y
        
        
    with q_plot.batch_update():
        #q plot
        q_plot.data[0].x = x
        q_plot.data[0].y = q
        
        q_plot.update_xaxes(range=[0, L])
    
    
        


def initialize_graphs(h1, h2, K, W, L):
    # Initializing traces with plot.add_trace
    x = np.linspace(0, L, 1000) #should go to the max L value
    h = calc_h(h1, h2, K, W, L, x)
    q = calc_q(h1, h2, K, W, L, x)
    d = calc_d(h1, h2, K, W, L)
    
    #elevation plot
    elevation_plot.add_trace(go.Scatter(x=x, y=h, line=dict(color='MediumTurquoise'), name="h"))
    
    index = min(range(len(x)), key=lambda i: abs(x[i]-d))
    elevation_plot.add_trace(go.Scatter(x=[d, d], y=[0, h[index]], mode='lines', line=dict(color='FireBrick'), name="d"))
    
    elevation_plot.update_layout(xaxis_title='x', yaxis_title="Water Table Elevation (L)")
    elevation_plot.update_xaxes(range=[0, L])
    elevation_plot.layout.title = "Elevation Plot"
    elevation_plot.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    
    #elevation_plot.update_layout(annotations=get_arrows(h1, L, q, x))
    
    #quiver plot 
    x_quiver = np.linspace(L/8, L-(L/8), 8)
    y_quiver = np.linspace(0, (5/6)*calc_h_max(h1, h2, K, W, L), 5) #go to max y value
    X, Y = np.meshgrid(x_quiver, y_quiver)
    X, Y = remove_mesh_points(X, Y, h1, h2, K, W, L)
    u = calc_q(h1, h2, K, W, L, X)*20
    v = Y*0
    quiver_plot = ff.create_quiver(X, Y, u, v, arrow_scale=0.3, angle=np.pi/(9*16), name="qx")
    elevation_plot.add_traces(data=quiver_plot.data)
    
    
    #q plot
    q_plot.add_trace(go.Scatter(x=x, y=q, line=dict(color='MediumPurple'), name="q"))
    
    q_plot.add_trace(go.Scatter(x=[x[0], x[-1]], y=[0, 0], mode='lines', line=dict(color='FireBrick'), name="0"))
    
    q_plot.update_layout(xaxis_title='x', yaxis_title="qx (L^2/T)")
    q_plot.update_xaxes(range=[0, L])
    q_plot.layout.title = "q Plot"
    q_plot.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    
```

```{code-cell} ipython3
#widget handling
import ipywidgets as widgets
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#hydraulic conductivity: http://www.aqtesolv.com/aquifer-tests/aquifer_properties.htm

#starting values from: https://www.egr.msu.edu/igw/testing/Unconfined_Aquifer_rechrge.pdf
#parameters (in meters and days)
h1_slider = widgets.FloatSlider(value=20, min=1, max=50, step=0.5, description='h1 (L)')
h2_slider = widgets.FloatSlider(value=10, min=1, max=50, step=0.5, description='h2 (L)')
K_slider = widgets.FloatSlider(value=50, min=1, max=100, step=1, description='K (L/T)')
W_slider = widgets.FloatSlider(value=0.1, min=0.01, max=1, step=0.001, description='W (L/T)')
L_slider = widgets.FloatSlider(value=1000, min=100, max=1000, step=5, description='L (L)')

#units
#L_radiobuttons = widgets.RadioButtons(options=['km', 'm', 'cm'], value='m', 
#    description='L units:')
#T_radiobuttons = widgets.RadioButtons(options=['day', 'hour', 'min', 'sec'], value='day', 
#    description='T units:')


#functions, linked to the widgets, to update the plot when a widget is changed
def h1_eventhandler(change):
    update_graphs(change.new, h2_slider.value, K_slider.value, W_slider.value, L_slider.value)
def h2_eventhandler(change):
    update_graphs(h1_slider.value, change.new, K_slider.value, W_slider.value, L_slider.value)
def K_eventhandler(change):
    update_graphs(h1_slider.value, h2_slider.value, change.new, W_slider.value, L_slider.value)
def W_eventhandler(change):
    update_graphs(h1_slider.value, h2_slider.value, K_slider.value, change.new, L_slider.value)
def L_eventhandler(change):
    update_graphs(h1_slider.value, h2_slider.value, K_slider.value, W_slider.value, change.new)


    
#link the widgets to the appropriate event handler functions above
h1_slider.observe(h1_eventhandler, 'value')
h2_slider.observe(h2_eventhandler, 'value')
K_slider.observe(K_eventhandler, 'value')
W_slider.observe(W_eventhandler, 'value')
L_slider.observe(L_eventhandler, 'value')

#initialize plot
elevation_plot = go.FigureWidget()
q_plot = go.FigureWidget()
#quiver_plot = go.FigureWidget()
initialize_graphs(h1_slider.value, h2_slider.value, K_slider.value, W_slider.value, L_slider.value)

#selection_box = widgets.VBox([widgets.Label(value = "Parameters"), h1_slider, h2_slider, K_slider, W_slider, L_slider,
#                   widgets.Label(value = "Units"), L_radiobuttons, T_radiobuttons])
selection_box = widgets.VBox([widgets.Label(value = "Parameters (L in meters, T in days)"), h1_slider, h2_slider, K_slider, W_slider, L_slider])
plot_box = widgets.VBox([elevation_plot, q_plot])
output_box = widgets.HBox([plot_box, selection_box])
display(output_box)
```

```{code-cell} ipython3

```
