from math import *
import numpy as np

def replace_string_element(str,index,value):
    str_list=list(str)
    str_list[index]=value
    return ''.join(str_list)

class DerivInterpreter():    
    
    def take_derivative(self,expression,var):
        sorted_list=self.decontructor(expression,var)
        final_expression=self.recompiler(sorted_list,var)
        return final_expression
    
    def decontructor(self,expression,var):
        #expression=' '+expression+' '
        list_of_parentesis_indexs=[]
        # if a u is discovered in a u it creates a list in place of the dictionary value for the original key and it keeps going until no more 'u's exist
        
        if expression.find('(')!=-1:
            while expression.find('(')!=-1:
                function_output=self.index_parenthesis(expression) # finds closing index for the internal function
                indexes=function_output[0]
                expression=function_output[1]
                list_of_parentesis_indexs.append(indexes)
        
            list_of_internal_expressions=self.pull_internal_expressions(expression,list_of_parentesis_indexs)
        else:
            list_of_internal_expressions=[]
        
        expression_list=self.expression_processor(expression,list_of_parentesis_indexs)
        list_of_internal_expressions=self.check_cmplx_expression(list_of_internal_expressions,var)
        sorted_list=self.chain_rule_sorting([expression_list,list_of_internal_expressions],var)
        
        return sorted_list
    
    def recompiler(self,sorted_list,var):
        final_expression_list=[]
        for i in range(len(sorted_list)):
            if type(sorted_list[i])==list:
                for k in range(len(sorted_list[i])):
                    if type(sorted_list[i][k])!=list and sorted_list[i][k].find('^')!=-1:
                        under_exponent=sorted_list[i][k][:sorted_list[i][k].find('^')]
                        in_exponent=sorted_list[i][k][sorted_list[i][k].find('^')+1:]
                        under_exponent=under_exponent.replace('(','')
                        under_exponent=under_exponent.replace(')','')
                        under_exponent=under_exponent.replace(' ','')
                        in_exponent=in_exponent.replace(' ','')
                        sorted_list[i][k]=under_exponent+'^'+in_exponent
                final_expression_list.append(self.classify_expressions(sorted_list[i],var))
            else:
                final_expression_list.append(sorted_list[i])
        for i in range(len(final_expression_list)):
            if type(final_expression_list[i])==list:
                if final_expression_list[i][1]=='1' and final_expression_list[i][2]!='':
                    final_expression_list[i]=final_expression_list[i][2]
                elif final_expression_list[i][1]=='-1':
                    final_expression_list[i]='-'+final_expression_list[i][2]
                elif final_expression_list[i][1]=='0':
                    final_expression_list[i]=''
                else:
                    final_expression_list[i]=final_expression_list[i][1]+final_expression_list[i][2]
        final_expression=''.join(final_expression_list)
        
        final_expression=final_expression.replace('+-','-')
        final_expression=final_expression.replace('--','+')
        final_expression=final_expression.replace('++','+')
        final_expression=final_expression.replace('-+','-')
        final_expression=final_expression.replace('+-','-')
        final_expression=final_expression.replace('-+','-')
        if final_expression[0]=='+':
            final_expression=final_expression[1:]
        if final_expression[-1]=='+' or final_expression[-1]=='-':
            final_expression=final_expression[:len(final_expression)-1]
        return final_expression
    
    def index_parenthesis(self,expression):
        open_u_index=expression.find('(')
        expression=replace_string_element(expression,expression.find('('),'{')
        if expression.find('(')<expression.find(')') and expression.find('(')!=-1:
            counter=1
            while counter==1:
                expression=replace_string_element(expression,expression.find('('),'[')
                expression=replace_string_element(expression,expression.find(')'),']')
                counter=counter-1
                if expression.find('(')<expression.find(')') and expression.find('(')!=-1:
                    counter+=1
            close_u_index=expression.find(')')
            expression=replace_string_element(expression,close_u_index,'}')
            expression=expression.replace('[','(')
            expression=expression.replace(']',')')
        else:
            close_u_index=expression.find(')')
            expression=replace_string_element(expression,close_u_index,'}')
        return [[open_u_index,close_u_index],expression]
    
    def pull_internal_expressions(self,expression,list_of_indexes):
        list_of_internal_expressions=[]
        for i in range(len(list_of_indexes)):
            list_of_internal_expressions.insert(0,expression[list_of_indexes[-i-1][0]+1:list_of_indexes[-i-1][1]])
        return list_of_internal_expressions
    
    def expression_processor(self,expression,par_index):
        temp_expression_list=[]
        
        last_cutoff_index=0
        k=0
        while k<len(expression):
            
            if expression[k] == '+' or expression[k] == '-':
                if expression[k-1]=='^':
                    k+=1
                else:
                    flag=0
                    for i in range(len(par_index)):
                        if par_index[i][0]<k<par_index[i][1]:
                           flag=1
                    if flag==1:
                        k+=1
                    else:
                        temp_expression_list.append(expression[last_cutoff_index:k])
                        temp_expression_list.append(expression[k])
                        last_cutoff_index=k+1
                        k+=1
            else:
                k+=1
        temp_expression_list.append(expression[last_cutoff_index:])
        return temp_expression_list
    
    def chain_rule_sorting(self,temp_expression_list,var):
        expression_list=[]
        external_expression_list=temp_expression_list[0]
        u_list=temp_expression_list[1]
        temp_list=[]
        for j in range(len(external_expression_list)):
            if external_expression_list[j].find('{')!=-1:
                temp_list.append(external_expression_list[j])
                for k in range(len(u_list)):
                    if type(u_list[k])==list:
                        if u_list[k][0] in external_expression_list[j]:
                            temp_list.append(u_list[k])
                            u_list[k]='`' 
                    else:   
                        if u_list[k] in external_expression_list[j]:
                            temp_list.append(u_list[k])
                            u_list[k]='`' 
                if temp_list[-1]!=var and type(temp_list[-1])!=list:
                    temp_list.append(var)
                expression_list.append(temp_list)
                temp_list=[]
            elif external_expression_list[j]!='+' and external_expression_list[j]!='-':
                expression_list.append([external_expression_list[j],var])
                
            else:
                expression_list.append(external_expression_list[j])       
        
        for h in range(len(expression_list)):
            if type(expression_list[h])==list:
                expression_list[h].reverse()
                temp_list=expression_list[h]
                
                for k in range(len(temp_list)):
                    if type(temp_list[k])==list:
                        temp_list[k][0]=temp_list[k][0].replace('{','(')
                        temp_list[k][0]=temp_list[k][0].replace('}',')')
                    else:
                        temp_list[k]=temp_list[k].replace('{','(')
                        temp_list[k]=temp_list[k].replace('}',')')
                reference_list=list(expression_list[h])
                for i in range(len(temp_list)):
                    if i != len(temp_list)-1:
                        if type(temp_list[i])==list:
                            temp_list[i+1]=temp_list[i+1].replace(reference_list[i][0],var)
                        else:
                            temp_list[i+1]=temp_list[i+1].replace(reference_list[i],var)
                expression_list[h]=temp_list        
                
                        
        return expression_list
        
    def check_cmplx_expression(self,internal_expression_list,var):
        for i in range(len(internal_expression_list)):
            copy=str(internal_expression_list[i])
            if internal_expression_list[i].count('x')>1 or internal_expression_list[i].find('+')!=-1:
                for k in range(i+1,len(internal_expression_list)):
                    if internal_expression_list[k] in internal_expression_list[i]:
                        internal_expression_list[k]='`'
                internal_expression_list[i]=internal_expression_list[i].replace('{','(')
                internal_expression_list[i]=internal_expression_list[i].replace('}',')')       
                int_cmplx_expression=CplxInternalExpression(internal_expression_list[i],var)     
                internal_expression_list[i]=[copy,int_cmplx_expression]
                return internal_expression_list
            elif internal_expression_list[i].find('-')!=-1 and internal_expression_list[i].find('-')!=0:
                for k in range(i+1,len(internal_expression_list)):
                    if internal_expression_list[k] in internal_expression_list[i]:
                        internal_expression_list[k]='`'
                internal_expression_list[i]=internal_expression_list[i].replace('{','(')
                internal_expression_list[i]=internal_expression_list[i].replace('}',')')
                int_cmplx_expression=CplxInternalExpression(internal_expression_list[i],var)     
                internal_expression_list[i]=[internal_expression_list[i],int_cmplx_expression]
                return internal_expression_list
            else:
                return internal_expression_list
    
    '''Classify each type of expression'''
    # eventually will become more complex as the classifications increase 
    def classify_expressions(self,temp_expression_list,var):
        # start from "inside" and work out defining each instance with the previous item in the list
        for i in range(len(temp_expression_list)):
            internal_exression=temp_expression_list[i]
            if type(internal_exression)==list:
                internal_exression=internal_exression[1]
            elif internal_exression.find('e')!=-1 or internal_exression.find('ln')!=-1 or internal_exression.find('log')!=-1:
                internal_exression=Exponential(internal_exression,var,temp_expression_list[i-1])
            elif internal_exression.find('^')!=-1:
                internal_exression=Exponent(internal_exression,var,temp_expression_list[i-1])
            elif internal_exression.find('cos')!=-1 or internal_exression.find('sin')!=-1 or  internal_exression.find('tan')!=-1:
                internal_exression=Trig(internal_exression,var,temp_expression_list[i-1])
            elif internal_exression.find(var)!=-1:
                internal_exression=SingleVar(internal_exression,var)
            elif internal_exression!='+' and internal_exression!='-':
                internal_exression=Constant(internal_exression)
            temp_expression_list[i]=internal_exression
        temp_expression_list.reverse()
        for k in range(len(temp_expression_list)):
            if temp_expression_list[k]!='+' and temp_expression_list[k]!='-':
                temp_expression_list[k]=temp_expression_list[k].derivative()
        return temp_expression_list[0]
        
