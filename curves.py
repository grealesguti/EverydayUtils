import numpy as np

def exponential(x, a, b, c):
    return a * np.exp(-b * x) + c

def logarithmic(x, a, b, c):
    return a * np.log(b * x) + c

def power(x, a, b, c):
    return a * x**b + c

def sine(x, a, b, c, d):
    return a * np.sin(b * x + c) + d

def cosine(x, a, b, c, d):
    return a * np.cos(b * x + c) + d

CURVE_FUNCS = [exponential, logarithmic, power, sine, cosine]
CURVE_TYPES = ['exponential', 'logarithmic', 'power', 'sine', 'cosine']
