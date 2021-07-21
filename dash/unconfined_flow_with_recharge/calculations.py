import numpy as np

def get_d(h1, h2, K, W, L):
    d = (L/2)-(K/W)*((h1**2-h2**2)/(2*L))
    return d

def get_h(h1, h2, K, W, L, x):
    h = np.sqrt((h1**2)-(((h1**2-h2**2)*x)/L)+((W/K)*(L-x)*x))
    return h

def get_h_max(h1, h2, K, W, L):
    d = get_d(h1, h2, K, W, L)
    h = np.sqrt((h1**2)-(((h1**2-h2**2)*d)/L)+((W/K)*(L-d)*d))
    return h

def get_q(h1, h2, K, W, L, x):
    q = ((K*(h1**2-h2**2))/(2*L))-(W*((L/2)-x))
    return q