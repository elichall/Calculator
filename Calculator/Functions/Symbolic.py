import sympy as smp
    
class mystr(str):
    def plug(self,values_dict_str=str):
        values_dict_str=values_dict_str.replace(' ','')
        values_dict_str=values_dict_str.replace(':','":"')
        values_dict_str=values_dict_str.replace(',','","')
        values_dict=eval('{"'+values_dict_str+'"}')
        
        keys=list(values_dict.keys())
        values_list=[[key,values_dict[key]] for key in keys]
        
        equals=self.split('=')[0]
        expr_list_str=self.split('=')[1]
        expr_list_str=expr_list_str.replace('[','["')
        expr_list_str=expr_list_str.replace(']','"]')
        expr_list_str=expr_list_str.replace(',','","')
        expr_list=eval(expr_list_str)
        
        for j in range(len(expr_list)):
            for i in range(len(values_list)):
                expr_list[j]=expr_list[j].replace(values_list[i][0],values_list[i][1])
            try:
                expr_list[j]=str(eval(expr_list[j]))
            except:
                expr_list[j]=expr_list[j].replace(' ','')
                expr_list[j]=sympify_string(expr_list[j],'x')[0]
        return equals+'='+str(expr_list)
    
def replace_string_element(str,index,value):
    str_list=list(str)
    str_list[index]=value
    return ''.join(str_list)
    
def diff(fin_string_slice):
    
    # expression var of diff
    if fin_string_slice[-2:]!=',x': # if var is missing
        fin_string_slice+=',x'
    fin_string_slice=fin_string_slice.replace(',','","') # interpreting the input string
    fin_string_slice='["'+fin_string_slice+'"]'
    string=eval(fin_string_slice)[0]
    var=eval(fin_string_slice)[1]
    
    string=into_sympy_notation(string)
    final_expression,var,list_of_vars=sympify_string(string,var)
    diff_expression=str(final_expression.diff(var)) 
    return diff_expression
def intg(fin_string_slice):
    # expression, var of intg
    if fin_string_slice[-2:]!=',x': # if user did not specify var of integration
        fin_string_slice+=',x'
    fin_string_slice=fin_string_slice.replace(',','","') # interpreting the input string
    fin_string_slice='["'+fin_string_slice+'"]'
    string=eval(fin_string_slice)[0]
    var=eval(fin_string_slice)[1]
    
    string=into_sympy_notation(string)
    final_expression,var,list_of_vars=sympify_string(string,var)
    integrated_expression=str(final_expression.integrate(var)) 
    return integrated_expression
def lim(fin_string_slice):
    # input: string,var,var_0
    fin_string_slice=fin_string_slice.replace(',','","') # interpreting the input string
    fin_string_slice='["'+fin_string_slice+'"]'
    string=eval(fin_string_slice)[0]
    var=eval(fin_string_slice)[1]
    var0=eval(fin_string_slice)[2]
    
    string=into_sympy_notation(string)
    final_expression,var,list_of_vars=sympify_string(string,var)
    integrated_expression=str(smp.limit(final_expression,var,var0)) 
    return integrated_expression
def solve(fin_string_slice):
    fin_string_slice=fin_string_slice.replace(',','","') # interpret string
    fin_string_slice=fin_string_slice.replace('"[','["')
    fin_string_slice=fin_string_slice.replace(']"','"]')
    fin_string_slice='["'+fin_string_slice+'"]'
    expression_s=eval(fin_string_slice)[0]
    var=eval(fin_string_slice)[1]
    
    og_var=str(var)
    
    if '=' not in expression_s:
        expression_s='0='+expression_s
    zeroed_expression=solve_zero(expression_s)
            
    if '(' in var:
        var=smp.Function(og_var[:og_var.find('(')])
        og_args=og_var[og_var.find('(')+1:og_var.find(')')].split(',')
        args=[]
        for i in range(len(og_args)):
            args.append('smp.symbols("'+og_args[i]+'")')
        final_args='('+','.join(args)+')'
        zeroed_expression=zeroed_expression.replace(og_var[:og_var.find('(')],'~')
        zeroed_expression=zeroed_expression.replace(og_var[og_var.find('('):og_var.find(')')+1],'')
        diff_flag=1
    else:
        diff_flag=0
            
    final_expression,var,list_of_vars=sympify_string(zeroed_expression,var)
    if diff_flag==1:
        final_expression=str(final_expression).replace('’',"'")+' '
        while "'" in final_expression:
            diff_flag=1
            index=[final_expression.find("'"),1]
            k=1
            while final_expression[index[0]+k]=="'":
                index[1]=index[1]+1   
                k+=1
            final_expression=final_expression.replace("'"*index[1],final_args+'.diff(smp.symbols("x"),'+str(index[1])+')')
        final_expression=final_expression.replace('~','var')
        print(final_expression)
        final_expression=smp.sympify(eval(final_expression))             
    
    print(final_expression)
    if diff_flag==0:
        solved_expression=smp.solve(final_expression,var)
    else:
        solved_expression=smp.dsolve(final_expression,var)
        print(solved_expression)
    if solved_expression=='':
        return 'No Solution'
    solved_expression=[smp.simplify(ans) for ans in solved_expression]
    solved_expression=sympy_to_calc_notation(str(solved_expression))
    result_string=og_var+'='+solved_expression
    return mystr(result_string)
