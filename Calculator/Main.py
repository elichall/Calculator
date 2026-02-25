import PyQt6.QtWidgets as qtw
from PyQt6.QtGui import QColor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
plt.style.use(['dark_background'])
from math import *
from Functions.General import *
from Functions.Symbolic import *
from Functions.MatrixFunctions import *

user_functions={}
user_vars=[]
user_funct=[]
history=[]
list_of_sympy_functions=['diff','intg','lim','solve_sys','solve']

'''Defines the main window and is the core brains of the whole calculator'''
class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.keypad()
        self.temp_nums=[]
        self.fin_nums=[]
        self.constantandfunctionlist=['pi','e','j']
        
    '''Defines Keyboard layout and functionality''' 
    def keypad(self):
        container=qtw.QWidget()
        container.setLayout(qtw.QGridLayout())
    
        #buttons
        self.result_field=qtw.QLineEdit()
        self.result_field.returnPressed.connect(self.input_field)
        btn_result=qtw.QPushButton('Enter',clicked=self.input_field)
        btn_clear=qtw.QPushButton('Clear',clicked=self.clear_calc)
        btn_9=qtw.QPushButton('9',clicked=lambda:self.num_press('9'))
        btn_8=qtw.QPushButton('8',clicked=lambda:self.num_press('8'))
        btn_7=qtw.QPushButton('7',clicked=lambda:self.num_press('7'))
        btn_6=qtw.QPushButton('6',clicked=lambda:self.num_press('6'))
        btn_5=qtw.QPushButton('5',clicked=lambda:self.num_press('5'))
        btn_4=qtw.QPushButton('4',clicked=lambda:self.num_press('4'))
        btn_3=qtw.QPushButton('3',clicked=lambda:self.num_press('3'))
        btn_2=qtw.QPushButton('2',clicked=lambda:self.num_press('2'))
        btn_1=qtw.QPushButton('1',clicked=lambda:self.num_press('1'))
        btn_0=qtw.QPushButton('0',clicked=lambda:self.num_press('0'))
        btn_plus=qtw.QPushButton('+',clicked=lambda:self.func_press('+'))
        btn_mins=qtw.QPushButton('-',clicked=lambda:self.func_press('-'))
        btn_mult=qtw.QPushButton('*',clicked=lambda:self.func_press('*'))
        btn_divd=qtw.QPushButton('/',clicked=lambda:self.func_press('/'))
        # general Functions
        btn_period=qtw.QPushButton('.',clicked=lambda:self.func_press('.'))
        btn_comma=qtw.QPushButton(',',clicked=lambda:self.func_press(','))
        btn_lbrackets=qtw.QPushButton('(',clicked=lambda:self.func_press('('))
        btn_rbrackets=qtw.QPushButton(')',clicked=lambda:self.func_press(')'))
        btn_sin=qtw.QPushButton('sin(x)',clicked=lambda:self.func_press('sin('))
        btn_cos=qtw.QPushButton('cos(x)',clicked=lambda:self.func_press('cos('))
        btn_tan=qtw.QPushButton('tan(x)',clicked=lambda:self.func_press('tan('))
        btn_asin=qtw.QPushButton('arcsin(x)',clicked=lambda:self.func_press('asin('))
        btn_acos=qtw.QPushButton('arccos(x)',clicked=lambda:self.func_press('acos('))
        btn_atan=qtw.QPushButton('arctan(x)',clicked=lambda:self.func_press('atan('))
        btn_e=qtw.QPushButton('e',clicked=lambda:self.func_press('e'))
        btn_log=qtw.QPushButton('log(x,b)',clicked=lambda:self.func_press('log('))
        btn_ln=qtw.QPushButton('ln(x)',clicked=lambda:self.func_press('log('))
        btn_power=qtw.QPushButton('a^x',clicked=lambda:self.func_press('^'))
        btn_sqrt=qtw.QPushButton('sqrt(a)',clicked=lambda:self.func_press('sqrt('))
        btn_pi=qtw.QPushButton('pi',clicked=lambda:self.func_press('pi'))
        # extra windows
        btn_graph=qtw.QPushButton('Side Window',clicked=lambda:Fw.open_side_window(Fw.subtab))
        btn_vars=qtw.QPushButton('empty',clicked=lambda:'')
        btn_func=qtw.QPushButton('LATEX',clicked=lambda:'')
        btn_funct=qtw.QPushButton('FUNCT',clicked=lambda:fw.open_window(fw))
        btn_options=qtw.QPushButton('OPTIONS',clicked=lambda:ow.open_window(ow))
        btn_clear_hist=qtw.QPushButton('Clear HIST',clicked=lambda:hw.history_list.clear())
        
        # adding buttons to layout
        container.layout().addWidget(self.result_field,0,0,1,6)
        container.layout().addWidget(btn_result,1,5)
        container.layout().addWidget(btn_clear,1,4)
        container.layout().addWidget(btn_9,2,2)
        container.layout().addWidget(btn_8,2,3)
        container.layout().addWidget(btn_7,2,4)
        container.layout().addWidget(btn_plus,2,5)
        container.layout().addWidget(btn_6,3,2)
        container.layout().addWidget(btn_5,3,3)
        container.layout().addWidget(btn_4,3,4)
        container.layout().addWidget(btn_mins,3,5)
        container.layout().addWidget(btn_3,4,2)
        container.layout().addWidget(btn_2,4,3)
        container.layout().addWidget(btn_1,4,4)
        container.layout().addWidget(btn_mult,4,5)
        container.layout().addWidget(btn_0,5,3,1,2)
        container.layout().addWidget(btn_divd,5,5)
        # Basic Functions
        container.layout().addWidget(btn_pi,1,0)
        container.layout().addWidget(btn_sin,2,0)
        container.layout().addWidget(btn_cos,3,0)
        container.layout().addWidget(btn_tan,4,0)
        container.layout().addWidget(btn_asin,5,0)
        container.layout().addWidget(btn_acos,6,0)
        container.layout().addWidget(btn_atan,6,1)
        container.layout().addWidget(btn_sqrt,5,1)
        container.layout().addWidget(btn_e,1,1)
        container.layout().addWidget(btn_ln,2,1)
        container.layout().addWidget(btn_log,3,1)
        container.layout().addWidget(btn_power,4,1)
        container.layout().addWidget(btn_lbrackets,1,2)
        container.layout().addWidget(btn_rbrackets,1,3)
        container.layout().addWidget(btn_period,5,2)
        container.layout().addWidget(btn_comma,6,2)
        # Other windows
        container.layout().addWidget(btn_graph,1,6)
        
        container.layout().addWidget(btn_vars,3,6)
        container.layout().addWidget(btn_func,2,6)
        container.layout().addWidget(btn_funct,4,6)
        container.layout().addWidget(btn_options,5,6)
        container.layout().addWidget(btn_clear_hist,6,6)
        # button color
        btn_result.setStyleSheet('background-color:black')
        btn_clear.setStyleSheet('background-color:black')
        btn_lbrackets.setStyleSheet('background-color:black')
        btn_rbrackets.setStyleSheet('background-color:black')
        btn_period.setStyleSheet('background-color:black')
        btn_comma.setStyleSheet('background-color:black')
        btn_graph.setStyleSheet('background-color:black')
        btn_options.setStyleSheet('background-color:black')
        btn_func.setStyleSheet('background-color:black')
        btn_vars.setStyleSheet('background-color:black')
        btn_funct.setStyleSheet('background-color:black')
        btn_clear_hist.setStyleSheet('background-color:black')
        btn_pi.setStyleSheet('background-color:grey;color:black')
        btn_e.setStyleSheet('background-color:grey;color:black')
        btn_sin.setStyleSheet('background-color:grey;color:black')
        btn_cos.setStyleSheet('background-color:grey;color:black')
        btn_tan.setStyleSheet('background-color:grey;color:black')
        btn_asin.setStyleSheet('background-color:grey;color:black')
        btn_acos.setStyleSheet('background-color:grey;color:black')
        btn_atan.setStyleSheet('background-color:grey;color:black')
        btn_sqrt.setStyleSheet('background-color:grey;color:black')
        btn_ln.setStyleSheet('background-color:grey;color:black')
        btn_log.setStyleSheet('background-color:grey;color:black')
        btn_power.setStyleSheet('background-color:grey;color:black')
        btn_plus.setStyleSheet('background-color:orange;color:black')
        btn_mins.setStyleSheet('background-color:orange;color:black')
        btn_divd.setStyleSheet('background-color:orange;color:black')
        btn_mult.setStyleSheet('background-color:orange;color:black')
        # container.layout().addWidget(btn_save_result,5,6)
        self.layout().addWidget(hw)
        self.layout().addWidget(container)
    def num_press(self,key_number):
        self.fin_nums=[str(self.result_field.text())]
        self.fin_nums.append(key_number)
        temp_string= ''.join(self.fin_nums)
        if self.fin_nums:
            self.result_field.setText(''.join(self.fin_nums))
        else:
            self.result_field.setText(temp_string)    
    def func_press(self,operator):
        self.fin_nums=[str(self.result_field.text())]
        self.fin_nums.append(operator)
        self.temp_nums=[]
        self.result_field.setText(''.join(self.fin_nums))
    def clear_calc(self):
        self.result_field.clear()
        self.temp_nums=[]
        self.fin_nums=[]   
    
    '''Interface between user input and calculator'''
    def input_field(self):
        org_string=str(self.result_field.text())
        str_result_string=self.process_input(str(self.result_field.text()))
        #try: # output formating
        
            #if len(str_result_string)>10:
                #str_result_string= '%E' % eval(str_result_string)
            #self.result_field.setText(str_result_string)
        #except:
        if str_result_string!='None' and str_result_string!=None:
            str_result_string=ow.check_complex_mode(str_result_string)
            str_result_string=self.to_calc_notation(str_result_string)
            self.result_field.setText(str_result_string)
            hw.add_to_history(org_string,str_result_string)  # add results to history 
            OppFunct.update_hist_memory()
        return
    def process_input(self,input):
        expression_counter=0
        fin_string=input # import the result field
        
        temp_string=fin_string.split('=')[0]
        if ('=' in fin_string) and (('(' not in temp_string) and ('[' not in temp_string)): 
            self.is_equals_sign(fin_string)
            return
                
        else: # if not, then evaluate  
            fin_string=self.to_system_notation(fin_string) # Change calculator notation to python processable inputs
            fin_string,expression_counter=self.check_sympy_function(fin_string,expression_counter)
            if expression_counter>0: # checks if the expression is symbolic and cannot be evaled
                fin_string=self.clean_up_sympy(fin_string)
                fin_string=self.to_calc_notation(fin_string)        
                return fin_string
            
            fin_string=self.check_variables(fin_string) # checks variables/funct
            
            if fin_string.find('[')!=-1: # is there a matrix
                str_result_string=self.matrix(fin_string)
            
            else: # evals string
                try:
                    fin_string=ow.check_degree_mode(fin_string)
                    str_result_string=str(eval(fin_string)) 
                except: 
                    str_result_string=fin_string
        
        return str_result_string
    def is_equals_sign(self,expression):
        function=expression.split('=')
        function[1]=self.check_abs_reference(function[1])          
        if function[0].find('{')!=-1: # check if the user is defining a function
            arguments=list(function[0][function[0].find('{')+1:function[0].find('}')].split(',')) # def function
            expression=[arguments,function[1]]
            if self.check_overwritting_vars(function[0][:function[0].find('{')])==True: #checks for overlapping function names
                self.result_field.setText('Attempted to overwrite constants(e, i, pi) or function')
            else: 
                user_functions[function[0][:function[0].find('{')]]=expression
                mw.result_field.clear()
                self.store_user_vars_and_funct(function[0],expression)
                graphed_funct=[item[2] for item in gw.function_storage]
                for i in range(len(graphed_funct)):
                    if function[0][:function[0].find('{')] == graphed_funct[i]:
                        gw.function_storage[i][0]=function[0]+'='+expression[1]
                gw.update_graph()
        else: # def variable
            if self.check_overwritting_vars(function[0])==True:  
                self.result_field.setText('Attempted to overwrite constants(e, i, pi) or function')
            else:
                hw.add_to_history(function[0],function[1])
                if function[1].find('[')!=-1:
                    user_functions[function[0]]=self.matrix(function[1])
                    mw.result_field.clear()
                else:
                    function[1]=self.to_system_notation(function[1])
                    try: 
                        function[1]=str(eval(function[1]))
                    except:
                        pass
                    user_functions[function[0]]=function[1]
                    mw.result_field.clear()
                self.store_user_vars_and_funct(function[0],user_functions[function[0]])
                gw.update_graph()
      
    '''Core of the dynamic variable system'''
    def check_variables(self,fin_string):
        k=0
        sorted_vars=sorted(list(user_functions.keys()),key=len) # sort so that the longest strings are indexed first
        sorted_vars.reverse()
        while k < len(list(user_functions.keys())): # checks if there is a variable in the expression
            
            if sorted_vars[k] in fin_string:
                key=sorted_vars[k] # stores name of variable being replaced
                fin_string=fin_string.replace(key,'`') # sets a dummy value for the variable
                item=str(user_functions[key]) # retrieves the user defined string associated with the variable
                key='`' 
                fin_string+=' ' # sets margin of error for +1 indexes
                if fin_string[fin_string.find(key)+1]=='{': # finds if the variable called is a function
                    while '`' in fin_string:
                        fin_string=self.var_is_funct(fin_string,item)
                    
                else: # if not function replace with the associated value of the variable
                    # checks for the index right after the key, if operator, proceed with replacing it, if not, don't replace and skip to next instance of variable
                    for n in range(fin_string.count(key)): 
                        if fin_string[fin_string.find(key)+1] in ['*','/','^','-','+',')',' ',',',';',']','.','0','1','2','3','4','5','6','7','8','9'] and fin_string[fin_string.find(key)-1] in ['*','/','^','-','+','(',' ',',','[',';','.','0','1','2','3','4','5','6','7','8','9']:
                            if fin_string[fin_string.find(key)-1] in ['0','1','2','3','4','5','6','7','8','9']:
                                str_list=list(fin_string)
                                str_list.insert(fin_string.find(key),'*')
                                fin_string=''.join(str_list)
                            if fin_string[fin_string.find(key)+1] in ['0','1','2','3','4','5','6','7','8','9']:
                                str_list=list(fin_string)
                                str_list.insert(fin_string.find(key)+1,'*')
                                fin_string=''.join(str_list)
                            fin_list=list(fin_string)
                            fin_list[fin_string.find(key)]=item
                            fin_string=''.join(fin_list)
                        else:
                            fin_list=list(fin_string)
                            fin_list[fin_string.find(key)]=sorted_vars[k]
                            fin_string=''.join(fin_list)                
            k+=1 
        return fin_string 
    def check_overwritting_vars(self,expression):
        a=False
        b=0
        while a == False and b<len(self.constantandfunctionlist):
            a=expression in self.constantandfunctionlist[b]
            b+=1
        return a
    def check_abs_reference(self,expression):
        expression+=' '
        if '$' in expression:
            index_list=[]
            for i in range(expression.count('$')):
                index_list.append(expression.find('$'))
                expression=self.replace_string_element(expression,expression.find('$'),'~')
            for i in range(len(index_list)):
                k=0
                add=2
                while k==0:
                    if expression[index_list[i]+add] in ['*','^','/','+','-',' ']:
                        str_slice=expression[index_list[i]+1:index_list[i]+add]
                        org_str=str(str_slice)
                        str_slice=self.check_variables(str_slice)
                        str_slice=str_slice.replace(' ','')
                        k=1
                    else:
                        add+=1
                expression_list=list(expression)   
                expression_list[index_list[i]:index_list[i]+add]=str_slice
                for j in range(len(index_list)):
                    index_list[j]=index_list[j]+(len(str_slice)-(len(org_str)+1))
                expression=''.join(expression_list)
        return expression
    def parnthesis_multiplication(self,expression):
        expression=' '+expression+' '
        open_count=expression.count('(')
        close_count=expression.count(')')
        for i in range(open_count):
            if expression[expression.find('(')-1] in ['0','1','2','3','4','5','6','7','8','9',')']:
                str_list=list(expression)
                str_list.insert(expression.find('('),'*')
                str_list[expression.find('(')+1]='~'
                expression=''.join(str_list)
            else:
                str_list=list(expression)
                str_list[expression.find('(')]='~'
                expression=''.join(str_list)
        expression=expression.replace('~','(')
        for i in range(close_count):
            if expression[expression.find(')')+1] in ['0','1','2','3','4','5','6','7','8','9','(']:
                str_list=list(expression)
                str_list.insert(expression.find(')')+1,'*')
                str_list[expression.find(')')]='~'
                expression=''.join(str_list)
            else:
                str_list=list(expression)
                str_list[expression.find(')')]='~'
                expression=''.join(str_list)
        expression=expression.replace('~',')')
        return expression
    def to_system_notation(self,expression):
        expression=' '+expression+' '
        
        for i in range(expression.count('j')):
            if expression[expression.find('j')-1]==')':
                expression=self.replace_string_element(expression,expression.find('j'),'*1`')
            elif expression[expression.find('j')+1]=='(':     
                expression=self.replace_string_element(expression,expression.find('j'),'1`*')
            elif expression[expression[expression.find('j')-1]=='*']:
                expression=self.replace_string_element(expression,expression.find('j'),'1`')
            elif expression[expression[expression.find('j')+1]=='*'] and expression[expression[expression.find('j')-1]] not in ['9','8','7','6','5','4','3','2','1','0']:
                expression=self.replace_string_element(expression,expression.find('j'),'1`')
        expression=expression.replace('`','j')   
        
        for i in range(expression.count('e')):
            if expression[expression.find('e')-1] in ['9','8','7','6','5','4','3','2','1','0']:
                expression=self.replace_string_element(expression,expression.find('e'),'*`')
        expression=expression.replace('`','e') 
        
        expression=expression.replace('^','**')
        expression=expression.replace('ln','log')
        #expression=ow.check_degree_mode(expression)
        expression=self.parnthesis_multiplication(expression)
        expression=expression.replace(' ','')
        return expression
    def to_calc_notation(self,expression):
        expression=expression.replace('**','^')
        expression=expression.replace('log','ln')
        return expression
    
    '''Core of Dynamic Functions'''
    def var_is_funct(self,fin_string,item):
        if fin_string.find('}')<fin_string.find('`'): # finds correct function indexes
            modified_string=fin_string[fin_string.find('}')+1:]
            stored_string=fin_string[:fin_string.find('}')+1]
            h=0
            while h==0: 
                if modified_string.find('}')<modified_string.find('`'):
                    modified_string_2=modified_string[:modified_string.find('}')+1]
                    modified_string=modified_string[modified_string.find('}')+1:]
                    stored_string=stored_string+modified_string_2
                else:
                    h=1
            close_funct_index=len(stored_string)+modified_string.find('}')   
        else:
            close_funct_index=fin_string.find('}')
        
        variables_string=fin_string[fin_string.find('`')+2:close_funct_index] # extracts the internal function string for evaluation  
        
        variables_string=' '+variables_string+' '
        
        variables_list=variables_string.split(',') # Proccesses string in preperation for the eval function
        
        evaluated_string=self.eval_function(eval(item),variables_list) # evaluate the function
        
            
        fin_string=fin_string.replace(fin_string[fin_string.find('`'):close_funct_index+1],evaluated_string)# replaces fin_string with the evaluated function
        
        return fin_string
    def eval_function(self,f,var):
        expression=f[1]
        
        result=''
        for l in range(len(var)):
            expression=expression.replace(f[0][l],var[l])
        expression=self.check_variables(expression)
        expression=self.to_system_notation(expression)  
        if expression.find('[')!=-1:     
            result=self.matrix(expression)
        else:  
            try:   
                result=str(eval(expression))
            except:
                result=expression
                result=result.replace(' ','')
        return result
    
    '''Compatability functions with numpy and scipy arrays'''
    def matrix(self,evaluation_string):
        evaluation_string=self.into_np_format(evaluation_string)
        evaluation_string=self.check_linalg(evaluation_string)
        evaluated_matix=eval(evaluation_string)
        evaluated_string=self.out_np_format(evaluated_matix)
        return evaluated_string
    def check_linalg(self,evaluation_string):
        if evaluation_string.find('.*')!=-1:
            evaluation_string=evaluation_string.replace('np.array([[',"np.matrix('[")
            evaluation_string=evaluation_string.replace('],[',';')
            evaluation_string=evaluation_string.replace('], [',';')
            evaluation_string=evaluation_string.replace(']])',"]')")
            evaluation_string=evaluation_string.replace('.*','*')
        return evaluation_string
    def into_np_format(self,vector_string):
        vector_string=vector_string.replace('[','np.array([[')
        vector_string=vector_string.replace(']',']])')
        vector_string=vector_string.replace(';','],[')
        if vector_string.find('.(')!=-1:
            vector_string=vector_string.replace('.(','`')
            if vector_string.find(')')<vector_string.find('`'): # finds correct function indexes
                modified_string=vector_string[vector_string.find(')')+1:]
                stored_string=vector_string[:vector_string.find(')')+1]
                h=0
                while h==0: 
                    if modified_string.find(')')<modified_string.find('`'):
                        modified_string_2=modified_string[:modified_string.find(')')+1]
                        modified_string=modified_string[modified_string.find(')')+1:]
                        stored_string=stored_string+modified_string_2
                    else:
                        h=1
                index=len(stored_string)+modified_string.find(')')   
            else:
                index=vector_string.find(')')
            vector_list=list(vector_string)
            vector_list[index]=']'
            vector_string=''.join(vector_list)
            vector_string=vector_string.replace('`','[')
        return vector_string
    def out_np_format(self,array):
        array_string=str(np.array(array).tolist())
        array_string=array_string.replace('np.array([[','[')
        array_string=array_string.replace(']])',']')
        array_string=array_string.replace('[[','[')
        array_string=array_string.replace(']]',']')
        array_string=array_string.replace('],[',';') 
        array_string=array_string.replace('], [',';') 
        return array_string
    
    '''Compatability w/ sympy'''
    def check_sympy_function(self,fin_string,counter):
        mapped_vars={}
        for item in list_of_sympy_functions:
            while item in fin_string:
                flag=0
                extracted_string=fin_string[fin_string.find(item)+len(item):]
                org_extracted_string=str(extracted_string)
                extracted_string,counter=self.check_sympy_function(extracted_string,counter)
                
                if '{' in extracted_string: # processes internal functions specific to sympy
                    flag=1
                    extracted_string,funct_vars_list=self.sympy_funct_eval(extracted_string)
                    
                extracted_string=extracted_string.replace(' ','')
                fin_string=fin_string.replace(org_extracted_string,extracted_string)
                left_over=fin_string[:fin_string.find(item)+len(item)]
                parn_index=self.index_parenthesis(extracted_string)
                
                method='' # finds a potential method used on the sympy function
                org_method=''
                fin_string+=' '
                if fin_string[parn_index[1]+len(left_over)+1]=='.':
                    after_str=fin_string[parn_index[1]+len(left_over)+2:]
                    method_parn_index=self.index_parenthesis(after_str)
                    org_method='.'+after_str[:method_parn_index[1]+1]
                    after_str=self.replace_string_element(after_str,after_str.find('('),'("')
                    after_str=self.replace_string_element(after_str,method_parn_index[1]+1,'")')
                    method='.'+after_str[:method_parn_index[1]+3]
                    
                fin_string_slice=fin_string[fin_string.find(item):parn_index[1]+len(left_over)+1] # the sympy function evaluated
                saved_fin_string_slice=str(fin_string_slice)+org_method
                fin_string_slice+=method # the sympy function+method
                fin_string_slice=self.replace_string_element(fin_string_slice,fin_string_slice.find('('),'("') # cleanup and processing for eval function
                fin_string_slice=self.replace_string_element(fin_string_slice,parn_index[1]+len(left_over)+1,'")')
                evaluated_slice=str(eval(fin_string_slice))
                
                if flag != 0: # processes if a function was used in the sympy function
                    for i in range(len(funct_vars_list)):
                        for k in range(len(funct_vars_list[i][0])):
                            if funct_vars_list[i][0][k] in list(mapped_vars.keys()) and mapped_vars[funct_vars_list[i][0][k]]!=funct_vars_list[i][1][k]:
                                return 'Error:DoubleValueAssignment',counter
                            else:
                                mapped_vars[funct_vars_list[i][0][k]]=funct_vars_list[i][1][k]
                            evaluated_slice=evaluated_slice.replace(funct_vars_list[i][0][k],funct_vars_list[i][1][k])
                    try:
                        evaluated_slice=str(eval(evaluated_slice))
                    except:
                        pass
                fin_string=fin_string.replace(saved_fin_string_slice,evaluated_slice)
                #fin_string=fin_string.replace(' ','')
                counter+=1
        return fin_string,counter
    def clean_up_sympy(self,expression): 
        expression=expression.replace('**','^')
        expression=expression.replace('log','ln')
        expression=expression.replace('exp','e^')
        return expression
    def sympy_funct_eval(self,fin_string): # evals a myfunction after preforming a sympy function on it
        funct_vars_list=[]
        sorted_vars=sorted(list(user_functions.keys()),key=len) # sort so that the longest strings are indexed first
        sorted_vars.reverse()
        for k in range(len(sorted_vars)):
            if sorted_vars[k] in fin_string and type(user_functions[sorted_vars[k]])==list:
                key=sorted_vars[k] # stores name of variable being replaced
                fin_string=fin_string.replace(key,'`') # sets a dummy value for the variable
                funct_list=user_functions[key] # retrieves the user defined string associated with the variable
                args=funct_list[0]
                expr=funct_list[1]
                key='`' 
                fin_string+=' ' # sets margin of error for +1 indexes
                    
                while '`' in fin_string:
            
                    if fin_string.find('}')<fin_string.find('`'): # finds correct function indexes
                        modified_string=fin_string[fin_string.find('}')+1:]
                        stored_string=fin_string[:fin_string.find('}')+1]
                        h=0
                        while h==0: 
                            if modified_string.find('}')<modified_string.find('`'):
                                modified_string_2=modified_string[:modified_string.find('}')+1]
                                modified_string=modified_string[modified_string.find('}')+1:]
                                stored_string=stored_string+modified_string_2
                            else:
                                h=1
                        close_funct_index=len(stored_string)+modified_string.find('}')   
                    else:
                        close_funct_index=fin_string.find('}')
                    
                    variables_string=fin_string[fin_string.find('`')+2:close_funct_index] # extracts the internal function string for evaluation  
                    
                    variables_list=variables_string.split(',') # Proccesses string in preperation for the eval function
                    
                    funct_vars_list.append([args,variables_list])
                    fin_string=fin_string.replace(key+'{'+variables_string+'}','('+expr+')')
                
        return self.to_system_notation(fin_string),funct_vars_list
    
    '''Storage of functions and variables'''
    def store_user_vars_and_funct(self,key,value):
        has_it_been_stored=0
        if type(value)==list:
            for i in range(len(user_funct)):
                if user_funct[i][0][:user_funct[i][0].find('{')]==key[:key.find('{')]:
                    user_funct[i][0]=key.replace(' ','')
                    user_funct[i][1]=[value[0],value[1].replace(' ','')]
                    has_it_been_stored=1
            flag=-1
            for k in range(len(user_vars)):
                if user_vars[k][0]==key[:key.find('{')]:
                    flag=k
            if flag!=-1:
                del user_vars[flag]
            if has_it_been_stored==0:
                user_funct.append([key,value])
            mfw.update_functions_list()
            vw.update_variable_list()
            OppFunct.update_memory()
        else:
            for j in range(len(user_vars)):
                if user_vars[j][0]==key:
                    user_vars[j][1]=value
                    has_it_been_stored=1
            flag=-1
            for h in range(len(user_funct)):
                if user_funct[h][0][:user_funct[h][0].find('{')]==key:
                    flag=h
            if flag!=-1:
                del user_funct[flag]
            if has_it_been_stored==0:
                value=value.replace(' ','')
                key=key.replace(' ','')
                user_vars.append([key,value])
            vw.update_variable_list()
            mfw.update_functions_list()
            OppFunct.update_memory()

    '''Extra'''
    def replace_string_element(self,str,index,value):
        str_list=list(str)
        str_list[index]=value
        return ''.join(str_list)
    def index_parenthesis(self,expression):
        open_u_index=expression.find('(')
        expression=self.replace_string_element(expression,expression.find('('),'{')
        if expression.find('(')<expression.find(')') and expression.find('(')!=-1:
            counter=1
            while counter==1:
                expression=self.replace_string_element(expression,expression.find('('),'[')
                expression=self.replace_string_element(expression,expression.find(')'),']')
                counter=counter-1
                if expression.find('(')<expression.find(')') and expression.find('(')!=-1:
                    counter+=1
            close_u_index=expression.find(')')
            expression=self.replace_string_element(expression,close_u_index,'}')
            expression=expression.replace('[','(')
            expression=expression.replace(']',')')
        else:
            close_u_index=expression.find(')')
            expression=self.replace_string_element(expression,close_u_index,'}')
        return [open_u_index,close_u_index]
    
