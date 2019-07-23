'''Contains functions to Monte Carlo sample DFAs to investigate what proportion approximate the true DFA'''
import matplotlib.pyplot as plt
import TensorGenerator
import random
import AcceptingStringGenerator
import numpy as np
import CompareDFAGenerator as cdg
import time
import copy
from reachable import reachesAll
NUM_STATES = 5 # number of states in target DFA (and randomly sampled test DFAs)
NUM_SYM = 2 # number of symbols in alphabet of language accepted DFAs in search space
NUM_EXAMPLES = 100 # number of training examples (WARNING: might not work as intended if this is odd)
STR_LENGTH = AcceptingStringGenerator.STRING_LENGTH # length of strings in training data
NUM_SIM = 5000 # number of random DFAs to test on training data
Q_MIN = .3 # proportion of strings in training data that must be correctly classified as acccepting or rejecting for a DFA to be considered approximately correct

# 1. Randomly generate DFA and training data

def get_dfa(state_num, sym_num):
	'''
	Randomly generates a DFA (tensor representation) with state_num states
	and sym_num symbols in its alphabet

	Parameters
	----------
	state_num: int
	  number of states in DFA to generate
	sym_num: int
	  cardinality of alphabet in DFA to generate

	Returns
	-------
	TensorGenerator object (which is a DFA tensor)
	'''
	count = 0
	dfa = TensorGenerator.TensorGenerator(state_num, sym_num)
	return dfa,reachesAll(dfa.tensor)
	'''
	# check connectivity
	connected = True
	for dest_state in range(1,state_num):
		if connected == True:
			connected = False
			for str_len in range(1,state_num):
				if connected == False:
					if AcceptingStringGenerator.get_strings(dfa.tensor, dest_state, str_len) != set():
						connected = True
		else: connected = False

	if connected:
		return dfa
	else:
		return get_dfa(state_num, sym_num)
	'''