def solve_sys(fin_string_slice):
    # expression_s,unknowns,solving_for
    finalized_solutions={}
    fin_string_slice=fin_string_slice.replace(',','","') # interpret string
    fin_string_slice='["'+fin_string_slice+'"]'
    fin_string_slice=fin_string_slice.replace('"[','["')
    fin_string_slice=fin_string_slice.replace(']"','"]')
    expression_s=eval(fin_string_slice)[0]
    vars=eval(fin_string_slice)[1]
    vars=[var.replace(' ','') for var in vars]
    if len(eval(fin_string_slice))==3:
        solving_for=eval(fin_string_slice)[2]
    else:
        solving_for=list(vars)
    if type(solving_for)==list:
        wanted_solns=[item.replace(' ','') for item in solving_for]
        solving_for=solving_for[0]
    else:
        wanted_solns=[solving_for]
    
    if len(vars)>len(expression_s): # check solvablility
        return 'Unsolvable:MoreVarsThanEquations'
    
    for i in range(len(expression_s)): # zeros all the expressions entered
        if '=' not in expression_s[i]:
            expression_s[i]='0='+expression_s[i]
    zeroed_list=[solve_zero(item) for item in expression_s]
    
    
    contraint_equations=[expr for expr in zeroed_list if solving_for not in expr] # reorders the expression list to have expressions without the desired variable be on top
    left_over=[expr for expr in zeroed_list if solving_for in expr]
    zeroed_list=contraint_equations+left_over
    
    yet_to_be_solved=[item for item in vars if item not in solving_for]
    
    solved_for_expressions=[]
    expression_s_copy=list(zeroed_list)
    for v in yet_to_be_solved:
        for expr in expression_s_copy:
            if v in expr:
                final_expression,v,list_of_vars=sympify_string(expr,v)
                solved_expression=smp.solve(final_expression,v)
                solved_for_expressions.append([v,solved_expression[0]])
                expression_s_copy.remove(expr)
                break
    
    for item in expression_s_copy:
        if str(solving_for) in item:
            finished_str=item
            for expr in solved_for_expressions:
                finished_str=item.replace(str(expr[0]),'('+str(expr[1])+')')
                item=item.replace(str(expr[0]),'('+str(expr[1])+')')
            break
    
    finished_str=finished_str.replace(' ','')
    final_expression,solving_for,list_of_vars=sympify_string(finished_str,solving_for)
    solved_expression=smp.solve(final_expression,solving_for)
    
    finalized_solutions[str(solving_for)]=solved_expression

    # recursivly solve for all variables
    k=len(vars)
    while len(finalized_solutions)<k:
        vars.remove(str(solving_for))
        unsolved_vars=list(vars)
        ans_list=[[] for i in range(len(unsolved_vars))]
        for i in range(len(finalized_solutions[str(solving_for)])):
            combined_list=[str(pair[0])+'='+str(pair[1]) for pair in solved_for_expressions]
            substituted_list=[expr.replace(str(solving_for),'('+str(finalized_solutions[str(solving_for)][i])+')').replace(' ','') for expr in combined_list]
            solved_for_expressions=[expr.split('=') for expr in substituted_list]
            input_str=str(substituted_list).replace("'",'')+','+str(unsolved_vars).replace("'",'')+','+str(unsolved_vars).replace("'",'')
            ans=solve_sys(input_str).split(' ')[:-1]
    
            for i in range(len(ans)):
                temp=eval(ans[i][ans[i].find('=')+1:])
                if len(temp)==1:
                    temp=temp[0]
                ans_list[i].append(temp)
        
        solving_for=unsolved_vars[0] 
        for i in range(len(unsolved_vars)): 
            finalized_solutions[unsolved_vars[i]]=ans_list[i]
        
    # plug back into the original list of equations to test solvability
    keys=list(finalized_solutions.keys())
    plugged_equations=[]
    for eq in expression_s:
        substituted_eq_list=[eq]*len(finalized_solutions[keys[0]])
        for i in range(len(finalized_solutions)):
            for j in range(len(substituted_eq_list)):
                substituted_eq_list[j]=substituted_eq_list[j].replace(keys[i],'('+str(finalized_solutions[keys[i]][j])+')')
        plugged_equations.append(substituted_eq_list)
    
    # Checking solvability  
    for eq_list in plugged_equations:
        for eq in eq_list:
            pair=eq.split('=')
            if eval(pair[0])!=eval(pair[1]):
                return 'No Solutions'
    if len(solved_expression)==0:
        return 'No Solutions'
    
    result_str=''
    for v in wanted_solns:
        result_str+=str(v)+'='+sympy_to_calc_notation(str(finalized_solutions[v]))+' '
    
    return mystr(result_str)

