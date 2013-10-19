import copy

def set_global_vars(num_vars):
	global all_vars, assigned_vars, assignments;
	all_vars = range(1,num_vars+1)
	assignments = {2:True}

def assign_var(var_index,val):
	assigned_vars.append(var_index)
	assignments[var_index] = val

def find_unit_clause(clauses, assignments):
	returndict = {}
	for clause in clauses:
		literals = clause.split(' ')[:-1]
		present_vars = [int(i) for i in literals if abs(int(i)) not in assignments.keys()]
		if len(present_vars) == 1:
			var = abs(int(present_vars[0]))
			val = present_vars[0]>0
			if var in returndict.keys():
				if returndict[var] != present_vars[0]>0:
					#Conflict hai boss!
					return -1,{}
			else:
				returndict[var] = val
				find_unit_clause(
				
	return 0,returndict
			assign_var(abs(present_vars[0]),(present_vars>0))

def dpll(all_clauses, assignments):
	propsat, unit_prop = find_unit_clause(all_clauses, assignments)
	print propsat
	if propsat>=0:
		print unit_prop
		for item in unit_prop:
			print unit_prop.key(item)
			assignments[unit_prop.keys()[0]] = unit_prop[unit_prop.keys()[0]]
	else:
		return -1
	





f = open('data.txt')

fLines = f.readlines()

l1 = fLines[0].split(' ')

num_vars = int(l1[2])
num_clauses = int(l1[3])

all_clauses = fLines[1:]

set_global_vars(num_vars)

dpll(all_clauses,assignments)