'''Defines the variable window'''        
class VarsWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.keypad()
        self.varscontainer=qtw.QListWidget()
        self.varscontainer.show()
        self.layout().addWidget(self.varscontainer)
        self.varscontainer.itemDoubleClicked.connect(self.btn_clicked)
        
    def btn_clicked(self,btn):
        mw.result_field.setText(btn.text())
    
    def keypad(self):
        container=qtw.QWidget()
        container.setLayout(qtw.QGridLayout())
        
        label_name=qtw.QLabel()
        label_name.setText('Variables')
        btn_clear=qtw.QPushButton('Clear',clicked=lambda:self.clear_vars())
        btn_save=qtw.QPushButton('Export',clicked=lambda:self.export_vars())
        
        container.layout().addWidget(label_name,0,0)
        container.layout().addWidget(btn_clear,1,0)
        container.layout().addWidget(btn_save,1,1)
        self.layout().addWidget(container)
         
                    
    def update_variable_list(self):
        self.varscontainer.clear()
        for i in range(len(user_vars)):
            self.varscontainer.addItem(f'{user_vars[i][0]}={user_vars[i][1]}')
                
    def clear_vars(self):
        global user_functions 
        list_of_keys=list(user_functions.keys())
        for i in range(len(user_vars)):
            if user_vars[i][0] in list_of_keys:
                del user_functions[user_vars[i][0]]
        user_vars.clear()
        self.varscontainer.clear()
        OppFunct.update_memory()
        gw.update_graph()
    
    def export_vars(self):
        pass

