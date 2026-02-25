import math as m
import cmath as cm
import numpy as np

'''Complex Opperations'''
def polar(cplx_expr):
    polar_tup=cm.polar(cplx_expr)
    if polar_tup[0]==float(1):
        return 'e**('+str(polar_tup[1])+'j)'
    else:
        return str(polar_tup[0])+'e**('+str(polar_tup[1])+'j)'
def polard(cplx_expr):
    polar_tup=cm.polar(cplx_expr)
    if polar_tup[0]==float(1):
        return 'e**('+str(m.degrees(polar_tup[1]))+'j)'
    else:
        return str(polar_tup[0])+'e**('+str(m.degrees(polar_tup[1]))+'j)'
def rect(cplx_expr):
    return str(eval(str(cplx_expr)))
def sqrt(x):
    try: 
        x=m.sqrt(x)
    except:
        x=cm.sqrt(x)
        x=np.imag(x)*1j
    return x

'''Other'''
def quad(a,b,c):
    x=(-b+sqrt(b**2+4*a*c))/(2*a)
    y=(-b-sqrt(b**2+4*a*c))/(2*a)
    return str([x,y])

def mag(vector):
    return str(m.sqrt(sum(k*k for k in vector[0])))

def summation(start,end,var=str,f=str):
    sum_vector=[]
    for k in range(start,end+1):
        sum_vector.append(eval(f.replace(var,str(k))))
    return str(sum(sum_vector))

'''Trig Functions'''
def sind(x):
    return np.sin(m.radians(x))
def cosd(x):
    return np.cos(m.radians(x))
def tand(x):
    return np.tan(m.radians(x))
def asind(x):
    return m.degrees(np.asin(x))
def acosd(x):
    return m.degrees(np.acos(x))
def atand(x):
    return m.degrees(np.atan(x))
def sec(x):
    return np.cos(x)**-1
def csc(x):
    return np.sin(x)**-1
def cot(x):
    return np.tan(x)**-1
def secd(x):
    return np.cos(m.radians(x))**-1
def cscd(x):
    return np.sin(m.radians(x))**-1
def cotd(x):
    return np.tan(m.radians(x))**-1
def asecd(x):
    return m.degrees(np.arccos(x**-1))
def acscd(x):
    return m.degrees(np.arcsin(x**-1))
def acotd(x):
    return m.degrees(np.arctan(x**-1))
