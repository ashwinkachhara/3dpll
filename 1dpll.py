from copy import deepcopy
import sys

# Make this true for Debug Mode, which prints value on every step
DEBUG_Mode = False

def check_consistent(clauses, assignments):
	# Check the consistency of clauses based on current (possibly partial) assignment of variables
	for clause in clauses:
		asgn_vars = [i for i in clause if abs(i) in assignments.keys()]
		clause_result = False
		for var in asgn_vars:
			if (bool(assignments[abs(var)]) == bool(var>0)):
				clause_result = True
				#~ print "Here"
				break
		if not clause_result:
			# If any clause evaluates to False, we return False (i.e. the problem is UNSAT)
			return False
	return True

def empty_clause(clauses, assignments):
	# Returns False if empty clause is found
	# Empty clause: all the literals have been assigned in a way that makes the clause False
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

def find_unit_clauses(clauses):
	# The function is self explanatory. If length of a clause is one, we return
	unit_dict = {}
	for clause in clauses:
		if len(clause) == 1:
			unit_dict[clause[0]]=1
	unit_clauses=[]
	for unit in unit_dict:
		unit_clauses.append(unit)		
	return unit_clauses

def literal_propagate(old_clauses, assigned):# assigned is a length 1 dict -> var:value
	# This function propagates value of a literal into all other clauses. literal under propagation is specified in assignmed variable argument
	# This function is used to reduce clause w.r.t. to a given literal
	assigned_var = assigned.keys()[0]
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

# This is a TEST function written for Program Testing
#~ def unit_test(clauses, assignments):
	#~ clauses = literal_propagate(clauses,assignments)
	#~ # print clauses
	#~ unit_clauses = find_unit_clauses(clauses)
	#~ for unit_clause in unit_clauses:
		#~ assigned = {abs(unit_clause[0]): (unit_clause[0]>0)}
		#~ clauses = literal_propagate(clauses,assigned)
		#~ # print clauses
		
		
def find_pure_literals(clauses):# all_literal = -1 : Not a Pure Literal, 0 : Complemented Pure Literal, 1 : Pure Literal
	# Finds pure literal in clauses.
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
	
# This is a TEST function written for Program Testing
#~ def pure_literal_test(clauses):
	#~ pure_literals = find_pure_literals(clauses)
	#~ for pure_literal in pure_literals:
		#~ assigned = {abs(pure_literal): (pure_literal>0)}
		#~ clauses = literal_propagate(clauses,assigned)
		#~ print clauses
					
def dpll(old_clauses,old_assignments,recursion_depth):
	clauses = deepcopy(old_clauses)
	assignments = deepcopy(old_assignments)
	if (DEBUG_Mode):
		print "\n# Recursion Depth ", recursion_depth  # where i is recusion depth
		print "# Clauses",old_clauses
		print "# Assignments",old_assignments
	if(check_consistent(clauses, assignments)):
		print 'Done', assignments
		return True
	elif not empty_clause(clauses, assignments):
		if (DEBUG_Mode):
			print 'Empty Clause detected. Variable Assignments :',assignments
			print 'Backtracking sequence initiated. Backtracking in 3...2...1...'
		return False
	unit_clauses = find_unit_clauses(clauses)
	if (DEBUG_Mode):
		print 'Unit Clauses : ',unit_clauses
	
	for unit_clause in unit_clauses:
		
		asgn_var = abs(unit_clause)
		asgn_val = unit_clause>0
		assigned = {asgn_var: asgn_val}
		if(asgn_var in assignments.keys()):
			if(assignments[asgn_var] != asgn_val):
				if (DEBUG_Mode):
					print 'Conflicting Unit Clause has been Detected. Two unit clauses are contradictory:' 
					print 'Backtracking sequence initiated. Backtracking in 3...2...1...'
				return False
		else:
			assignments[asgn_var] = asgn_val
		clauses = literal_propagate(clauses,assigned)
		#~ for clause in clauses:
			#~ if not clause: # Check for an Empty Clause, as Empty Clause will imply that No literals of the clause were able to make clause Satisfiable\True
				#~ print 'Empty Clause, Unsat'
				#~ return False
	if (DEBUG_Mode):
		print "Unit Propagation complete. Reduced clauses: ", clauses
	pure_literals = find_pure_literals(clauses)
	for pure_literal in pure_literals:
		assigned = {abs(pure_literal): (pure_literal>0)}
		assignments[abs(pure_literal)] = (pure_literal>0)
		clauses = literal_propagate(clauses,assigned)
	if (DEBUG_Mode):
		print "Pure Literals found:", pure_literals
		print "Pure Literal elimination complete. Reduced clauses: ", clauses
	#Choose New Literal
	if(clauses == []):
		print "\n\n************ SAT: ",assignments
		return True
	elif(clauses[0] == []):
		return False
	else:
		I= clauses[0][0];
		if DEBUG_Mode:
			print 'Choosing new literal: ',I
	#~ print (clauses+[[I]])
	if(dpll(clauses+[[I]],assignments,recursion_depth+1)):
		return True
	elif(dpll(clauses+[[-I]],assignments,recursion_depth+1)):
		return True
	else:
		return False
	
def main(argv=None):
	if argv is None: argv = sys.argv
	if len(argv) != 2:
		print "Usage: %s <cnf_file>" % argv[0]
		return 1
	try:
  		filename = argv[1]
		# Read the clauses in DIMACS conjunctive normal form from a cnf file
		f = open(filename)
		fLines = f.readlines()
		l1 = fLines[0].split(' ')

		num_vars = int(l1[2])
		num_clauses = int(l1[3])

		all_clauses = []
		for line in fLines[1:]:
			all_clauses.append([int(i) for i in line.split(' ')[:-1]])
		#~ print all_clauses

		# Compute a solution for the SAT problem using our SAT solver
		if not dpll(all_clauses,{},0):
			print '\n\n************ UNSAT: The given clauses are not satisfiable by any variable assignment'
	except IOError: # try as formula
		print "Could not find file '%s'!!" % argv[1]
	return 0	


if __name__ == '__main__':
	sys.exit(main())
