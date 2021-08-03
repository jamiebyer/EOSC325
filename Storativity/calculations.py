
import numpy as np

g = 9.81 #gravitational acceleration in m/s^2
compressibility = 4.40*10**(-10) #water compressibility in m^2/N

#all arrays are in order: Clay, Sand, Gravel, Jointed Rock, Sound Rock

def alpha(inp_alpha):
    if inp_alpha == 'min':
        a = np.array([(10**(-8)), (10**(-9)), (10**(-10)), (10**(-10)), (10**(-11))])
    elif inp_alpha == 'avg':
        a = np.array([(10**(-7)), (10**(-8)), (10**(-9)), (10**(-8)), (10**(-10))])
    elif inp_alpha == 'max':
        a = np.array([(10**(-6)), (10**(-7)), (10**(-8)), (10**(-8)), (10**(-9))])
    return a #m^2/N

def porosity(inp_porosity):
    p = 0.3
    return p #dimensionless

def density(inp_density):
    d = 1000
    return d #kg/m^3

def specific_storage(inp_alpha, inp_porosity, inp_density):
    Ss = density(inp_density)*g*(alpha(inp_alpha) + porosity(inp_porosity)*compressibility)
    return Ss

def storativity(inp_alpha, inp_porosity, inp_density, inp_thickness):
    thickness = inp_thickness # in m
    S = specific_storage(inp_alpha, inp_porosity, inp_density)*thickness
    return S
