import re

# http://ivanzuzak.info/noam/webapps/fsm_simulator/
def tensorToNoam(tensor, file="noam.txt"):
    states = ['s' + str(i) for i in range(tensor.state)]
    accept = []
    for i in tensor.accept:
        accept.append(states[i])
    alphabet = [str(i) for i in range(tensor.symbol)]
    transitions = []
    for symbol in range(len(tensor.tensor)):
        for row in range(len(tensor.tensor[symbol])):
            input = states[row]
            output = ''
            for column in range(len(tensor.tensor[symbol][row])):
                if tensor.tensor[symbol][row][column] == 1:
                    output = states[column]
            transitions.append(input + ':' + alphabet[symbol] + '>' + output)
    noamFile = open(file, 'w')
    noamFile.writelines(['#states', '\n'])
    for i in states:
        noamFile.writelines([i, '\n'])
    noamFile.writelines(['#initial\n', 's0\n'])
    noamFile.writelines(['#accepting\n'])
    for i in accept:
        noamFile.writelines([i, '\n'])
    noamFile.writelines(['#alphabet\n'])
    for i in range(tensor.symbol):
        noamFile.writelines([str(i), '\n'])
    noamFile.writelines(['#transitions\n'])
    for i in transitions:
        noamFile.writelines([i,'\n'])

def parseDot(file="ans.dot"):
    ansFile = open(file, 'r')
    ansString = ansFile.read()
    ansStringList = ansString.split('\n')
    initState = 0
    accStates = set()
    stateDict = {}
    symbolDict = {}
    takenStates = 0
    takenSymbols = 0
    delta = []
    for stringToTest in ansStringList:
        #Check if it represents an initial state.
        if stringToTest.__contains__('bold'):
            startState = int(re.findall('[0-9][0-9]*', stringToTest)[0])
            if not stateDict.keys().__contains__(startState):
                stateDict[startState] = takenStates
                delta.append([0 for i in range(takenSymbols)])
                takenStates += 1
            initState = stateDict[startState]
        #Check if it represents an accepting state.
        if stringToTest.__contains__('peripheries'):
            endState = int(re.findall('[0-9][0-9]*', stringToTest)[0])
            if not stateDict.keys().__contains__(endState):
                stateDict[endState] = takenStates
                delta.append([0 for i in range(takenSymbols)])
                takenStates += 1
            accStates.add(stateDict[endState])
        #Check if it is a transition.
        if stringToTest.__contains__('->'):
            transitionList = re.findall('[0-9][0-9]*|"."', stringToTest) # Get in state, out state, and character.
            startState = int(transitionList[0])
            endState = int(transitionList[1])
            symbol = transitionList[2][1]
            if not stateDict.keys().__contains__(startState):
                stateDict[startState] = takenStates
                delta.append([0 for i in range(takenSymbols)])
                takenStates += 1
            if not stateDict.keys().__contains__(endState):
                stateDict[endState] = takenStates
                delta.append([0 for i in range(takenSymbols)])
                takenStates += 1
            if not symbolDict.keys().__contains__(symbol):
                symbolDict[symbol] = takenSymbols
                takenSymbols += 1
                for row in delta:
                    row.append(0)
            delta[stateDict[startState]][symbolDict[symbol]] = stateDict[endState]

    return initState, accStates, delta

def deltaToNoam(initState, accStates, delta, file="noam.txt"):
    noamFile = open(file, 'w')
    noamFile.writelines(['#states', '\n'])
    noamFile.writelines([f"s{i}\n" for i in range(len(delta))])
    noamFile.writelines(['#initial\n', f's{initState}\n'])
    noamFile.writelines(['#accepting\n'])
    noamFile.writelines([f"s{i}\n" for i in accStates])
    noamFile.writelines(['#alphabet\n'])
    noamFile.writelines([f"{i}\n" for i in range(len(delta[0]))])
    noamFile.writelines(['#transitions\n'])
    noamFile.writelines([f"s{start}:{symbol}>s{delta[start][symbol]}\n" for symbol in range(len(delta[0])) for start in range(len(delta))])

def abbadingoToGD(file="dfa.dct"):
    abFile = open(file, 'r')
    abString = abFile.read()
    abStringList = abString.split('\n')
    infoString = abStringList.pop(0)
    infoStringList = infoString.split(' ')
    numberOfExamples = int(infoStringList[0])
    train = []
    for i in range(numberOfExamples):
        stringArray = []
        exampleString = abStringList.pop(0)
        exampleStringList = list(map(int, exampleString.split(' ')))
        correct = exampleStringList[0]
        stringArray = exampleStringList[2:]
        train.append((stringArray, correct))
    return train