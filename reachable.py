import numpy as np
import copy
'''
rows as input and columns as output. a[x][y]=1 iff x is input and y is output
tensor is the transition tensor
matrix is the reachability matrix
'''

def reachable(tensor, accepts):
	
	# 1. create reachability matrix by combing transition matrix per alphabet

	#matrix is reability matrix
	matrix = tensor[0]
	
	#created by combing all alphabet transitions
	if len(tensor)>1:
		for i in range(1,len(tensor)):
			matrix += tensor[i]

	# 2. TO DO: get transpose for final states

	# 3. get sets of terminals (the destination of transitions) for all states
	
	numState = len(matrix)

	workingMatrix = matrix
	
	terminalSet = [ copy.deepcopy( set([i]) ) for i in range(numState)]
	
	for i in range( numState ):

		workingMatrix[i] = [ j if matrix[i][j] == 1 else  0.1 for j in range( numState ) ]
		
		terminalSet[i] = set(workingMatrix[i])
		
		if 0.1 in workingMatrix[i]:
			terminalSet[i].remove(0.1)

	if len( list( terminalSet[0] + accepts ) ) < len( terminalSet[0] ) + len( accepts ) :
		
		return True
	
	while True:
		
def compare():
	

