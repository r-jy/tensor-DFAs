import numpy as np
import random
import TensorGenerator

def getNumbers(length, alphabet):
    stringsOfLength = np.zeros(length)
    strings = []
    strings.clear()
    for i in range(0, length):
        numberOfStrings = random.randint(0, alphabet**(i+1))
        tempStrings = set()
        tempStrings.clear()
        for j in range(numberOfStrings):
            string = "".join([str(random.randint(0,1)) for k in range(i + 1)])
            tempStrings.add(string)
        stringsOfLength[i] = len(tempStrings)
        strings.append(tempStrings)
    for i in range(length - 1, 0, -1):
        tempStrings = strings[i]
        print(strings[i-1])
        for j in tempStrings:
            strings[i - 1].add(j[0:i])
        stringsOfLength[i - 1] = len(strings[i - 1])
    # + 2 for initial state and trash state
    tensor = TensorGenerator.TensorGenerator(int(sum(stringsOfLength)) + 2, alphabet)
    return stringsOfLength, strings, tensor