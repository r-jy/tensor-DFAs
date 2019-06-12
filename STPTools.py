import numpy
import copy
import STP

def STPVector(row, column):
    bigger = []  # 1 = row bigger; ends as row, 0 = column bigger; ends as column
    rowMultiplied = []
    columnMultiplied = []
    if len(row) > len(column) or len(row) == len(column):
        bigger = 1
        rowMultiplied = row
        columnMultiplied = column
        if len(row) % len(column) != 0:
            print("failed")
            return
    else:
        bigger = 0
        rowMultiplied = column
        columnMultiplied = row
        if len(column) % len(row) != 0:
            print("failed")
            return
    print(rowMultiplied)
    numpy.lcm
    print(columnMultiplied)
    partitionSize = len(rowMultiplied)//len(columnMultiplied)
    numPartitions = len(columnMultiplied)
    partitionArray = [numpy.multiply(rowMultiplied[i:i + partitionSize], columnMultiplied[i//partitionSize]) for i in range(0, len(rowMultiplied), partitionSize)]
    return numpy.asarray(partitionArray).sum(axis=0)

def PathAlgorithm(tensor, length, initialState, finalState):
    m = tensor.symbol
    t = length
    M = copy.deepcopy(tensor.swappedSTM)
    for i in range(length - 1):
        M = STP.STP.compute(M, tensor.swappedSTM)
    iDelta = tensor.stateID[:, [initialState]]
    M = STP.STP.compute(M, iDelta)
    # print(M)
    fDelta = tensor.stateID[:, [finalState]]
    acceptedColumns = []
    for i in range(len(M[0])):
        currentColumn = M[:, [i]]
        if (currentColumn == fDelta).all():
            acceptedColumns.append(i)
    # print(acceptedColumns)
    setOfS = []
    for j in range(t):
        tempMatrix = []
        Im = tensor.charID
        ones = numpy.ones(m ** (t - 1 - j))
        sPart = numpy.kron(Im, ones)
        for i in range(m ** j):
            tempMatrix.append(sPart)
        tempMatrix = numpy.concatenate(tempMatrix, 1)
        setOfS.append(tempMatrix)
    # print(setOfS)
    setOfStrings = []
    bigID = numpy.identity(m ** t)
    for l in acceptedColumns:
        string = []
        lDelta = bigID[:, [l]]
        for j in range(length):
            charDelta = STP.STP.compute(setOfS[j], lDelta)
            char = tensor.getNumFromDelta(charDelta)
            string.append(char)
        setOfStrings.append(string)
    return setOfStrings
