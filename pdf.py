import matplotlib.pyplot as plt
import DfaSearchSim
from os import listdir
import TensorGenerator
import random
import AcceptingStringGenerator
import numpy as np
import generator
import reachable

NUM_STATES = 5 # number of states in target DFA (and randomly sampled test DFAs)
NUM_SYM = 2 # number of symbols in alphabet of language accepted DFAs in search space
NUM_EXAMPLES = 100 # number of testing examples (WARNING: might not work as intended if this is odd)
STR_LENGTH = 500 # length of strings in testing data
NUM_SIM = 100 # number of random DFAs to test on testing data

NUM_TRIAL = 50

	

def sim_posneg(choice0="div",choice1=(5,0)):
	'''
	Wrapper function to run Monte Carlo simulation with different threshold accuracies (q_min)
	Could expand to vary more than just parameter q_min
	'''
	meanGraph =[]
	pointGraph=[]
	pointSet =[]
	standardGraph = []
	standardPointGraph =[]
	standardPointSet =[]
	for i in range(NUM_TRIAL):
		print("--------------------------------------")
		print(   "	  trail   "+str(i))
		print("--------------------------------------")
		mean,graph,standard, standardG = single_posneg(choice0,choice1)
		meanGraph.append(mean)
		pointGraph = pointGraph + graph
		pointSet.append(graph)
		standardGraph.append(standard)
		standardPointGraph = standardPointGraph + standardG
		standardPointSet.append(standardG)
	return meanGraph, pointGraph, pointSet, standardGraph, standardPointGraph, standardPointSet

def single_posneg(choice0,choice1):
	generator.NUM_EXAMPLES = NUM_EXAMPLES
	generator.STR_LENGTH = STR_LENGTH
	positive,negative = generator.generator_uniform(choice0,choice1)
	accuracyGraph =[]
	standardGraph = []
	for i in range(NUM_SIM):
		test_dfa = get_dfa(NUM_STATES,NUM_SYM)
		#get_dfa(NUM_STATES, NUM_SYM)
		accuratePos = test_accuracy(test_dfa, positive)
		accurateNeg = test_accuracy(test_dfa, negative)
		standard = test_accuracy(test_dfa, {**positive,**negative})
		accuracyGraph.append( accuratePos * accurateNeg )
		standardGraph.append( standard )
	return np.mean(accuracyGraph), accuracyGraph, np.mean(standardGraph), standardGraph
		


def test_accuracy(dfa_tens, training_data):
    '''
    Parameters
    ----------
    dfa_tens

    Returns
    -------
    '''
    correct = 0
    failed = 0

    for key in training_data:
        if training_data[key] == dfa_tens.checkAccepting([int(i) for i in key]): correct += 1
        else: failed += 1
    
    return correct/(correct + failed)

def get_dfa(state_num, sym_num):
	'''
	Randomly generates a DFA with state_num states and sym_num symbols in its alphabet

	Returns
	-------
	TensorGenerator object (which is a DFA tensor)
	'''
	con = True
	while con:
		dfa = TensorGenerator.TensorGenerator(state_num, sym_num)

		con = not reachable.reachable(dfa.tensor,dfa.accept)
	return dfa


if __name__ == "__main__":

	mean, points, pointls, standard, standpt, standls = sim_posneg()
	num_bins = 20
	plt.figure(0)
	n, bins, patches = plt.hist(mean, num_bins, facecolor='blue', alpha=0.5)
	plt.title('Plot of Multiplicative Means for Targeted DFA')
	plt.xlabel('pos and neg accuracy') #approximately accurate threshold proportion of correctly classified DFAs
	plt.ylabel('proportion')
	#textstr = 'Constants'
	
	textstr2 ='NUM_STATES = ' + str(NUM_STATES) + ' \n' + 'NUM_SYM = ' + str(NUM_SYM) + ' \n' + 'NUM_DFA = ' + str(NUM_SIM) + ' \n' + 'STR_LENGTH = ' + str(STR_LENGTH) + "STR AMOUNT= "+str(NUM_EXAMPLES)+' \n' + 'Num Trail = ' + str(NUM_TRIAL)
	#textstr2 = 'NUM_Q_MIN = ' + str(NUM_Q_MIN) + ' \n' + 'NUM_DFA = ' + str(NUM_DFA) + ' \n' + 'NUM_STATES = ' + str(DfaSearchSim.NUM_STATES) + ' \n' + 'NUM_SYM = ' + str(DfaSearchSim.NUM_SYM) + ' \n' + 'NUM_EXAMPLES = ' + str(DfaSearchSim.NUM_EXAMPLES) + ' \n' + 'STR_LENGTH = ' + str(DfaSearchSim.STR_LENGTH) + ' \n' + 'NUM_SIM = ' + str(DfaSearchSim.NUM_SIM) + ' \n' + 'Q_MIN = ' + str(DfaSearchSim.Q_MIN) + ' \n'
	#plt.text(0.92, 0.8, textstr, fontsize=14, fontweight='bold', transform=plt.gcf().transFigure)
	#textstr = 'Constants'
	plt.text(0.92, .3, textstr2, fontsize=14, transform=plt.gcf().transFigure)
	
	plt.figure(1)
	n, bins, patches = plt.hist(points, num_bins, facecolor='purple', alpha=0.5)
	plt.title('Plot of Multiplicative Points for Targeted DFA')
	plt.xlabel('pos and neg accuracy') #approximately accurate threshold proportion of correctly classified DFAs
	plt.ylabel('proportion')
	#############################################

	plt.figure(2)
	n, bins, patches = plt.hist(standard, num_bins, facecolor='red', alpha=0.5)
	plt.title('Plot of Standard Means for Targeted DFA')
	plt.xlabel('standard accuracy') #approximately accurate threshold proportion of correctly classified DFAs
	plt.ylabel('proportion')
	#textstr = 'Constants'


	plt.figure(3)
	n, bins, patches = plt.hist(standpt, num_bins, facecolor='green', alpha=0.5)
	plt.title('Plot of Standard Points for Targeted DFA')
	plt.xlabel('standard accuracy') #approximately accurate threshold proportion of correctly classified DFAs
	plt.ylabel('proportion')
	#textstr = 'Constants'
	plt.show()
