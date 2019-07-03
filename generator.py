import random
import numpy as np
import DfaSearchSim
STR_LENGTH=10
NUM_EXAMPLES = 100
ty = "uniform"

def generator_uniform(option, n=(0, 0)):
    posSet = {}
    negSet = {}
    def generator_g():
        if option == 'switch': return generator_switch()
        if option == 'right': return generator_nth_from_right(n[0])
        if option == 'div': return generator_divn(n)
    while len(posSet) < NUM_EXAMPLES or len(negSet) < NUM_EXAMPLES:
        sample,result = generator_g()
        if result == 1: posSet[sample] = result
        else: negSet[sample] = result

    return [posSet, negSet]

'''
def generator_uniform():
	generator_g()=
    sampleSet = {}
    numSample = NUM_EXAMPLES
	while len(sampleSet)<numSample:
		sample,result = generator_g()
		sampleSet[sample] = result
	return sampleSet
def generator_posneg():
	generator_g() = 
    samplePos = {}
	sampleNeg = {}
    numSample = NUM_EXAMPLES
	while len(samplePos)<numSample/2:
		sample,result = generator_g()
		if(result>0):
			samplePos[sample] = result
	while len(sampleNeg)<numSample/2:
		sample,result = generator_g()
		if(result
		sampleNeg[sample]=result
	return sampleSet
'''


def generator_switch():
    length = random.randint(2, STR_LENGTH)
    switches = 0
    string_array = [random.randint(0, 1)]
    for i in range(length - 1):
        next = random.randint(0, 1)
        string_array.append(next)
        if next != string_array[i]:
            switches += 1
    s = "".join(map(str, string_array))
    return s, int(switches % 2 == 0)

def generator_nth_from_right(n):
    sample = tuple([np.random.randint(2) for j in range(np.random.randint(n + 1, STR_LENGTH + n))])
    s = "".join(map(str, sample))
    result = int(s[len(s) - n] == '1')
    return s,result

def generator_divn(n):
    sample = tuple([np.random.randint(2) for i in range(np.random.randint(1,STR_LENGTH))])
    s = "".join(map(str, sample))
    result = int(int(s,2) % n[0] == n[1])
    return s, result

def dict2ls(dictionary):
    tuple_set = []
    for key in dictionary.keys():
        tuple_set.append((key, dictionary[key]))
    return tuple_set

#def convert(pos,neg):
