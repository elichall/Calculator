import numpy as np
import sympy as smp

'''cross product function'''
def cprod(a,b):
    if a.ndim and b.ndim != 2:
        return 'Error:OnlyVectorsAreAccepted'
    if len(a)!=1:
        a=a.transpose()
    if len(b)!=1:
        b=b.transpose()
    if a.shape and b.shape != (3,1):
        return 'Error:OnlyThreeEntryArraysAccepted'
    x=np.cross(a,b)
    return x

'''Dot Product Function or use math.sumprod()'''
def dprod(a,b):
    if a.ndim and b.ndim != 2:
        return 'Error:OnlyVectorsAreAccepted'
    if len(a)!=1:
        a=a.transpose()
    if len(b)!=1:
        b=b.transpose()
    sum_list=[]
    print(a,b)
    for i in range(np.shape(a)[1]):
        print(a[0,i],b[0,i])
        sum_list.append(a[0,i]*b[0,i])
    x=sum(sum_list)
    return x

def rref(a):
    return smp.Matrix(a).rref()[0]

def det(a):
    return smp.Matrix(a).det()