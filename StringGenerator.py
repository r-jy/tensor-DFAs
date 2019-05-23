import numpy
import copy
import random
from Graph import Graph
class StringGenerator:
	depth = 0 # not used
	length = 0 # not used
	tensor = []
	accept=set()
	state = 0
	symbol = 0
	transition=set()

	def __init__(self,tensor_input,state_input,accept_input,symbol_input):
		self.tensor = tensor_input # make sure to input actual tensor
		self.accept = accept_input # make sure to input actual accepting states for tensor
		self.symbol = symbol_input # make sure to input actual alphabet size for tensor
		self.state = state_input # make sure to input actual number of states for tensor

		# content = ["empty",[]]
		# row = [ copy.deepcopy(content) for i in range(self.state)]
		# self.path = [copy.deepcopy(row) for i in range(self.state)]

	def convert(self):
		'''Converts tensor graph to representation as a set of (state, next state, transition symbol) 3-tuples'''
		for i in range(self.symbol): # iterate through length of alphabet
			for j in range(self.state): # iterate through number of states
				for k in range(self.state): # iterate through number of states
					if self.tensor[i][j][k] == 1:
						self.transition.add((j, k, i)) #--> (input/current state, next state, symbol))
		return self.transition

	def export(self):
		g = Graph(self.state*self.symbol,self.symbol) # Graph(number of states * size of alphabet vertices, size of alphabet names of vertices)
		for i in self.transition: # iterate through all transitions
			# We are assigning reference numbers to the start and end states
			#   Start state is (start state # * transition #)
			#   End state is   (end   state # * transition #) + transition #
			start = i[0]*self.symbol
			end = i[1]*self.symbol+i[2]
			for j in range(self.symbol): # iterate through all transitions
				start2 = start + j # Start state now is (start state # * transition #) + alphabet #
				g.addEdge(start2,end)

		for accept_state in self.accept: # iterate through list of accepting states
			for a in range(self.symbol): # iterate through alphabet symbols
				for d in range(self.symbol): # iterate through alphabet symbols
					# Again, create reference number
					s = accept_state*self.symbol+a # accepting state number * (size of alphabet - 1) + alphabet symbol
					g.printAllPaths(s,d)
'''
	def generate(self):
		for i in self.accept:
			for j in range(self.symbol):
				self.search(i,[j])
	
	

	def search(self,currentState,pastState,path):
		if currentState = 0:
			self.path[currentState][pastState]=[True,path]
		elif currentState != 0:
'''
