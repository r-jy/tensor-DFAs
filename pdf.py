import matplotlib.pyplot as plt
import DfaSearchSim
from os import listdir
import TensorGenerator
import random
import AcceptingStringGenerator
import numpy as np
import generator

NUM_STATES = 7 # number of states in target DFA (and randomly sampled test DFAs)
NUM_SYM = 2 # number of symbols in alphabet of language accepted DFAs in search space
NUM_EXAMPLES = 300 # number of testing examples (WARNING: might not work as intended if this is odd)
STR_LENGTH = AcceptingStringGenerator.STRING_LENGTH # length of strings in testing data
NUM_SIM = 200 # number of random DFAs to test on testing data

NUM_TRIAL = 50

	

def sim_posneg(choice0="mod",choice1=(5,0)):
	'''
	Wrapper function to run Monte Carlo simulation with different threshold accuracies (q_min)
	Could expand to vary more than just parameter q_min
	'''
	meanGraph =[]
	pointGraph=[]
	pointSet =[]
	for i in range(NUM_TRIAL):
		print("--------------------------------------")
		print(   "	  trail   "+str(i))
		print("--------------------------------------")
		mean,graph = single_posneg(choice0,choice1)
		meanGraph.append(mean)
		pointGraph = pointGraph + graph
		pointSet.append(graph)
	return meanGraph, pointGraph, pointSet

def single_posneg(choice0,choice1):
	generator.NUM_EXAMPLES = NUM_EXAMPLES
	positive,negative = generator.generator_uniform(choice0,choice1)
	accuracyGarph =[]
	for i in range(NUM_SIM):
        test_dfa = get_dfa(NUM_STATES, NUM_SYM)
        accuratePos = test_accuracy(test_dfa, positive)
		accurateNeg = test_accuracy(test_dfa, negative)
		accuracyGraph.append( accuratePos * accurateNeg )
	return np.mean(accuracyGraph), accuracyGraph
		




def get_dfa(state_num, sym_num):
    '''
    Randomly generates a DFA with state_num states and sym_num symbols in its alphabet

    Returns
    -------
    TensorGenerator object (which is a DFA tensor)
    '''
    return TensorGenerator.TensorGenerator(state_num, sym_num)



if __name__ == "__main__":

	mean, points, pointls = sim_posneg()
	plt.figure(0)
	plt.plot(mean)
	plt.title('Randomly-Sampled DFAs Accepting Target Language Histogram')
	plt.xlabel('pos and neg accuracy') #approximately accurate threshold proportion of correctly classified DFAs
	plt.ylabel('proportion')
	textstr = 'Constants'
	textstr2 = 'NUM_Q_MIN = ' + str(NUM_Q_MIN) + ' \n' + 'NUM_DFA = ' + str(NUM_DFA) + ' \n' + 'NUM_STATES = ' + str(DfaSearchSim.NUM_STATES) + ' \n' + 'NUM_SYM = ' + str(DfaSearchSim.NUM_SYM) + ' \n' + 'NUM_EXAMPLES = ' + str(DfaSearchSim.NUM_EXAMPLES) + ' \n' + 'STR_LENGTH = ' + str(DfaSearchSim.STR_LENGTH) + ' \n' + 'NUM_SIM = ' + str(DfaSearchSim.NUM_SIM) + ' \n' + 'Q_MIN = ' + str(DfaSearchSim.Q_MIN) + ' \n'
	plt.text(0.92, 0.8, textstr, fontsize=14, fontweight='bold', transform=plt.gcf().transFigure)
	textstr = 'Constants'
	plt.text(0.92, .3, textstr2, fontsize=14, transform=plt.gcf().transFigure)

