
import numpy as np

def Q(T, h1, h2, r1, r2):
    Q = (2*np.pi*T*(h2-h1))/(np.log(r2/r1))
    return Q

def T(Q, h1, h2, r1, r2):
    T = (Q/(2*np.pi*(h2-h1)))*(np.log(r2/r1))
    return T

def h1(Q, T, h2, r1, r2):
    h1 = h2 - ((Q/(2*np.pi*T))*(np.log(r2/r1)))
    return h1

def h2(Q, T, h1, r1, r2):
    h2 = ((Q/(2*np.pi*T))*(np.log(r2/r1))) + h1
    return h2