'''My Functions Window'''
class MyFunctionsWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.keypad()
        self.functcontainer=qtw.QListWidget()
        self.functcontainer.show()
        self.layout().addWidget(self.functcontainer)
        self.functcontainer.itemDoubleClicked.connect(self.btn_clicked)
        
    def keypad(self):
        container=qtw.QWidget()
        container.setLayout(qtw.QGridLayout())
        
        label_name=qtw.QLabel()
        label_name.setText('Functions')
        btn_clear=qtw.QPushButton('Clear',clicked=lambda:self.clear_funct())
        btn_save=qtw.QPushButton('Save',clicked=lambda:self.export_funct())
        
        container.layout().addWidget(label_name,0,0)
        container.layout().addWidget(btn_clear,1,0)
        container.layout().addWidget(btn_save,1,1)
        self.layout().addWidget(container)
         
    def btn_clicked(self,btn):
        mw.result_field.setText(btn.text())
    
    def update_functions_list(self):
        self.functcontainer.clear()
        for i in range(len(user_funct)):
            self.functcontainer.addItem(user_funct[i][0]+'='+str(user_funct[i][1][1]))
    
    def clear_funct(self):
        global user_functions 
        list_of_keys=list(user_functions.keys())
        for i in range(len(user_funct)):
            if user_funct[i][0][:user_funct[i][0].find('{')] in list_of_keys:
                del user_functions[user_funct[i][0][:user_funct[i][0].find('{')]]
        user_funct.clear()
        self.functcontainer.clear()
        gw.function_storage.clear()
        gw.function_list.clear()
        OppFunct.update_memory()
        OppFunct.update_graph_memory()
        
    def export_funct(self):
        pass

