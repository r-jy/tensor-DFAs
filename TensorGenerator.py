import numpy 
import random
import copy
<<<<<<< HEAD

class TensorGenerator:
	start = 0
	accept={0}
	state=2
	symbol=2
	tensor = []
	def __init__(self,stateNum,symbolNum):
		self.input(stateNum,symbolNum)
		self.generator()
		self.randomize()
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
=======
start = 0
accept={0}
state=2
symbol=2
tensor = []

def run(stateNum,symbolNum):
	input(stateNum,symbolNum)
	generator()
	randomize()
def input(stateNum,symbolNum):
	global state
	global symbol
	state = stateNum
	symbol = symbolNum

def generator():
	global state
	global symbol
	global tensor
	row = [0 for i in range(state)]
	matrix = [copy.deepcopy(row) for i in range(state)]
	tensor = [copy.deepcopy(matrix) for i in range(symbol)]
def randomize():
	global state
	global symbol
	global tensor
	global accept
	numberAccept = random.randrange(0,state)
	for i in range(numberAccept):
		accept.add(random.randrange(0,state))
	for i in range(symbol):
		for j in range(state):
			k = random.randrange(0,state)
			tensor[i][j][k]=1
	return tensor
>>>>>>> b424016a015676e7f216d7f21385e86e36746e22