def solve_zero(expression_s):
    print(expression_s)
    left=expression_s.split('=')[0]
    right=expression_s.split('=')[1]
    
    k=-1
    temp_list=[]
    temp_string=''
    left=' '+left
    while k>-len(left)-1:
        if left[k] in ['+','-',' ']:
            if left[k]==' ':
                temp_string+='+'
            else:
                temp_string+=left[k]
            temp_list.append(temp_string[::-1])
            temp_string=''
            k=k-1
        elif left[k]==')':
            temp_string+=left[k]
            k-=1
            parent_count=1
            while parent_count>0:
                if left[k]==')':
                    parent_count+=1
                    temp_string+=left[k]
                elif left[k]=='(':
                    parent_count-=1
                    temp_string+=left[k]
                else:
                    temp_string+=left[k]
                k-=1
        else:
            temp_string+=left[k]
            k=k-1
    
    for i in range(len(temp_list)):
        if temp_list[i][0]=='+':
            if temp_list[i][1:]!='':
                right+='-'+temp_list[i][1:]
        else:
            right+='+'+temp_list[i][1:]
    return right
def sympify_string(string,var):
    list_of_sympy_functions=['e','sin','cos','tan','asin','acos','atan','sec','csc','cot','asec','acsc','acot','ln','log','sqrt','LambertW']
    var_string=str(var)
    expression_list=[]
    list_of_vars=[]
    
    k=0
    temp_string=''
    while k<len(string):
        if string[k] in ['1','2','3','4','5','6','7','8','9','0','(','*','+','-','/',')',',','.']:
            expression_list.append(string[k])
            k+=1
        else:
            counter=0
            temp_string=''
            temp_string+=string[k]
            while counter==0:
                k+=1
                try:
                    if string[k] in ['1','2','3','4','5','6','7','8','9','0','(','*','+','-','/',')',',','.']:
                        counter=1
                    else:  
                        temp_string+=string[k]
                except:
                    counter=1
                
            if temp_string==var_string:
                if '(' not in var_string:
                    var=smp.symbols(var_string, real=True)
                expression_list.append('var')
            elif temp_string in list_of_sympy_functions:
                for i in range(len(list_of_sympy_functions)):
                    if temp_string=='e':
                        temp_string='smp.exp'
                        k+=2
                        break
                    elif temp_string==list_of_sympy_functions[i]:
                        temp_string='smp.'+list_of_sympy_functions[i]
                        break
                expression_list.append(str(temp_string))
            #elif temp_string in list(user_functions.keys()):
                #temp_string='smp.symbols("'+temp_string+'")'
                #expression_list.append(str(temp_string)) 
                #list_of_vars.append(temp_string)
            else:
                temp_string='smp.symbols("'+temp_string+'")'
                expression_list.append(str(temp_string))
                list_of_vars.append(temp_string)
    list_of_vars.append(var)
    print(''.join(expression_list))
    if '~' in expression_list:
        return ''.join(expression_list),var,list_of_vars
    else:
        final_expression=smp.simplify(eval(''.join(expression_list)))
    return final_expression,var,list_of_vars
def into_sympy_notation(expression):
    expression=expression.replace('^','**')
    expression=expression.replace(' ','')
    expression=expression.replace('sind','sin')
    expression=expression.replace('cosd','cos')
    expression=expression.replace('tand','tan')
    expression=expression.replace('secd','sec')
    expression=expression.replace('cscd','csc')
    expression=expression.replace('cotd','cot')
    return expression
def sympy_to_calc_notation(expression):
        expression=expression.replace('**','^')
        expression=expression.replace('log','ln')
        return expression