def get_examples(target_tens):
	'''
	Generates training data set with NUM_EXAMPLES strings of length STR_LENGTH
	from tens
	# TODO maybe add more string lengths
	# TODO automatically choose string length

	Parameters
	----------
	target_tens: TensorGenerator object
	  tensor representation of a DFA as encoded by TensorGenerator class

	Returns
	-------
	dictionary of training examples
	'''
	test_data = {}

	# Generate NUM_EXAMPLES/2 random strings
	# We're assuming these will probably not be accepted so we'll have a 50/50 dist acc/rej strings
	for datum in range(NUM_EXAMPLES//2):
		# Randomly generate string
		datum_str = ''
		for i in range(STR_LENGTH):
			datum_str += str(random.randint(0,NUM_SYM-1)) # make a list of characters to test
		accepted = target_tens.checkAccepting([int(i) for i in datum_str])
		test_data[datum_str] = accepted

	# Generate NUM_EXAMPLES/2 accepted strings
	accepted_str = AcceptingStringGenerator.count_wrapper(target_tens)
	if len(accepted_str) > 0:
		for datum in range(NUM_EXAMPLES//2):
			datum_str = random.choice(accepted_str)
			test_data[datum_str] = True
	return test_data


# 2. Randomly sample DFAs and test whether they accept training data


def standard_accuracy(dfa_tens, test_data):
	'''Returns the standard accuracy of dfa_tens on test_data, i.e.
		  (# examples in test_data classified correctly)/(total # examples in test_data)
		= (# examples in test_data classified correctly)/NUM_EXAMPLES

	Parameters
	----------
	dfa_tens: TensorGenerator object
	 tensor on which to test accuracy on training data
	test_data: set of tuples (string, bool)
	  the bool is either 0 or 1 and is whether the training string is accepted

	Returns
	-------
	proportion of test_data samples that are correctly classified by dfa_tens
	'''
	correct = 0
	failed = 0

	for string in test_data:
		if test_data[string] == dfa_tens.checkAccepting([int(i) for i in string]):
			correct += 1
		else:
			failed += 1
	return correct/(correct + failed)


def f_accuracy(dfa_tens, test_data):
	'''Returns the F1 accuracy of dfa_tens on test_data, i.e.
		  2*(# correctly classified positive examples)/
			(# examples classified as positive + # positive examples in test_data)

	Parameters
	----------
	dfa_tens: TensorGenerator object
	 tensor on which to test accuracy on training data
	test_data: dictionary where keys are strings and values are bools
	  the bool is either 0 or 1 and is whether the training string is accepted

	Returns
	-------
	F1 score of dfa_tens on test_data
	'''
	try:
		true_pos = 0
		all_relevant = 0
		all_pos = 0
		for string in test_data:
			if test_data[string] == 1:
				all_relevant += 1
				if test_data[string] == dfa_tens.checkAccepting([int(i) for i in string]):
					true_pos += 1
			if dfa_tens.checkAccepting([int(i) for i in string]):
				all_pos += 1
		return 2 * true_pos / (all_pos + all_relevant)
	except ZeroDivisionError as err:
		print(err)
		return 2


def mult_accuracy(dfa_tens, test_data):
	'''Returns the multiplicative accuracy (Kyle's accuracy) of dfa_tens on test_data, i.e.
		  (accuracy on positive examples) * (accuracy on negative examples)

	Parameters
	----------
	dfa_tens: TensorGenerator object
	 tensor on which to test accuracy on training data
	test_data: dictionary where keys are strings and values are bools
	  the bool is either 0 or 1 and is whether the training string is accepted

	Returns
	-------
	multiplicative accuracy of dfa_tens on test_data
	'''
	pos_data = {datum: test_data[datum] for datum in test_data if test_data[datum] == 1}
	neg_data = {datum: test_data[datum] for datum in test_data if test_data[datum] == 0}
	pos_acc = standard_accuracy(dfa_tens, pos_data)
	neg_acc = standard_accuracy(dfa_tens, neg_data)
	return pos_acc * neg_acc # TODO do we take the sqrt of this?


def generator():
	sampleSet = {}
	numSample = NUM_EXAMPLES
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

	'''
	for i in range(numSample):
		sample = tuple([np.random.randint(2) for j in range(np.random.randint(4, STR_LENGTH))])
		s = "".join(map(str, sample))
		result = int(s[len(s) - 4] == '1')
		sampleSet[s] = result
	'''
	'''
	while len(sampleSet) < numSample:

		sample = tuple([np.random.randint(2) for i in range(np.random.randint(STR_LENGTH))])

		if len(sample) > 0:
			s = "".join(map(str, sample))
			result = int(int(s, 2) % 7 == 0)
		else:
			s = ''
			result = 1

		sampleSet[s] = result
	'''
	return sampleSet


def sim():
	'''
	Returns proportion of DFAs with n or fewer states that are approximately
	correct (within Q_MIN accuracy)
	'''
	target_tens = get_dfa(NUM_STATES, NUM_SYM) # Randomly generate a target DFA, from which we will get training data
	test_data = get_examples(target_tens)

	# MAKE SURE DFA ACCEPTS SOMETHING
	# tensor_success = False
	# while tensor_success is False:
	#	 if (list(test_data.values()).__contains__(True)):
	#		 tensor_success = True
	#	 else:
	#		 target_tens = get_dfa(NUM_STATES, NUM_SYM)
	#		 test_data = get_examples(target_tens)


	# UNCOMMENT IF YOU WANT DIVISIBILITY-BY-5 TARGET DFA. YOU CAN ALTER GENERATOR FUNCTION FOR ANY SPECIFIC DFA
	# test_data = generator()

	accurate = 0
	inaccurate = 0

	for i in range(NUM_SIM):
		test_dfa = get_dfa(NUM_STATES, NUM_SYM)
		accuracy = standard_accuracy(test_dfa, test_data)
		if accuracy <= 1:
			if accuracy >= Q_MIN: accurate += 1
			else: inaccurate += 1

	return accurate/(accurate + inaccurate)


def sim2(num_test_dfa=NUM_SIM):
	'''
	Returns list of accuracies of DFAs with n or fewer states
	'''
	totalTime=time.time()
	startTime = time.time()
	target_tens = get_dfa(NUM_STATES, NUM_SYM) # Randomly generate a target DFA, from which we will get training data
	print('finish get dfa', time.time()-startTime)
	startTime=time.time()
	test_data = get_examples(target_tens)
	print('finish get examples',time.time()-startTime)
	#test_data = generator() # TODO uncomment if you want divisibility-by-5 target DFA. Can also change generator function to be divisibility-by-[any number]

	accuracy_l = []
	

	for i in range(num_test_dfa):
		startTime = time.time()
		test_dfa = get_dfa(NUM_STATES, NUM_SYM)
	
		print('get test dfa ', i, 'take time', time.time()-startTime)
		startTime=time.time()
		accuracy = standard_accuracy(test_dfa, test_data)
		print('get accuracy',i,' take time', time.time()-startTime)
		
		accuracy_l.append(accuracy)
	print('total ', time.time()-totalTime)
	return accuracy_l

def sim3(num_test_dfa = NUM_SIM, length = 3, alphabet = 2):
	adfaset, cdfaset, tensor = cdg.getExampleDict(length, alphabet)
	accuracy_a = []
	accuracy_c = []

	for i in range(num_test_dfa):
		test_dfa = get_dfa(tensor.state, alphabet)
		accuracy = (standard_accuracy(test_dfa, adfaset), standard_accuracy(test_dfa, cdfaset))
		accuracy_a.append(accuracy[0])
		accuracy_c.append(accuracy[1])

	return accuracy_a, accuracy_c
def get_dfa4(state,sym):
	accept=set()

	row = [0 for i in range(state)]
	matrix = [copy.deepcopy(row) for i in range(state)]
	tensor = [copy.deepcopy(matrix) for i in range(sym)]
	numberAccept = random.randint(1,state)
	for i in range(numberAccept):
		accept.add(random.randrange(0,state))
	for i in range(sym):
		for j in range(state):
			k = random.randrange(0,state)
			tensor[i][j][k]=1
	return (tensor,accept), reachesAll(tensor)

def getData4(num_states=20,num_sym=2,minNum=450,perSample=30):
	print('start dfa collection')
	numSample = minNum//perSample
	dfa_ls=[copy.deepcopy([]) for i in range(num_states+1) ]
	for i in range(2,(num_states+1)*2):
		for j in range(450):
			#print(i,j)
			dfa, num = get_dfa4(i,num_sym)
			if num < num_states+1:
				dfa_ls[num].append(dfa)
		print('dfa collection process', i)
	print("complete dfa collection")
	print('start checking')
	for i in range(2,num_states+1):
			print('state number', i , 'number of dfa', len(dfa_ls[i]))
			if len(dfa_ls[i])<minNum:
				print('insufficient dfa')
				a= 2/0
	print('finish checking')
	return dfa_ls

def sim4(num_states=20,num_test=1,num_sym=2, minNum = 450, perSample = 30,stringSize = 300,threshold=0.4):
	'''
	Returns list of accuracies of DFAs with n or fewer states
	'''
	print('start dfa collection')
	numSample = minNum//perSample
	dfa_ls=[copy.deepcopy([]) for i in range(num_states+1) ]
	for i in range(2,(num_states+1)*2):
		for j in range(450):
			#print(i,j)
			dfa, num = get_dfa4(i,num_sym)
			if num < num_states+1:
				dfa_ls[num].append(dfa)
		print('dfa collection process', i)
	print("complete dfa collection")

	x_axis=[]
	y_axis=[]
	print('start checking')
	for i in range(2,num_states+1):
			print('state number', i , 'number of dfa', len(dfa_ls[i]))
			if len(dfa_ls[i])<minNum:
				print('insufficient dfa')
				a= 2/0
	print('finish checking')
	print('start testing')
	for i in range(2,num_states+1):
		print(' testing state',i)
		ls = random.shuffle(dfa_ls[i])
		accuracy_ls=[]
		for j in range(minNum//perSample):
			
			print(' testing state',i, ' part ', j,'getting test data')
			
			index = random.randrange(j,j+perSample)
			
			#target dfa
			tensor,accept = dfa_ls[i][index]
			
			print('getting pre made pos for state',i,'part', j)
			test_data = get_examples4(tensor,accept)
			
			if len(test_data)==0 or test_data is None:
				print('not sufficient test data')
				continue
			
			random.shuffle(test_data)
			
			if len(test_data)>stringSize//2:
				pos_test_data= test_data[0:stringSize//2]
			else:
				pos_test_data=test_data

			posCount = len(pos_test_data)
			
			negCount = 0
			
			neg_test_data = []
			print('getting random for state',i,'part', j)
			for k in range(stringSize+100):
				length = random.randint( 1,num_states)
				s = ''.join( [ str( random.randrange( num_sym ) ) for l in range(length) ] )
				
				if lookupString(s, tensor, accept):
					if posCount< stringSize//2:
						posCount+=1
						pos_test_data.append(s)
				elif not lookupString(s,tensor, accept):
					if  negCount< stringSize//2:
						negCount+=1
						neg_test_data.append(s)
					
			print('testing accuracy for state',i,'part', j)
			part_ls=[]
			for k in range(j*perSample,(j+1)*perSample):
				if k != index:
					totalCount = 0
					correctCount = 0
					test_dfa,test_accept = dfa_ls[i][k]
					if len(pos_test_data) !=0 :
						correctCount += accuracy4(pos_test_data,test_dfa,test_accept, True)
						totalCount += stringSize//2
					if len(neg_test_data) !=0 :
						correctCount += accuracy4(neg_test_data,test_dfa,test_accept,False)
						totalCount += stringSize//2
					part_ls.append(correctCount/totalCount)
					print(correctCount/totalCount)
			accuracy_ls.append(np.mean(np.array(part_ls)))
		accuracy_ls = np.array(accuracy_ls)
		accuracy_ls = accuracy_ls > threshold
		score = np.sum(accuracy_ls)/perSample
		if score>1:
			print("Error")
			print(accuracy_ls)
			a=2/0
		y_axis.append(score)
		x_axis.append(i)
		print(' state i accuracy ', score)

	
	plt.scatter(x_axis,y_axis)
	plt.show()
	return x_axis,y_axis

def accuracy4(test_data,tensor,accept,condition):
	totalCount = 0
	count = 0
	for s in test_data:
		if lookupString(s,tensor,accept) == condition:
			count+=1
	return count

def lookupString(string, tensor,accept):
	current_state = 0
	for i in string:
		current_state = iterCharInternal(current_state,tensor,int(i))
	return current_state in accept
def iterCharInternal(state,tensor, char):
	row = tensor[char][state]
	newstate = 0
	return row.index(1)
			

def get_examples4(tensor, accept):
	startTime = time.time()
	print(len(tensor[0]))
	ls=[]
	#accept = dfa.outputAccept()
	numState = len(tensor[0])
	table = acceptStrings4(tensor, numState+1)

	for i in range(1,numState):
		for j in accept:
			thing = table[0][j][i]
			for k in thing:
				ls.append(k)
	ls = list(set(ls))
	print(time.time()-startTime, 'seconds')
	return ls

def acceptStrings4(tensor,maxLen):
	init_state = 0

	num_states = len(tensor[0]) # number of states in the DFA
	alphabet_size = len(tensor) # number of symbols in alphabet
	# Initialize table to be filled up using DP. The value string_table[source][dest][e] will
	# store the possible walks from source to dest with exactly e edges
	cell_content = set()
	row = [copy.deepcopy(cell_content) for i in range(maxLen)]
	matrix = [copy.deepcopy(row) for i in range(num_states)]
	string_table = [copy.deepcopy(matrix) for i in range(num_states)]

	# Now fill in table
	for e in range(maxLen): # Loop for number of state transitions from 0 to str_len
		for source in range(num_states):  # for source
			for dest in range(num_states):  # for destination
				for sym in range(alphabet_size):
					sym_adj_matrix = tensor[sym] # adjacency matrix representation of DFA states and transitions for one symbol in alphabet

					# from base cases
					if (e == 0) and (source == dest):
						string_table[source][dest][e].add('')

					if (e == 1) and (sym_adj_matrix[source][dest] == 1):
						string_table[source][dest][e].add(str(sym))

					# go to adjacent only when number of edges is more than 1
					if e > 1:
						for a in range(num_states):  # for every possibly adjacent state
							if sym_adj_matrix[source][a] == 1:  # if there is a transition from source state to a^th state
								str_l = string_table[a][dest][e - 1]
								for string in str_l.copy():
									string_table[source][dest][e].add(str(sym) + string)

	return string_table