# opperations and rules


# structure types 
class Exponent():
    def __init__(self,expression,variable_of_intergration,internal_expression):
        self.expression=expression
        self.var=variable_of_intergration
        self.internal_expression=internal_expression
        
    # differentiate between exponents of variables and standard exponents
    def derivative(self):
        list_of_num=[] 
        var_index=self.expression.find(self.var)
        internal_deriv_list=self.internal_expression.derivative()
        internal_deriv_expression=internal_deriv_list[2]
        internal_expression=internal_deriv_list[0]
        in_exp_int=str(eval(self.expression[var_index+2:])-1)
        
        temp_string=''
        h=0
        while h<len(internal_expression):
            try:
                if internal_expression[h]=='.':
                    temp_string=temp_string+'.'
                    h+=1
                else:
                    temp_string=temp_string+str(eval(internal_expression[h]))
                    h+=1
            except:
                leftovers=internal_expression[h:]
                h=len(internal_expression)
        if temp_string=='':        
            temp_string='1'
        
        list_of_num.append(temp_string+'**'+str(eval(self.expression[var_index+2:]+'-1')))
        list_of_num.append(internal_deriv_list[1])
        list_of_num.append(self.expression[:var_index])
        list_of_num.append(self.expression[var_index+2:])
        
        for i in range(len(list_of_num)):
            if list_of_num[i]=='':
                list_of_num[i]=1
            else:
                list_of_num[i]=eval(list_of_num[i])
        out_of_exp_sum=str(prod(list_of_num))
        
        new_expression='('+self.var+')'+self.expression[self.expression.find('^'):]
        new_expression=new_expression.replace(self.var,internal_expression)
        
        if in_exp_int!='1':
            return [new_expression, out_of_exp_sum, internal_deriv_expression+'('+leftovers+')^'+in_exp_int]
        else:
            return [new_expression, out_of_exp_sum, internal_deriv_expression+leftovers]
        
