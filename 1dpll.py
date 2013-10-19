from copy import deepcopy

def check_consistent(clauses, assignments):
	for clause in clauses:
		asgn_vars = [i for i in clause if abs(i) in assignments.keys()]
		clause_result = False
		for var in asgn_vars:
			if (bool(assignments[abs(var)]) == bool(var>0)):
				clause_result = True
				#~ print "Here"
				break
		if not clause_result:
			return False
	return True

def empty_clause(clauses, assignments):# Returns False if empty clause is found
	for clause in clauses:
		asgn_vars = [i for i in clause if abs(i) in assignments.keys()]
		if len(asgn_vars) == len(clause):
			clause_val = False
			for literal in clause:
				if (bool(assignments[abs(literal)]) == bool(literal>0)):
					clause_val = True
					break
			if not clause_val:
				#~ print 'Empty'
				return False
	return True

#~ def find_unit_clauses(clauses):
	#~ unit_clauses = []
	#~ for clause in clauses:
		#~ if len(clause) == 1:
			#~ unit_clauses.append(clause)
	#~ return unit_clauses

def find_unit_clauses(clauses):
	unit_dict = {}
	for clause in clauses:
		if len(clause) == 1:
			unit_dict[clause[0]]=1
	unit_clauses=[]
	for unit in unit_dict:
		unit_clauses.append(unit)		
	return unit_clauses

def unit_propagate(old_clauses, assigned):# assigned is a length 1 dict -> var:value
	assigned_var = assigned.keys()[0]
	#~ need_to_reduce = [clause for clause in clauses if (assigned_var in clause) or (-assigned_var in clause)]
	reduced_clauses = []
	clauses = deepcopy(old_clauses)
	for clause in clauses:
		#~ print clause
		if (assigned_var not in clause) and (-assigned_var not in clause):
			reduced_clauses.append(clause)
			continue
		for literal in clause:
			#~ print abs(literal), assigned_var
			if abs(literal) == assigned_var:
				if (bool(assigned[assigned_var]) == bool(literal>0)):
					break
				else:
					clause.remove(literal)
					#~ print 'Reduced',clause
					reduced_clauses.append(clause)
					break
	return reduced_clauses

def unit_test(clauses, assignments):
	clauses = unit_propagate(clauses,assignments)
	print clauses
	unit_clauses = find_unit_clauses(clauses)
	for unit_clause in unit_clauses:
		assigned = {abs(unit_clause[0]): (unit_clause[0]>0)}
		clauses = unit_propagate(clauses,assigned)
		print clauses
		
		
def find_pure_literals(clauses):# all_literal = -1 : Not a Pure Literal, 0 : Complemented Pure Literal, 1 : Pure Literal
	all_literal ={};
	for clause in clauses:
		for literal in clause:
			if(abs(literal) in all_literal.keys()):
				if (bool(all_literal[abs(literal)]>0) != bool(literal > 0)):
					all_literal[abs(literal)] = 0;
			else:
				if(literal >0):
					all_literal[abs(literal)] = 1;
				else:
					all_literal[abs(literal)] = -1;
	pure_literals = []
	for key in all_literal:
		if all_literal[key] != 0:
			pure_literals.append(all_literal[key]*key)
	return pure_literals;
	
def pure_literal_test(clauses):
	pure_literals = find_pure_literals(clauses)
	for pure_literal in pure_literals:
		assigned = {abs(pure_literal): (pure_literal>0)}
		clauses = unit_propagate(clauses,assigned)
		print clauses
					
def dpll(clauses,assignments):
	if(check_consistent(clauses, assignments)):
		print 'Done', assignments
		return True
	elif not empty_clause(clauses, assignments):
		print 'Empty Clause'
		return False
	unit_clauses = find_unit_clauses(clauses)
	print 'Unit-clauses : ',unit_clauses
	
	for unit_clause in unit_clauses:
		#~ print 'unit-clauses',unit_clauses
		#~ print 'unit-clause',unit_clause
		asgn_var = abs(unit_clause)
		asgn_val = unit_clause>0
		assigned = {asgn_var: asgn_val}
		if(asgn_var in assignments.keys()):
			if(assignments[asgn_var] != asgn_val):
				print 'UNSAT, Conflicting Unit Clauses'
				return False
		else:
			assignments[asgn_var] = asgn_val
		clauses = unit_propagate(clauses,assigned)
		#~ for clause in clauses:
			#~ if not clause: # Check for an Empty Clause, as Empty Clause will imply that No literals of the clause were able to make clause Satisfiable\True
				#~ print 'Empty Clause, Unsat'
				#~ return False
	print "Unit Propogated : ", clauses
	pure_literals = find_pure_literals(clauses)
	for pure_literal in pure_literals:
		assigned = {abs(pure_literal): (pure_literal>0)}
		assignments[abs(pure_literal)] = (pure_literal>0)
		clauses = unit_propagate(clauses,assigned)
	print "Pure Literal Propogated : ", clauses
	

f = open('data.txt')
fLines = f.readlines()
l1 = fLines[0].split(' ')

num_vars = int(l1[2])
num_clauses = int(l1[3])

all_clauses = []
for line in fLines[1:]:
	all_clauses.append([int(i) for i in line.split(' ')[:-1]])
print all_clauses

assignments = {2:True}

#~ print check_consistent(all_clauses,assignments)
#~ print empty_clause(all_clauses,assignments)
#~ unit_clauses = find_unit_clauses(all_clauses)
#~ if len(unit_clauses) == 0:
	#~ print 'No Unit Clauses'
#~ else:
	#~ print 'Unit Clause(s)', unit_clauses

#~ unit_propagate(all_clauses,assignments)
#~ unit_test(all_clauses, assignments)
#~ find_pure_literals(all_clauses);
#~ pure_literal_test(all_clauses)
dpll(all_clauses,{})
