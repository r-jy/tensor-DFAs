import numpy 
import random
import copy
import STP
import SwapMatrix

class TensorGenerator:
	start = 0
	accept={0}
	state=2
	symbol=2
	tensor = []
	STM = []
	swappedSTM = []
	charID = numpy.array([])
	stateID = numpy.array([])
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
		self.charID = numpy.identity(self.symbol)
		self.stateID = numpy.identity(self.state)

	def randomize(self):
		numberAccept = random.randrange(0,self.state)
		for i in range(numberAccept):
			self.accept.add(random.randrange(0,self.state))
		for i in range(self.symbol):
			for j in range(self.state):
				k = random.randrange(0,self.state)
				self.tensor[i][j][k]=1
		return self.tensor
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
		self.swappedSTM = STP.STP.compute(self.STM, SwapMatrix.SwapMatrix.getMatrix(self.state, self.symbol))
		return self.STM

	def processChar(self, state, char):
		return self.processCharInternal(self.stateID[:, [state]], char)

	def processCharInternal(self, stateV, char):
		m1 = STP.STP.compute(self.STM, self.charID[:, [char]])
		m2 = STP.STP.compute(m1, stateV)
		return m2

	def processString(self, string):  # runs a string through your DFA and tells you the final state
		current_state = self.stateID[:, [self.start]]
		for i in string:
			current_state = self.processCharInternal(current_state, i)
		return self.getNumFromDelta(current_state)

	def pathAlgorithm(self, length, initialState, finalState):
		m = self.symbol
		t = length
		M = copy.deepcopy(self.swappedSTM)
		for i in range(length - 1):
			M = STP.STP.compute(M, self.swappedSTM)
		iDelta = self.stateID[:, [initialState]]
		M = STP.STP.compute(M, iDelta)
		# print(M)
		fDelta = self.stateID[:, [finalState]]
		acceptedColumns = []
		for i in range(len(M[0])):
			currentColumn = M[:, [i]]
			if (currentColumn == fDelta).all():
				acceptedColumns.append(i)
		# print(acceptedColumns)
		setOfS = []
		for j in range(t):
			tempMatrix = []
			Im = self.charID
			ones = numpy.ones(m**(t-1-j))
			sPart = numpy.kron(Im, ones)
			for i in range(m**j):
				tempMatrix.append(sPart)
			tempMatrix = numpy.concatenate(tempMatrix, 1)
			setOfS.append(tempMatrix)
		# print(setOfS)
		setOfStrings = []
		bigID = numpy.identity(m**t)
		print("number of paths for Jonan: " + str(len(acceptedColumns)))
		for l in acceptedColumns:
			string = []
			lDelta = bigID[:, [l]]
			for j in range(length):
				charDelta = STP.STP.compute(setOfS[j], lDelta)
				char = self.getNumFromDelta(charDelta)
				string.append(char)
			setOfStrings.append(string)
		return setOfStrings

	def getNumFromDelta(self, delta):
		for i in range(len(delta)):
			if delta[i][0] == 1:
				return i


