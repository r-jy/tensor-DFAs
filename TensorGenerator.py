import numpy 
import random
import copy

class TensorGenerator:
	start = 0
	accept={0}
	state=2
	symbol=2
	tensor = []
	STM = []
	def __init__(self,stateNum,symbolNum):
		self.input(stateNum,symbolNum)
		self.generator()
		self.newRandomize()

	def input(self,stateNum,symbolNum):
		self.state = stateNum
		self.symbol = symbolNum

	def generator(self):
		row = [0 for i in range(self.state)]
		matrix = [copy.deepcopy(row) for i in range(self.state)]
		self.tensor = [copy.deepcopy(matrix) for i in range(self.symbol)]

	def randomize(self):
		numberAccept = random.randrange(0,self.state)
		for i in range(numberAccept):
			self.accept.add(random.randrange(0,self.state))
		for i in range(self.symbol):
			for j in range(self.state):
				k = random.randrange(0,self.state)
				self.tensor[i][j][k]=1
		return self.tensor

	def newRandomize(self):
		numberAccept = random.randrange(0, self.state)
		for i in range(numberAccept):
			self.accept.add(random.randrange(0, self.state))
		for i in range(self.symbol):
			for j in range(self.state):
				k = random.randrange(0, self.state)
				self.tensor[i][j][k] = 1
			self.tensor[i] = numpy.transpose(self.tensor[i])
		self.STM = numpy.concatenate(self.tensor, 1)
		return self.STM