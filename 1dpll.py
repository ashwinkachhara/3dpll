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

def empty_clause(clauses, assignments):
	for clause in clauses:
		print clause
		asgn_vars = [i for i in clause if abs(i) in assignments.keys()]
		if len(asgn_vars) == len(clause):
			clause_val = False
			for literal in clause:
				if (bool(assignments[abs(literal)]) == bool(literal>0)):
					clause_val = True
					break
			if not clause_val:
				print 'Empty'
				return False
	return True



f = open('data.txt')
fLines = f.readlines()
l1 = fLines[0].split(' ')

num_vars = int(l1[2])
num_clauses = int(l1[3])

all_clauses = []
for line in fLines[1:]:
	all_clauses.append([int(i) for i in line.split(' ')[:-1]])
print all_clauses

assignments = {}

#~ print check_consistent(all_clauses,assignments)
print empty_clause(all_clauses,assignments)
			
