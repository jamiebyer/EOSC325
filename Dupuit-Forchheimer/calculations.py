
import numpy as np

def Q(K, h1, h2, r1, r2):
    Q = (np.pi*K*(h2**2-h1**2))/(np.log(r2/r1))
    return Q

def K(Q, h1, h2, r1, r2):
    if h1 != h2:
        K = (Q*np.log(r2/r1))/(np.pi*(h2**2-h1**2))
    else:
        K = 0
    return K

def h1(Q, K, h2, r1, r2):
    if K != 0:
        h1 = np.sqrt(h2**2-((Q*np.log(r2/r1))/(np.pi*K)))
    else:
        h1 = 0
    return h1

def h2(Q, K, h1, r1, r2):
    if K != 0:
        h2 = np.sqrt(((Q*np.log(r2/r1))/(np.pi*K))+h1**2)
    else:
        h2 = 0
    return h2
