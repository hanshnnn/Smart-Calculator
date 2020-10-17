symbols = ['(', ')', '+', '-', '/', '*']


def remove_spaces(equation):  # removes unnecessary spaces, check whether is assignment
    equation = equation.replace(' ', '')
    if len(equation) == 1 or equation.isalpha():
        return [equation], 'no'
    elif '=' not in equation:
        x = []
        symbol_index = [i for i, ltr in enumerate(equation) if ltr in symbols]
        for i in range(len(symbol_index)):
            if i == 0 and symbol_index[i] != 0:
                x.append(equation[:symbol_index[i]])
            temp = equation[symbol_index[i-1]+1:symbol_index[i]]
            if temp != '':
                x.append(temp)
            x.append(equation[symbol_index[i]])
        if symbol_index[-1] != len(equation) - 1:  # if there's still number left
            x.append(equation[symbol_index[-1] + 1:])
        return x, 'no'
    elif '=' in equation:
        equation = equation.replace(' ', '')
        equation = equation.split('=')
        return equation, 'yes'


def deal_variables(_equation):  # this func deals with keys and removes '+''-'
    global variables
    equation = []
    temp = []
    bracket_checker = 0
    num_of_digit = 0
    for index, content in enumerate(_equation):
        if content in variables:
            _equation[index] = variables[content]
            num_of_digit += 1
        elif content.isdigit():
            num_of_digit += 1
            _equation[index] = int(content)
        if _equation[index] != '+' and _equation[index] != '-':
            if temp:
                if temp.count('-') % 2 == 0:
                    equation.append('+')
                else:
                    equation.append('-')
            equation.append(_equation[index])
            temp = []   # clear
        elif _equation[index] == '+' or _equation[index] == '-':
            temp.append(_equation[index])
        if _equation[index] == '(':
            bracket_checker += 1
        elif _equation[index] == ')':
            bracket_checker -= 1
    # below deals if there's sign infront of the equation
    if equation[0] == '+':
        equation.remove('+')
    elif equation[0] == '-':
        equation[1] *= -1
        equation.remove('-')
    # check if the parenthesis is in correct form
    if bracket_checker != 0:
        return False
    if equation.count('+') + equation.count('-') + equation.count('*') + equation.count('/') != num_of_digit - 1:
        return False
    return equation


def assignments(equations):
    global variables
    if len(equations) != 2:
        return 'Invalid assignment'
    elif not equations[0].isalpha():  # before '='
        return 'Invalid identifier'
    elif equations[1] in variables:
        variables[equations[0]] = variables[equations[1]]  # if variable is predefined
    else:
        try:
            int(equations[1])
        except ValueError:
            if not equations[1].isalpha():  # after '='
                return 'Invalid assignment'
            return 'Unknown variable'
        else:
            variables[equations[0]] = int(equations[1])  # if variable is not predefined


def inf_to_postf(a_list):  # convert an infix_list to postfix_list
    postfix = []
    stack = []
    priority = {'+': 1, '-': 1, '/': 2, '*': 2, '(': 0, ')': 0}
    for i in a_list:
        if isinstance(i, int):
            postfix.append(i)
        else:
            if not stack:
                stack.append(i)
                continue
            elif i == '(':
                stack.append(i)
            elif i == ')':
                while stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
                continue
            else:
                while not stack or priority[i] <= priority[stack[-1]]:
                    if not stack:
                        break
                    postfix.append(stack.pop())
                stack.append(i)
    while stack:
        postfix.append(stack.pop())
    return postfix


def postf_to_answer(postfix):
    stack = []
    for i, content in enumerate(postfix):
        if content not in symbols:
            stack.append(content)
        else:
            back = stack.pop()
            front = stack.pop()
            if content == '+':
                stack.append(front + back)
            elif content == '-':
                stack.append(front - back)
            elif content == '/':
                stack.append(int(front / back))
            elif content == '*':
                stack.append(int(front) * back)
    return stack[0]


variables = {}
while True:
    x = input()
    if x.startswith('/') and x != '/exit' and x != 'help':
        print('Unknown command')
    elif x == '/exit':
        break
    elif x == '/help':
        print('The program calculates the sum of numbers')
    elif x == '':
        continue
    else:
        x, equal = remove_spaces(x)
        if equal == 'yes':
            if assignments(x) is None:
                pass
            else:
                print(assignments(x))
                continue
        elif len(x) == 1 and not ('+' in x[0] or '-' in x[0]):
            try:
                int(x[0])
            except ValueError:
                if x[0] in variables:
                    print(variables[x[0]])
                else:
                    if x[0] not in variables:
                        print('Unknown variable')
                    else:
                        print('Invalid identifier')
            else:
                print(int(x[0]))
        else:
            x = deal_variables(x)
            if not x:
                print('Invalid expression')
            else:
                x = inf_to_postf(x)
                print(postf_to_answer(x))
print('Bye!')