'''Graphing Window'''
class GraphWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
        self.layout().addWidget(self.canvas)
        self.ax=self.figure.add_subplot(111)
        self.initialize_plot()
        
        self.xrange_input=qtw.QLineEdit()
        self.xrange_input.setText('-10,10')
        self.yrange_input=qtw.QLineEdit()
        self.yrange_input.setText('-10,10')
        
        self.functions_bloc=qtw.QWidget()
        self.functions_bloc.setLayout(qtw.QGridLayout())
        self.input_field=qtw.QLineEdit()
        
        self.color_field=qtw.QLineEdit()
        self.setup_functions_bloc()
        
        self.function_list=qtw.QListWidget()
        self.function_storage=[]
        
        self.settings_bloc=qtw.QWidget()
        self.settings_bloc.setLayout(qtw.QGridLayout())
        self.setup_settings_bloc()
        
        self.color_list=['#8dd3c7','#feffb3','#bfbbd9','#fa8174','#81b1d2','#fdb462','#b3de69','#bc82bd','#ccebc4','#ffed6f']
        self.input_field.returnPressed.connect(lambda: self.input_processing(str(self.input_field.text()),1,str(self.color_field.text())))
        
    '''Setting up Window'''
    def initialize_plot(self):
        self.ax.plot()
        xr_list=[-10,10]
        yr_list=[-10,10]
        self.ax.set_xlim(xr_list[0],xr_list[1])
        self.ax.set_ylim(yr_list[0],yr_list[1])
        self.ax.axhline(linewidth=2, color="w")
        self.ax.axvline(linewidth=2, color="w")
        self.ax.grid()
        self.scatter=self.ax.scatter([],[])
        self.annotations=self.ax.annotate(
            text='hello',
            xy=(5,5),
            xytext=(15,15), # distance from point
            textcoords='offset points',
            arrowprops={'arrowstyle': '->','facecolor':'black'}
        )
        self.annotations.set_visible(False)
        
        self.canvas.mpl_connect('motion_notify_event',self.motion_hover)
        self.canvas.draw()
    
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.canvas)
    def setup_settings_bloc(self):
        functions_label=qtw.QLabel()
        functions_label.setText('Graphing Functions')
        xrange=qtw.QLabel()
        xrange.setText('xrange:')
        yrange=qtw.QLabel()
        yrange.setText('yrange:')
        btn_update=qtw.QPushButton('Set Range',clicked=lambda:self.update_graph())
        btn_smart_range=qtw.QPushButton('Smart Range',clicked=lambda:self.smart_range())
        btn_mins_max=qtw.QPushButton('MIN/MAX',clicked=lambda:self.maxnmins())
        btn_intersect=qtw.QPushButton('INTERSECT',clicked=lambda:self.intersection())
        btn_zeros=qtw.QPushButton('ZEROS',clicked=lambda:self.zeros())
        
        self.settings_bloc.layout().addWidget(btn_update,0,0)
        self.settings_bloc.layout().addWidget(btn_smart_range,1,0)
        
        self.settings_bloc.layout().addWidget(xrange,0,1)
        self.settings_bloc.layout().addWidget(self.xrange_input,0,2)
        
        self.settings_bloc.layout().addWidget(yrange,1,1)
        self.settings_bloc.layout().addWidget(self.yrange_input,1,2)
        
        self.settings_bloc.layout().addWidget(functions_label,2,0)
        
        self.settings_bloc.layout().addWidget(btn_intersect,3,0)
        self.settings_bloc.layout().addWidget(btn_mins_max,3,1)
        self.settings_bloc.layout().addWidget(btn_zeros,3,2)
    def setup_functions_bloc(self):
        btn_graph=qtw.QPushButton('Graph',clicked=lambda:self.input_processing(str(self.input_field.text()),1,str(self.color_field.text())))
        btn_clear=qtw.QPushButton('empty',clicked=lambda:'')
        btn_clear_all=qtw.QPushButton('Clear All',clicked=lambda:self.clear_all())
        
        input_label=qtw.QLabel('Input:')
        graph_widget=qtw.QWidget()
        graph_widget.setLayout(qtw.QGridLayout())
        graph_widget.layout().addWidget(input_label,0,0)
        graph_widget.layout().addWidget(self.input_field,0,1)
        color_label=qtw.QLabel('Color:')
        color_widget=qtw.QWidget()
        color_widget.setLayout(qtw.QGridLayout())
        color_widget.layout().addWidget(color_label,0,0)
        color_widget.layout().addWidget(self.color_field,0,1)
        
        self.functions_bloc.layout().addWidget(graph_widget,0,0,1,2)
        self.functions_bloc.layout().addWidget(btn_clear,0,2)
        self.functions_bloc.layout().addWidget(btn_clear_all,1,2)
        self.functions_bloc.layout().addWidget(btn_graph,1,0,1,1)
        self.functions_bloc.layout().addWidget(color_widget,2,0) 

    '''Processing User Inputs'''
    def input_processing(self,f,flag,color):
        f=f.replace(' ','')
        f_org=str(f)
        error=''
        
        f_org=mw.check_abs_reference(f_org)
        f_org=mw.to_calc_notation(f_org)
        f=f.replace('$','')
        
        f=self.next_to_multiplication(f)
        
        if f.find('=')!=-1: # case where user is defining something
            mw.is_equals_sign(f)
            f_list=f.split('=')
            f_name=f_list[0]
            f=f_list[1]
            if f_name.find('{')!=-1:
                f=mw.process_input(f)
                f_name=f_name[:f_name.find('{')]
                samename=self.check_repeated_name(f_org,f_name,flag)
                if samename==0:
                    self.plot(f,f_name,f_org,flag,color,error) 
            else: 
                self.input_field.clear()
                self.color_field.clear()
                self.update_graph()
                
        else: # case where user is either typing a function or entering a previously defined function to be graphed
            is_function=0
            
            try:
                if f in user_functions.keys():
                    replace=user_functions[f]
                    f_name=f
                    if str(replace).replace(' ','')[-2:]=="']":
                        f_args=','.join(replace[0])
                        f=replace[1]
                        f_org=f_name+'{'+','.join(f_args)+'}='+f
                        is_function=1
                    else:
                        f=str(replace)
                        f_org=f_name+'='+f
                        is_function=1
            except:
                error='!'
                
            if is_function==1:
                samename=self.check_repeated_name(f_org,f_name,flag)
                if samename==0:
                    f=mw.process_input(f)
                    self.plot(f,f_name,f_org,flag,color,error) 
            else: 
                f_name='y='
                try: 
                    f=mw.process_input(f)
                except:
                    error = '!'
                samename=self.check_repeated_name(f_org,f_name,flag)
                if samename==0:
                    self.plot(f,f_name,f_org,flag,color,error)
                    
        OppFunct.update_graph_memory()
    def plot(self,f,f_name,f_org,flag,color,error):
        self.input_field.clear()
        self.color_field.clear()

        color=self.color_system(color)
        
        xlist=eval('['+str(self.xrange_input.text())+']')
        ylist=eval('['+str(self.yrange_input.text())+']')
        if '[' in f:
            f='['+f+']'
            f=f.replace(';','],[')
            try:
                scatter_points_list=eval(f)
                x_list=[point[0] for point in scatter_points_list]
                y_list=[point[1] for point in scatter_points_list]
                self.scatter=self.ax.scatter(x_list,y_list,c=color,s=10)
            except:
                error='!'
        else:
            if flag==1:    
                scale=abs((xlist[1]-xlist[0]))*10**-3
                time=np.arange(xlist[0],xlist[1],scale)
                y=np.array([])
                
                for i in range(len(time)):
                    if time[i]<0<time[i+1]:
                        time=np.insert(time,i+1,0)
                        time=np.delete(time,-1)
                    try: 
                        y_value=eval(f.replace('x','('+str(time[i])+')'))
                    except NameError:
                        error='!Undef. Var!'
                        y_value=np.nan
                    except:
                        y_value=np.nan
                    y=np.append(y,y_value)
                self.ax.plot(time,y,color)
        self.ax.set_ylim(ylist[0],ylist[1])
        self.ax.set_xlim(xlist[0],xlist[1])
        
        self.store_function(f_org,color,f_name,flag,error,f)
        
        self.canvas.draw()
    def update_graph(self):
        self.ax.cla()
        xlist=eval('['+str(self.xrange_input.text())+']')
        ylist=eval('['+str(self.yrange_input.text())+']')
        self.ax.axhline(linewidth=2, color="w")
        self.ax.axvline(linewidth=2, color="w")
        self.ax.grid()
        self.ax.set_ylim(ylist[0],ylist[1])
        self.ax.set_xlim(xlist[0],xlist[1])
        
        copy_list=list(self.function_storage)
        self.function_storage.clear()
        self.function_list.clear()
        for i in range(len(copy_list)):
            self.input_processing(copy_list[i][0],copy_list[i][3],copy_list[i][1])
        self.function_storage=list(copy_list)
            
        self.canvas.draw()
    
    '''Storage and History'''
    def store_function(self,f_org,color,f_name,flag,error,evaled_exp): 
        self.function_storage.append([f_org,color,f_name,flag,evaled_exp])
        widgitItem = qtw.QListWidgetItem() 
        widgetbtn_del=qtw.QPushButton('del',clicked=lambda:self.clear_single(widgitItem))
        widgetbtn_del.setGeometry(20,15,10,10)
        widgetbtn_del.setStyleSheet("border-radius : 5;border : 2px solid red;background-color: red; color:black")
        widgetbtn_show=qtw.QPushButton('#'+str(len(self.function_storage)),clicked=lambda:self.change_flag(widgitItem))
        widgetbtn_show.setGeometry(20,15,10,10)
        if flag == 0:
            widgetbtn_show.setStyleSheet("border-radius : 5;border : 2px solid "+color+";background-color:black;color:white")
        else: 
            widgetbtn_show.setStyleSheet("border-radius : 5;border : 2px solid "+color+";background-color:"+color+';color:black')
        widget = qtw.QWidget()
        if f_name=='y=':
            widgetText =  qtw.QLabel(f_name+f_org+' <span style="color:red;">'+error+'</span>')
        #elif f_name=='scatter:
            #widgetText =  qtw.QLabel(f_org+' <span style="color:red;">'+error+'</span>')
        else:
            widgetText =  qtw.QLabel(f_org+' <span style="color:red;">'+error+'</span>')
        widgetLayout = qtw.QHBoxLayout()
        widgetLayout.addWidget(widgetbtn_show,0)
        widgetLayout.addWidget(widgetText,2)
        widgetLayout.addWidget(widgetbtn_del,0)
        widget.setLayout(widgetLayout)
              
        self.function_list.addItem(widgitItem)
        widgitItem.setSizeHint(widget.sizeHint()) 
        self.function_list.setItemWidget(widgitItem, widget)
        
    '''Deleting/Clearing Functions'''
    def clear_single(self,ref):
        index=self.function_list.indexFromItem(ref).row()
        self.function_storage.remove(self.function_storage[index])
        self.update_graph()
        OppFunct.update_graph_memory()
    def clear_all(self):
        self.ax.cla()
        self.ax.plot()
        xlist=eval('['+str(self.xrange_input.text())+']')
        ylist=eval('['+str(self.yrange_input.text())+']')
        self.ax.set_ylim(ylist[0],ylist[1])
        self.ax.set_xlim(xlist[0],xlist[1])
        self.ax.axhline(linewidth=2, color="w")
        self.ax.axvline(linewidth=2, color="w")
        self.ax.grid()
        self.canvas.draw()
        self.function_list.clear()
        self.function_storage=[]
        OppFunct.update_graph_memory()
    
    '''Graph Brain'''
    def color_system(self,color):
        current_colors=[item[1] for item in self.function_storage]
        if color not in current_colors and color!='':
            return color
        for i in range(len(self.color_list)):
            if self.color_list[i] in current_colors:
                pass
            else:
                color=self.color_list[i]
                break
        return color
    def check_repeated_name(self,f_org,name,flg):
        list_of_names=[item[2] for item in self.function_storage]
        flag=0
        for i in range(len(list_of_names)):
            if name == list_of_names[i] and name!='y=':
                self.function_storage[i]=[f_org,self.function_storage[i][1],name,flg]
                flag=1
                break
        if flag==1:
            self.update_graph()
        return flag
    def change_flag(self,ref):
        index=self.function_list.indexFromItem(ref).row()
        if self.function_storage[index][3]==0:
            self.function_storage[index][3]=1
        else:
            self.function_storage[index][3]=0
        self.update_graph()
    def next_to_multiplication(self,f):
        f+=' '
        for i in range(f.count('x')): # next to muliplication for 'x'
            if f[f.find('x')-1] in ['1','2','3','4','5','6','7','8','9','0']:
                f_list=list(f)
                f_list.insert(f.find('x'),'*')
                f=''.join(f_list)
            if f[f.find('x')+1] in ['1','2','3','4','5','6','7','8','9','0']:
                f_list=list(f)
                f_list.insert(f.find('x')+1,'*')
                f=''.join(f_list)
            f_list=list(f)
            f_list[f.find('x')]='~'
            f=''.join(f_list)
        f=f.replace('~','x')
        f=f.replace(' ','')
        return f
    
    '''Graphing Opperations'''
    def intersection(self):
        funct_list=[]
        for i in range(len(self.function_storage)):
            funct_list.append(self.function_storage[i][4])
            
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
        
        x=[]
        y=[]
        for l in range(len(soln_list)):
            for s in soln_list[l]:
                if s != 'No Solution':
                    x.append(s)
                    y.append(eval(set_equals_list[l][:set_equals_list[l].find('=')].replace('x',str(s))))
        
        # plot  
        self.scatter=self.ax.scatter(
            x,
            y,
            c='r',
            marker='x',
            s=100
        )
        self.canvas.draw_idle()  
                    
        return 
    def zeros(self):
        funct_list=[]
        for i in range(len(self.function_storage)):
            if '[' not in self.function_storage[i][4]:
                funct_list.append(self.function_storage[i][4])
        x=[]
        y=[]
        
        for funct in funct_list:
            x_soln_str=solve(str(funct)+',x')
            try:
                x_soln_str_list=x_soln_str[x_soln_str.find('=')+1:]
                x_soln_str_list=x_soln_str_list.replace(',','","')
                x_soln_str_list=x_soln_str_list.replace('[','["')
                x_soln_str_list=x_soln_str_list.replace(']','"]')
                x_soln_list=eval(x_soln_str_list)
            except:
                pass
            
            for soln in x_soln_list:
                y_soln=eval(funct.replace('x','('+soln+')'))
                if soln=='':
                    pass
                else: 
                    x.append(eval(soln))
                    y.append(y_soln)
                
        # eliminate answers outside of range to not take up more computing power than needed
                
        self.scatter=self.ax.scatter(
            x,
            y,
            c='r',
            marker='x',
            s=100
        )
        self.canvas.draw_idle()
        return 
    def maxnmins(self):
        funct_list=[]
        for i in range(len(self.function_storage)):
            funct_list.append(self.function_storage[i][4])
        x=[]
        y=[]
        deriv_list=[diff(funct+',x') for funct in funct_list]
        
        for i in range(len(deriv_list)):
            x_soln_str=solve(str(deriv_list[i])+',x')
            x_soln_str_list=x_soln_str[x_soln_str.find('=')+1:]
            x_soln_str_list=x_soln_str_list.replace(',','","')
            x_soln_str_list=x_soln_str_list.replace('[','["')
            x_soln_str_list=x_soln_str_list.replace(']','"]')
            x_soln_list=eval(x_soln_str_list)
            
            for x_soln in x_soln_list:
                y_soln=eval(funct_list[i].replace('x','('+x_soln+')'))
                x.append(eval(x_soln))
                y.append(y_soln)
                
        # plot
        
        self.scatter=self.ax.scatter(
            x,
            y,
            c='r',
            marker='x',
            s=100
        )
        self.canvas.draw_idle()
        
        return 
    def smart_range(self):
        pass
    
    '''Mouse Position Function'''
    def motion_hover(self,event):
        annotation_visible=self.annotations.get_visible()
        print(annotation_visible)
        if event.inaxes== self.ax:
            is_contained,annotation_index=self.scatter.contains(event)
            if is_contained==True:
                data_point_location=self.scatter.get_offsets()[annotation_index['ind'][0]]
                print(data_point_location)
                
                self.annotations.xy=tuple(data_point_location)
                text_label='({0:.2f}, {1:.2f})'.format(data_point_location[0],data_point_location[1])
                self.annotations.set_text(text_label)
                self.annotations.set_visible(True)
                self.canvas.draw_idle()
            else:
                if annotation_visible==True:
                    self.annotations.set_visible(False)
                    self.canvas.draw_idle()
        
