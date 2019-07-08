import numpy as np
import random
import TensorGenerator
import AcceptingStringGenerator as asg
import copy
import csv

def getStateNumbers(length, alphabet):
    stringsOfLength = np.zeros(length)
    strings = []
    posStrings = []
    strings.clear()
    for i in range(0, length):
        numberOfStrings = random.randint(0, alphabet**(i+1))
        tempStrings = {}
        tempPosStrings = set()
        tempStrings.clear()
        for j in range(numberOfStrings):
            string = "".join([str(random.randint(0,1)) for k in range(i + 1)])
            tempStrings[string] = True
            tempPosStrings.add(string)
        stringsOfLength[i] = len(tempStrings)
        strings.append(tempStrings)
        posStrings.append(tempPosStrings)
    for i in range(length - 1, 0, -1):
        tempStrings = strings[i]
        #print(strings[i-1])
        for j in tempStrings:
            strings[i - 1][j[0:i]] = False
        stringsOfLength[i - 1] = len(strings[i - 1])
    # + 2 for initial state and trash state
    tensor = TensorGenerator.TensorGenerator(int(sum(stringsOfLength)) + 2, alphabet)
    return stringsOfLength, strings, posStrings, tensor

def getExampleDict(length, alphabet):
    a, b, c, tensor = getStateNumbers(length, alphabet)
    adfaSet = {}
    strings = []
    strings.append(set())
    strings[0].clear()
    strings[0].update([str(i) for i in range(alphabet)])
    for i in strings[0]:
        adfaSet[i] = False
    for i in range(1, length):
        strings.append(set())
        strings[i].clear()
        for j in strings[i - 1]:
            strings[i].update([j + str(k) for k in range(alphabet)])
        for j in strings[i]:
            adfaSet[j] = False
    cdfaSet = copy.deepcopy(adfaSet)
    for i in range(length, tensor.state):
        strings.append(set())
        strings[i].clear()
        for j in strings[i - 1]:
            strings[i].update([j + str(k) for k in range(alphabet)])
        for j in strings[i]:
            cdfaSet[j] = False
    #print(cdfaSet)
    for i in c:
        for j in i:
            adfaSet[j] = True
    for i in asg.count_wrapper2(tensor, tensor.state):
        cdfaSet[i] = True

    return adfaSet, cdfaSet, tensor

def getExampleSet(length, alphabet):
    adfaSet, cdfaSet, tensor = getExampleDict(length, alphabet)
    adfaPos = set([k for (k, v) in adfaSet.items() if v])
    adfaNeg = set(adfaSet.keys()) - adfaPos
    cdfaPos = set([k for (k, v) in cdfaSet.items() if v])
    cdfaNeg = set(cdfaSet.keys()) - cdfaPos
    return (adfaPos, adfaNeg), (cdfaPos, cdfaNeg), tensor

def getTrainingSet(length, alphabet):
    adfa, cdfa, tensor = getExampleSet(length, alphabet)
    adfaTraining = (set(random.sample(adfa[0], len(adfa[0])//2)), set(random.sample(adfa[1], len(adfa[1])//2)))
    adfaTesting = (adfa[0] - adfaTraining[0], adfa[1] - adfaTraining[1])
    cdfaTraining = (set(random.sample(cdfa[0], len(cdfa[0]) // 2)), set(random.sample(cdfa[1], len(cdfa[1]) // 2)))
    cdfaTesting = (cdfa[0] - cdfaTraining[0], cdfa[1] - cdfaTraining[1])
    return (adfaTraining, adfaTesting), (cdfaTraining, cdfaTesting), tensor

def getCSV(adfaTuple, cdfaTuple, tensor):
    with open('adfa.csv', 'w') as adfacsv:
        adfawriter = csv.writer(adfacsv)
        adfawriter.writerow(adfaTuple[0][0])
        adfawriter.writerow(adfaTuple[0][1])
        adfawriter.writerow(adfaTuple[1][0])
        adfawriter.writerow(adfaTuple[1][1])
    with open('cdfa.csv', 'w') as cdfacsv:
        cdfawriter = csv.writer(cdfacsv)
        cdfawriter.writerow(cdfaTuple[0][0])
        cdfawriter.writerow(cdfaTuple[0][1])
        cdfawriter.writerow(cdfaTuple[1][0])
        cdfawriter.writerow(cdfaTuple[1][1])
    with open('tensor.csv', 'w') as tensorcsv:
        tensorwriter = csv.writer(tensorcsv)
        tensorwriter.writerow([tensor.start, tensor.symbol, tensor.state, len(tensor.accept)])
        tensorwriter.writerow(list(tensor.accept))
        tensorwriter.writerow([None])
        for i in range(tensor.symbol):
            for j in range(tensor.state):
                tensorwriter.writerow(tensor.tensor[i][j])
            tensorwriter.writerow([None])