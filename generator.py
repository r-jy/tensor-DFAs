
import numpy as np

NUM_EXAMPLES = 200
ty = "uniform"
	


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
def generator_switch():
    sampleSet = {}
    numSample = NUM_EXAMPLES
	#number of switches between 0 and 1
	for i in range(numSample):
        length = random.randint(2, STR_LENGTH)
        switches = 0
        string_array = [random.randint(0,1)]
        for i in range(length - 1):
            next = random.randint(0,1)
            string_array.append(next)
            if next != string_array[i]:
                switches += 1
        s = "".join(map(str, string_array))
        sampleSet[s] = int(switches % 2 == 0)
    return sampleSet

def generator_3rd_dig_1():
    sampleSet = {}
    numSample = NUM_EXAMPLES
    
	# 3rd ditigits is 1
	
    for i in range(numSample):
        sample = tuple([np.random.randint(2) for j in range(np.random.randint(4, STR_LENGTH))])
        s = "".join(map(str, sample))
        result = int(s[len(s) - 4] == '1')
        sampleSet[s] = result
    return sampleSet

def generator_divn(n):
    sampleSet = {}
    numSample = NUM_EXAMPLES
    while len(sampleSet) < numSample:

        sample = tuple([np.random.randint(2) for i in range(np.random.randint(STR_LENGTH))])

        if len(sample) > 0:
            s = "".join(map(str, sample))
            result = int(int(s, 2) % n == 0)
        else:
            s = ''
            result = 1

        sampleSet[s] = result
    return sampleSet