'''Options'''
class OptionsWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Options')
        self.setLayout(qtw.QVBoxLayout())
        self.degree_mode_tracker=0
        self.complex_mode_tracker=0
        self.keypad()
        self.hidden=True
         
    def open_window(self,window_btn):
        if self.hidden==True:
            window_btn.show()
            self.hidden=False
        else:
            window_btn.hide()
            self.hidden=True

    def keypad(self):
        container=qtw.QWidget()
        container.setLayout(qtw.QGridLayout())
        
        label_name=qtw.QLabel()
        label_name.setText('Options')
        btn_degree_mode=qtw.QPushButton('Degree Mode',clicked=lambda:self.change_degree_mode())
        self.label_degree_mode=qtw.QLabel()
        if self.degree_mode_tracker==0:
            self.label_degree_mode.setText('Degree')
        else:
            self.label_degree_mode.setText('Radian')
        
        btn_complex_mode=qtw.QPushButton('Cplx Mode',clicked=lambda:self.change_complex_mode())
        self.label_complex_mode=qtw.QLabel()
        if self.degree_mode_tracker==0:
            self.label_complex_mode.setText('Rect')
        else:
            self.label_complex_mode.setText('Polar')
        
        container.layout().addWidget(label_name,0,0)
        container.layout().addWidget(btn_degree_mode,1,0)
        container.layout().addWidget(self.label_degree_mode,1,1)
        container.layout().addWidget(btn_complex_mode,2,0)
        container.layout().addWidget(self.label_complex_mode,2,1)
        
        self.layout().addWidget(container)
    
    '''Degree mode'''
    def change_degree_mode(self):
        if self.degree_mode_tracker==0:
            self.degree_mode_tracker=1
            self.label_degree_mode.setText('Radian')
        else:
            self.degree_mode_tracker=0
            self.label_degree_mode.setText('Degree')
    def check_degree_mode(self,eval_string):
        if self.degree_mode_tracker==0:
            eval_string=eval_string.replace('sin','sind')
            eval_string=eval_string.replace('cos','cosd')
            eval_string=eval_string.replace('tan','tand')
            eval_string=eval_string.replace('sec','secd')
            eval_string=eval_string.replace('csc','cscd')
            eval_string=eval_string.replace('cot','cotd')             
        return eval_string

    '''Complex mode'''
    def change_complex_mode(self):
        if self.complex_mode_tracker==0:
            self.complex_mode_tracker=1
            self.label_complex_mode.setText('Polar')
        else:
            self.complex_mode_tracker=0
            self.label_complex_mode.setText('Rect')
    def check_complex_mode(self,string):
        try:  
            if type(eval(string))==complex and self.complex_mode_tracker==1:
                if self.degree_mode_tracker==0:
                    cplx_tup=cm.polar(eval(string))
                    if cplx_tup[0]==float(1):
                        string='e^('+str(degrees(cplx_tup[1]))+'j)'
                    else:    
                        string=str(cplx_tup[0])+'e^('+str(degrees(cplx_tup[1]))+'j)'
                else:
                    string=polar(eval(string))
                return string
            else:
                return string
        except:
            return string

