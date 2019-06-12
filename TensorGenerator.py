import numpy
import random
import copy
import STP
import SwapMatrix
import time


class TensorGenerator:
    start = 0
    accept = set()
    state = 2
    symbol = 2
    tensor = []
    STM = []
    swappedSTM = []
    charID = numpy.array([])
    stateID = numpy.array([])

    def __init__(self, stateNum, symbolNum):
        self.accept.clear()
        self.input(stateNum, symbolNum)
        self.generator()
        self.randomize()

    def input(self, stateNum, symbolNum):
        self.state = stateNum
        self.symbol = symbolNum


    def generator(self):
        row = [0 for i in range(self.state)]
        matrix = [copy.deepcopy(row) for i in range(self.state)]
        self.tensor = [copy.deepcopy(matrix) for i in range(self.symbol)]
        self.charID = numpy.identity(self.symbol)
        self.stateID = numpy.identity(self.state)


    def randomize(self):
        numberAccept = random.randrange(1, self.state)
        for i in range(numberAccept):
            self.accept.add(random.randrange(0, self.state))
        for i in range(self.symbol):
            for j in range(self.state):
                k = random.randrange(0, self.state)
                self.tensor[i][j][k] = 1
        temptensor = []
        for i in range(self.symbol):
            temptensor.append(numpy.transpose(self.tensor[i]))
        self.STM = numpy.concatenate(temptensor, 1)
        self.swappedSTM = STP.STP.compute(self.STM, SwapMatrix.SwapMatrix.getMatrix(self.state, self.symbol))
        return self.tensor


    def checkAccepting(self, string):
        if self.accept.__contains__(self.processString(string)):
            return True
        return False


    def processString(self, string):  # runs a string through your DFA and tells you the final state
        current_state = self.stateID[:, [self.start]]
        for i in string:
            current_state = self.processCharInternal(current_state, i)
        return self.getNumFromDelta(current_state)


    def processCharInternal(self, stateV, char):
        m1 = STP.STP.compute(self.STM, self.charID[:, [char]])
        m2 = STP.STP.compute(m1, stateV)
        return m2


    def processChar(self, state, char):
        return self.processCharInternal(self.stateID[:, [state]], char)


    def getNumFromDelta(self, delta):
        for i in range(len(delta)):
            if delta[i][0] == 1:
                return i
