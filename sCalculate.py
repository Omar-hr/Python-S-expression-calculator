import sys

#Simple S-Exceptions parser. slightly modified from https://en.wikipedia.org/wiki/S-expression
def parse_sexp(string):
    sexp = [[]]
    word = ''
    for char in string:
        if char is '(':
            sexp.append([])
        elif char is ')':
            if word:
                sexp[-1].append(word)
                word = ''
            temp = sexp.pop()
            sexp[-1].append(temp)
        elif char in (' ', '\n', '\t'):
            if word:
                sexp[-1].append(word)
                word = ''
        else:
            word += char
    return sexp[0]

#Calculation funtion, takes an operation and two numbers as input, calculates and returns the result
def calculate(op,n1,n2):
	result = 0
	global error
	#check if the arguments are numbers. If not, return an error
	try:
		n1 = int(n1)
		n2 = int(n2)
	except ValueError:
		error = True
	if (isinstance(n1, int) and isinstance(n2, int)):
		error = False
	#check which operation to perform 
	if op == "add":
		result = n1 + n2
	elif op == "multiply":
		result = n1 * n2
	#if the operation is invalide, return an error
	else:
		error = True
	
	return result
	
#Function for exploring the expression and looping through all the node
def xploresubexp(ls):
	#temp list to evaluate the expressions
	current = []
	global result
	global parsed
	#loop through the input string
	for i, element in enumerate(ls):
		#if a sublist is found, explort the sublist
		if isinstance(element,list):
			xploresubexp(element)
			#after exploring all the sublists, store the result of each successful calculation and re explore
			ls[i] = result
			xploresubexp(ls)
		
		#when inside a sublist, get the elements of each operation, and calculate the result	
		else:
			current.append(element)
			#when a valid expression is found (eg. add 2 3), calculate
			if (len(current) == 3):
				result = calculate(current[0], current[1], current[2])
				current = []
	
	return result

#bool that decides if something went wrong throughout the execusion	
error = True

#if the command line argument is a single number, print
if str.isdigit(sys.argv[1]):
	if (len(sys.argv) < 3):
		error = False
		print(sys.argv[1])
#otherwise, parse the expression and evaluate
else:
	#result holds the output of the execution 
	result = 0
	parsed = parse_sexp(sys.argv[1])
	result = xploresubexp(parsed)
	#if no errors were found, print the result
	if (error == False):
		print (result)

if (error == True):
	print ("Please enter a valid arguemnt... \nAccepted arguments are integers or \"(Function Expression Expression)\"\nAccepted functions are add and multiply\nExpressions can be an integer or another function call") 
