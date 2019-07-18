# http://ivanzuzak.info/noam/webapps/fsm_simulator/
def printNoam(tensor, file="noam.txt"):
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