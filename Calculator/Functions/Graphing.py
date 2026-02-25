from math import *
from Symbolic import diff,solve,solve_sys

def intersection(funct_list):
    
    #y_equals_funct_list=['y='+funct for funct in funct_list]
    #funct_list_str=str(y_equals_funct_list)
    #funct_list_str=funct_list_str.replace("'","")
    #funct_list_str=funct_list_str.replace(' ','')
    #print(funct_list_str)
    #complete_intersection=solve_sys(funct_list_str+',[x,y],x')
    #if complete_intersection=='No Solutions':
        #complete_intersection=0
    #print(complete_intersection)
    
    set_equals_list=[]
    for i in range(len(funct_list)):
        k=i+1
        while k<=len(funct_list)-1:
            set_equals_list.append(funct_list[i]+'='+funct_list[k])
            k+=1
        
    soln_list=[]
    for equality in set_equals_list:
        try:
            soln_list.append(solve(equality+',x')[2:])
        except:
            soln_list.append('No Solution')
    
    soln_list=[soln.replace('^','**') for soln in soln_list]
    soln_list=[soln.replace('ln','log') for soln in soln_list]
    soln_list=[eval(soln) for soln in soln_list]
    
    coordinate_list=[]
    for l in range(len(soln_list)):
        for s in soln_list[l]:
            if s != 'No Solution':
                coordinate_list.append((s,eval(set_equals_list[l][:set_equals_list[l].find('=')].replace('x','('+str(s)+')'))))
    
    return coordinate_list

def zeros(funct_list):
    coordinate_list=[]
    
    for funct in funct_list:
        x_soln_str=solve(str(funct)+',x')
        x_soln_str_list=x_soln_str[x_soln_str.find('=')+1:]
        x_soln_str_list=x_soln_str_list.replace(',','","')
        x_soln_str_list=x_soln_str_list.replace('[','["')
        x_soln_str_list=x_soln_str_list.replace(']','"]')
        x_soln_list=eval(x_soln_str_list)
        
        soln_list=[]
        for soln in x_soln_list:
            y_soln=eval(funct.replace('x','('+soln+')'))
            soln_list.append((soln,y_soln))

        coordinate_list.append(soln_list)
    
    return coordinate_list

def maxnmins(funct_list):
    coordinate_list=[]
    
    deriv_list=[diff(funct+',x') for funct in funct_list]
    
    soln_list=[]
    for i in range(len(deriv_list)):
        x_soln_str=solve(str(deriv_list[i])+',x')
        x_soln_str_list=x_soln_str[x_soln_str.find('=')+1:]
        x_soln_str_list=x_soln_str_list.replace(',','","')
        x_soln_str_list=x_soln_str_list.replace('[','["')
        x_soln_str_list=x_soln_str_list.replace(']','"]')
        x_soln_list=eval(x_soln_str_list)
        
        for x in x_soln_list:
            
            y_soln=eval(funct_list[i].replace('x',x))
            
            soln_list.append((eval(x),y_soln))
        coordinate_list.append(soln_list)
        soln_list=[]
    
    return coordinate_list

