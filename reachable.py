import numpy
import copy
'''
All functions here take the full TensorGenerator object.
rows as input and columns as output. a[x][y]=1 iff x is input and y is output
tensor is the transition tensor
matrix is the reachability matrix
'''

def getReached(tensorfull):
	tensor = tensorfull.tensor
	# 1. create reachability matrix by combing transition matrix per alphabet

	#matrix is reability matrix
	matrix = tensor[0].copy()
	
	#created by combing all alphabet transitions
	if len(tensor)>1:
		for i in range(1,len(tensor)):
			matrix = numpy.add(matrix, tensor[i])

	# 2. TO DO: get transpose for final states

	# 3. get sets of terminals (the destination of transitions) for all states
	
	numState = len(matrix)

	workingMatrix = matrix
	
	terminalSet = [ copy.deepcopy( set([i]) ) for i in range(numState)]
	reached = set()
	reached.clear()
	reached.add(0)
	toAnalyze = set()
	toAnalyze.clear()
	toAnalyze.add(0)
	nextAnalysis = set()
	nextAnalysis.clear()
	while len(toAnalyze) > 0:
		for state in toAnalyze:
			row = matrix[state]
			for i in range(len(row)):
				if row[i] > 0:
					if not reached.__contains__(i):
						reached.add(i)
						nextAnalysis.add(i)
		toAnalyze.clear()
		toAnalyze = nextAnalysis.copy()
		nextAnalysis.clear()

	'''
	for i in range( numState ):

		workingMatrix[i] = [ j if matrix[i][j] >= 1 else  0.1 for j in range( numState ) ]
		
		terminalSet[i] = set(workingMatrix[i])
		
		if 0.1 in workingMatrix[i]:
			terminalSet[i].remove(0.1)

	if len( list( terminalSet[0] + accepts ) ) < len( terminalSet[0] ) + len( accepts ) :
		
		return True
	'''
	return reached#, len(reached.intersection(accepts)) > 0

def getAccepted(tensor):
	reached = getReached(tensor)
	return reached.intersection(tensor.accept)

def reachesAccepted(tensor):
	reached = getReached(tensor)
	return len(reached.intersection(tensor.accept)) > 0

def reachesAll(tensor):
	accepts = {i for i in range(tensor.state)}
	reached = getReached(tensor)
	return len(reached.intersection(accepts)) == len(accepts)
#def compare():