'''Keeps a history of opperations'''
class HistoryWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('History')
        self.setLayout(qtw.QVBoxLayout())
        self.history_list=qtw.QListWidget()
        self.history_list.itemDoubleClicked.connect(self.btn_clicked)
        self.layout().addWidget(self.history_list)
        
    def add_to_history(self,left,right):
        left=left+'='
        history.append(left)
        history.append(right)
        
        self.history_list.addItem('')
        
        widgitItem = qtw.QListWidgetItem(left) 
        widgitItem.setForeground(QColor('orange'))   
        self.history_list.addItem(widgitItem)

        widgitItem = qtw.QListWidgetItem(right) 
        self.history_list.addItem(widgitItem)
        self.history_list.scrollToBottom()
        
        if len(history)>60:
            del history[0]
            del history[0]
    
    def btn_clicked(self,btn):
        btn_text=btn.text()
        if btn_text[-1]=='=':
            btn_text=btn_text[:-1]
        mw.result_field.setText(mw.result_field.text()+btn_text)
        
    def keypad(self):
        pass

'''Functions window that has the functions the calculator can use'''
class FunctWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Functions')
        self.setLayout(qtw.QVBoxLayout())
        self.container=qtw.QTabWidget()
        self.tabs()
        self.layout().addWidget(self.container)
        self.hidden=True
     
    def tabs(self):
        # general functions
        general_tab=qtw.QWidget()
        general_tab.setLayout(qtw.QGridLayout())
        
        funct_sum=qtw.QPushButton('Sum',clicked=lambda:OppFunct.call_function('Gf.sumation('))
        funct_quad=qtw.QPushButton('Quadratic',clicked=lambda:OppFunct.call_function('Gf.quad('))
        general_tab.layout().addWidget(funct_sum,0,0)
        general_tab.layout().addWidget(funct_quad,0,1)
        
        # calculus functions 
        calculus_tab=qtw.QWidget()
        calculus_tab.setLayout(qtw.QGridLayout())

        funct_D=qtw.QPushButton('Derivative(funct,var)',clicked=lambda:OppFunct.call_function('diff('))
        funct_I=qtw.QPushButton('Integral(funct,var)',clicked=lambda:OppFunct.call_function('intg('))
        funct_lim=qtw.QPushButton('Limit(funct,lim,var)',clicked=lambda:OppFunct.call_function('lim('))
        calculus_tab.layout().addWidget(funct_D,1,1)
        calculus_tab.layout().addWidget(funct_I,2,1)
        calculus_tab.layout().addWidget(funct_lim,3,1)
        
        # matrix functions
        matrix_tab=qtw.QWidget()
        matrix_tab.setLayout(qtw.QGridLayout())
        
        funct_Dprod=qtw.QPushButton('Dot Prod.',clicked=lambda:OppFunct.call_function('Mf.dprod('))
        funct_Cprod=qtw.QPushButton('Cross Prod.',clicked=lambda:OppFunct.call_function('Mf.dprod('))
        matrix_tab.layout().addWidget(funct_Dprod,1,2)
        matrix_tab.layout().addWidget(funct_Cprod,2,2)
        
        # uncertainties
        uncertainties_tab=qtw.QWidget()
        uncertainties_tab.setLayout(qtw.QGridLayout())
    
        # set widgets in tabs
        self.container.addTab(general_tab,'General')
        self.container.addTab(calculus_tab,'Calculus')
        self.container.addTab(matrix_tab,'Matrix')
        self.container.addTab(uncertainties_tab,'Error Prop')
        
    def open_window(self,window_btn):
        if self.hidden==True:
            window_btn.show()
            self.hidden=False
        else:
            window_btn.hide()
            self.hidden=True
     
