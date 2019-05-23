import numpy
import copy
import random
from Graph import Graph
class StringGenerator:
	depth = 0
	length = 0
	tensor = []
	accept=set({})
	state = 0
	transition=set({})
	def __init__(self,tensor_input,state_input,accept_input,symbol_input):
		self.tensor = tensor_input
		self.accept = accept_input
		self.symbol = symbol_input
		self.state = state_input
		self.accept.remove(0)
		content = ["empty",[]]
		row = [ copy.deepcopy(content) for i in range(self.state)]
		self.path = [copy.deepcopy(row) for i in range(self.state)]
	def convert(self):
		for i in range(self.symbol):
			for j in range(self.state):
				for k in range(self.state):
					if self.tensor[i][j][k] ==1:
						self.transition.add( (j,k,i)) #--> (input/current state, next state,symbol))
		return self.transition
	def export(self):
		g=Graph(self.state*self.symbol,self.state)
		for i in self.transition:
			start = i[0]*self.symbol
			end = i[1]*self.symbol+i[2]
			for j in range(self.symbol):
				start2 = start+j
				g.addEdge(start2,end)
		for i in self.accept:
			for j in range(self.symbol):
				for k in range(self.symbol):
					s = i*self.symbol+j
					d = k
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