class Trig():
    def __init__(self,expression,variable_of_intergration,internal_expression):
        self.expression=expression
        self.var=variable_of_intergration
        self.internal_expression=internal_expression
        
    def derivative(self):
        temp_list=[]
        temp_nums=[]
        internal_deriv_list=self.internal_expression.derivative()
        internal_deriv_expression=internal_deriv_list[2]
        internal_expresssion=internal_deriv_list[0]
        # make it so that any number multiplied on the backside of the trig function is brought to the front
        if self.expression.find('acos')!=-1:
            pass
        
        elif self.expression.find('atan')!=-1:
            pass
        
        elif self.expression.find('asin')!=-1:
            pass
        
        elif self.expression.find('sin')!=-1:
            try:
                temp_nums.append(eval(self.expression[:self.expression.find('s')]))
                temp_nums.append(eval(internal_deriv_list[1])) 
            except:
                temp_nums.append(eval(internal_deriv_list[1]))
            
            temp_list.append(internal_deriv_expression)
            temp_list.append('cos(')
            temp_list.append(internal_expresssion)
            temp_list.append(self.expression[self.expression.find(')'):])
            
            new_expression=self.expression[:self.expression.find('s')]+'sin('+internal_expresssion+')'
            
            return [new_expression,str(prod(temp_nums)),''.join(temp_list)]
        
        elif self.expression.find('cos')!=-1:
            temp_nums.append(-1)
            try: 
                temp_nums.append(eval(self.expression[:self.expression.find('c')]))
                temp_nums.append(eval(internal_deriv_list[1]))
            except:
                temp_nums.append(eval(internal_deriv_list[1]))
                
            temp_list.append(internal_deriv_expression)
            temp_list.append('sin(')
            temp_list.append(internal_expresssion)
            temp_list.append(self.expression[self.expression.find(')'):])
            
            new_expression=self.expression[:self.expression.find('c')]+'cos('+internal_expresssion+')'
            
            return [new_expression,str(prod(temp_nums)),''.join(temp_list)]

        elif self.expression.find('tan')!=-1:
            try:
                temp_nums.append(eval(self.expression[:self.expression.find('t')]))
                temp_nums.append(eval(internal_deriv_list[1]))
            except:
                temp_nums.append(eval(internal_deriv_list[1]))
            
            temp_list.append(internal_deriv_expression)
            temp_list.append('sec(')
            temp_list.append(internal_expresssion)
            temp_list.append(')^2')
            
            new_expression=self.expression[:self.expression.find('t')]+'tan('+internal_expresssion+')'
            
            return [new_expression,str(prod(temp_nums)),''.join(temp_list)]
        