'''Places all the windows into one full window'''
class FullWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('IcE')
        self.setLayout(qtw.QGridLayout())
        
        self.graph_container=qtw.QWidget()
        self.graph_container.setLayout(qtw.QVBoxLayout())
        self.graph_container.layout().addWidget(gw)
        
        self.maintab=qtw.QTabWidget()
        self.maintab.addTab(mw,'Calc')
        self.maintab.addTab(self.graph_container,'Graph')
        self.subtab=qtw.QTabWidget()
        
        self.container=qtw.QWidget()
        self.container.setLayout(qtw.QVBoxLayout())
        self.subcontainer=qtw.QWidget()
        self.subcontainer.setLayout(qtw.QVBoxLayout())
        
        self.container.layout().addWidget(vw)
        self.container.layout().addWidget(mfw)
        self.subcontainer.layout().addWidget(gw.functions_bloc)
        self.subcontainer.layout().addWidget(gw.function_list)
        self.subcontainer.layout().addWidget(gw.settings_bloc)
        self.subtab.addTab(self.container,'Vars/Funct')
        self.subtab.addTab(self.subcontainer,'Graphing')

        
        self.layout().addWidget(ow,0,0)
        self.layout().addWidget(self.maintab,0,1,3,2)
        self.layout().addWidget(self.subtab,0,3,1,1)
        self.layout().addWidget(fw,0,4,2,4)
        fw.hide()
        ow.hide()
        
        self.side_hidden=False
        
        self.show()
        
    def open_side_window(self,window_btn):
        if self.side_hidden==True:
            window_btn.show()
            self.side_hidden=False
        else:
            window_btn.hide()
            self.side_hidden=True