class Exponential():
    def __init__(self,expression,variable_of_intergration,internal_expression):
        self.expression=expression
        self.var=variable_of_intergration
        self.internal_expression=internal_expression
    
    def derivative(self):
        temp_list=[]
        temp_nums=[]
        internal_deriv_list=self.internal_expression.derivative()
        internal_deriv_expression=internal_deriv_list[2]
        internal_expression=internal_deriv_list[0]
        
        if self.expression.find('e')!=-1:
            temp_nums.append(internal_deriv_list[1])
            temp_nums.append(self.expression[:self.expression.find('e')])
            for i in range(len(temp_nums)):
                if temp_nums[i]=='':
                    temp_nums[i]=1
                else:
                    temp_nums[i]=eval(temp_nums[i])
            
            if internal_expression==self.var:
                new_expression=self.expression[:self.expression.find('^')+1]+self.var
            else: 
                new_expression=self.expression[:self.expression.find('^')+1]+'('+internal_expression+')'
            
            temp_list.append(internal_deriv_expression)
            temp_list.append('e^(')
            temp_list.append(internal_expression)
            temp_list.append(')')
            
            return [new_expression,str(prod(temp_nums)),''.join(temp_list)]
            
        # find way to simiplify results and cancel variables. 
        elif self.expression.find('ln')!=-1:
            temp_nums.append(internal_deriv_list[1])
            temp_nums.append(self.expression[:self.expression.find('l')])
                    
            for i in range(len(temp_nums)):
                if temp_nums[i]=='':
                    temp_nums[i]=1
                else:
                    temp_nums[i]=eval(temp_nums[i])
            
            if len(internal_deriv_expression)>1:
                temp_list.append('('+internal_deriv_expression+')/')
            else:
                if internal_deriv_expression=='':
                    temp_list.append('1/')
                else:
                    temp_list.append(internal_deriv_expression+'/')
            if len(internal_expression)>1:
                temp_list.append('('+internal_expression+')')
            else:
                temp_list.append(internal_expression)
            
            new_expression=self.expression.replace(self.var,internal_expression)
            
            return [new_expression,prod(temp_nums),''.join(temp_list)]
                
        elif self.expression.find('log')!=-1:
            pass
        
class Constant():
    def __init__(self,expression):
        self.expression=expression
    
    def derivative(self):
        return [self.expression,'0','']

class SingleVar():
    def __init__(self,expression,variable_of_intergration):
        self.expression=expression
        self.var=variable_of_intergration
    
    def derivative(self):
        list_of_nums=[]
        temp_string=''
        for i in range(len(self.expression)):
            if self.expression[i]=='x':
                list_of_nums.append(temp_string)
            else:
                temp_string=temp_string+self.expression[i]
        for k in range(len(list_of_nums)):
            if list_of_nums[k]=='':
                list_of_nums[k]='1'  
        if str(eval(''.join(list_of_nums)))=='1':
            new_expression=self.var
        else:
            new_expression=str(eval(''.join(list_of_nums)))+self.var
        return [new_expression,str(eval(''.join(list_of_nums))),'']
      
class CplxInternalExpression():
    def __init__(self,expression,variable_of_integration):
        self.expression=expression
        self.var=variable_of_integration
        
    def derivative(self):
        derivation=dip.take_derivative(self.expression,self.var)
        return [self.expression,'1','('+derivation+')']

dip=DerivInterpreter()

#l=SingleVar('x','x')
#k=Exponent('x^4','x',l)
#print(k.derivative())

# works
# '(sin(x))^2+cos(x^3)'


# 'e^(sin(x-4)-3)' 
# case where there is an internal expression but only one x
# 'e^(sin(x-4)-3x)' 
# case when there is multiple internal x's
# try a recursion method where it recogizes a 'complex internal expression' and runs it through the derivative function itself