'''Defines a class of universal opperational functions for general use in the program'''
class OpperationalFunctions():
    def call_function(self,function):
        mw.fin_nums=[str(mw.result_field.text())]
        mw.fin_nums.append(function)
        mw.result_field.setText(''.join(mw.fin_nums))
        
    def update_memory(self): 
        thing=pd.DataFrame([user_functions]).transpose()
        thing.to_csv('/Users/elijahhall/Documents/Phython/Personal Projects/Calculator/Calc_Memory/user_defined.csv')
        
    def update_hist_memory(self):
        pandas_data_frame=pd.DataFrame([history]).transpose()
        pandas_data_frame.to_csv('/Users/elijahhall/Documents/Phython/Personal Projects/Calculator/Calc_Memory/history.csv')
        
    def update_graph_memory(self):
        pandas_data_frame=pd.DataFrame([gw.function_storage]).transpose()
        pandas_data_frame.to_csv('/Users/elijahhall/Documents/Phython/Personal Projects/Calculator/Calc_Memory/graphing.csv')
        
    def reinstate_memory(self):
        try:
            memory_data_structure=pd.read_csv('/Users/elijahhall/Documents/Phython/Personal Projects/Calculator/Calc_Memory/user_defined.csv',index_col=False)
            arr=memory_data_structure.to_numpy()
            for i in range(len(arr)):
                if str(arr[i,1]).find('[[')!=-1:
                    user_functions[str(arr[i,0])]=eval(arr[i,1])
                    user_funct.append([arr[i,0]+'{'+','.join(eval(arr[i,1])[0])+'}',eval(arr[i,1])])
                    mfw.functcontainer.addItem(arr[i,0]+'{'+','.join(eval(arr[i,1])[0])+'}='+eval(arr[i,1])[1])
                else:
                    user_functions[str(arr[i,0])]=arr[i,1]
                    user_vars.append([arr[i,0],arr[i,1]])
                    vw.varscontainer.addItem(str(arr[i,0])+'='+str(arr[i,1]))
        except:
            mw.result_field.setText('Issue Recalling User Functions')
        try:
            pandas_data_frame=pd.read_csv('/Users/elijahhall/Documents/Phython/Personal Projects/Calculator/Calc_Memory/history.csv',index_col=0)
            arr_hist=pandas_data_frame.to_numpy()

            for j in range(len(arr_hist)):
                history.append(arr_hist[j,0])
                if j % 2==0:
                    widgitItem = qtw.QListWidgetItem(arr_hist[j,0]) 
                    widgitItem.setForeground(QColor('orange'))
                    hw.history_list.addItem('')
                    hw.history_list.addItem(widgitItem)
                else:
                    widgitItem = qtw.QListWidgetItem(arr_hist[j,0]) 
                    hw.history_list.addItem(widgitItem)
            hw.history_list.scrollToBottom()
        except:
            mw.result_field.setText('Issue Recalling History')
        try:
            pandas_data_frame=pd.read_csv('/Users/elijahhall/Documents/Phython/Personal Projects/Calculator/Calc_Memory/graphing.csv', index_col=False)
            arr_graph=pandas_data_frame.to_numpy()
        
            for j in range(len(arr_graph)):
                gw.function_storage.append(eval(arr_graph[j,1]))
            gw.update_graph()
        except:
            gw.input_field.setText('Issue Recalling History')

'''excecutes the program'''
app = qtw.QApplication([])
OppFunct=OpperationalFunctions()
hw=HistoryWindow()
mfw=MyFunctionsWindow()
mw=MainWindow()
gw=GraphWindow()
ow=OptionsWindow()
vw=VarsWindow()
fw=FunctWindow()
Fw=FullWindow()
OppFunct.reinstate_memory()
app.setStyle(qtw.QStyleFactory.create('Fusion'))
app.exec()