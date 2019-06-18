import matplotlib.pyplot as plt
import DfaSearchSim
from os import listdir
import TensorGenerator
import random
import AcceptingStringGenerator
import numpy as np
import generator
import reachable
import os
import scipy.stats as kde
NUM_STATES = 5 # number of states in target DFA (and randomly sampled test DFAs)
NUM_SYM = 2 # number of symbols in alphabet of language accepted DFAs in search space
NUM_EXAMPLES = 200 # number of testing examples (WARNING: might not work as intended if this is odd)
STR_LENGTH = 10 # length of strings in testing data
NUM_SIM = 500 # number of random DFAs to test on testing data

NUM_TRIAL = 10
name  = " mod 5 "
record = 2
info ="  reachable"
reach = True

# MAKE SURE TO CHANGE THE GENERATOR FUNCTION

def sim_posneg(choice0="switch",choice1=(0,0)):
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
	dfa_ls = []
	for i in range(NUM_TRIAL):
		print("--------------------------------------")
		print(   "	  trial   "+str(i))
		print("--------------------------------------")
		mean,graph,standard, standardG, dfa_record = single_posneg(choice0,choice1)
		meanGraph.append(mean)
		pointGraph = pointGraph + graph
		pointSet.append(graph)
		standardGraph.append(standard)
		standardPointGraph = standardPointGraph + standardG
		standardPointSet.append(standardG)
		dfa_ls.append(dfa_record)
	return meanGraph, pointGraph, pointSet, standardGraph, standardPointGraph, standardPointSet,dfa_ls

def single_posneg(choice0,choice1):
	generator.NUM_EXAMPLES = NUM_EXAMPLES
	generator.STR_LENGTH = STR_LENGTH
	positive,negative = generator.generator_uniform(choice0,choice1)
	print(len({**positive, **negative}))
	accuracyGraph =[]
	standardGraph = []
	dfa_record=[]
	for i in range(NUM_SIM):
		test_dfa = get_dfa(NUM_STATES,NUM_SYM)
		#get_dfa(NUM_STATES, NUM_SYM)
		accuratePos = test_accuracy(test_dfa, positive)
		accurateNeg = test_accuracy(test_dfa, negative)
		standard = test_accuracy(test_dfa, {**positive,**negative})
		accurateMul = (accuratePos * accurateNeg )**0.5 
		accuracyGraph.append( accurateMul)
		standardGraph.append( standard )
		dfa_record.append( (accurateMul,standard,test_dfa))
	return np.mean(accuracyGraph), accuracyGraph, np.mean(standardGraph), standardGraph, dfa_record


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
		if training_data[key] == dfa_tens.checkAccepting([int(i) for i in key]):
			correct += 1
		else:
			failed += 1
	return correct / (correct + failed)

def get_dfa(state_num, sym_num):
	'''
	Randomly generates a DFA with state_num states and sym_num symbols in its alphabet

	Returns
	-------
	TensorGenerator object (which is a DFA tensor)
	'''
	if "reachable" in info: 
		con = True
		while con:
			dfa = TensorGenerator.TensorGenerator(state_num, sym_num)
			con = not reachable.reachable(dfa.tensor,dfa.accept)
		return dfa
		reach = True
	else:
		return TensorGenerator.TensorGenerator(state_num, sym_num)
		reach = False

if __name__ == "__main__":
	#file = os.open("graph_log.txt",os.O_APPEND)
	mean, points, pointls, standard, standpt, standls,dfa_ls = sim_posneg()
	#textstr2 ="Test Number "+ str(record)+'\n '+' NUM_STATES = ' + str(NUM_STATES) + ' \n' + 'NUM_SYM = ' + str(NUM_SYM) + ' \n' + 'NUM_DFA = ' + str(NUM_SIM) + ' \n' + 'STR_LENGTH = ' + str(STR_LENGTH) + "\nSTR AMOUNT= "+str(NUM_EXAMPLES)+' \n' + 'Num Trail = ' + str(NUM_TRIAL)+ info+ " reachability? " + str(reach)
	#os.write(file,str.encode(textstr2))

	num_bins = 40
	plt.figure(0)
	n, bins, patches = plt.hist(mean, num_bins, facecolor='blue', alpha=0.5)
	title = 'Plot for Multiplicative Means for '+name+' DFA Run ' +str(record)+info
	plt.title(title)
	plt.xlabel('pos and neg accuracy') #approximately accurate threshold proportion of correctly classified DFAs
	plt.ylabel('proportion')
	#textstr = 'Constants'
	#textstr2 = 'NUM_Q_MIN = ' + str(NUM_Q_MIN) + ' \n' + 'NUM_DFA = ' + str(NUM_DFA) + ' \n' + 'NUM_STATES = ' + str(DfaSearchSim.NUM_STATES) + ' \n' + 'NUM_SYM = ' + str(DfaSearchSim.NUM_SYM) + ' \n' + 'NUM_EXAMPLES = ' + str(DfaSearchSim.NUM_EXAMPLES) + ' \n' + 'STR_LENGTH = ' + str(DfaSearchSim.STR_LENGTH) + ' \n' + 'NUM_SIM = ' + str(DfaSearchSim.NUM_SIM) + ' \n' + 'Q_MIN = ' + str(DfaSearchSim.Q_MIN) + ' \n'
	#plt.text(0.92, 0.8, textstr, fontsize=14, fontweight='bold', transform=plt.gcf().transFigure)
	#textstr = 'Constants'
	#plt.text(0.92, .3, textstr2, fontsize=14, transform=plt.gcf().transFigure)
	plt.savefig(title)
	plt.figure(1)
	n, bins, patches = plt.hist(points, num_bins, facecolor='purple', alpha=0.5)
	title = 'Plot for Multiplicative ALL for '+name+' DFA Run ' + str(record)+info
	plt.title(title)
	plt.xlabel('pos and neg accuracy') #approximately accurate threshold proportion of correctly classified DFAs
	plt.ylabel('proportion')
	plt.savefig(title)
	plt.figure(5)
	plt.plot(np.linspace(0, max(points), 100), kde.gaussian_kde(points)(np.linspace(0, 1, 100)))
	plt.title(title)
	plt.savefig(title)

	#############################################

	plt.figure(2)
	n, bins, patches = plt.hist(standard, num_bins, facecolor='red', alpha=0.5)
	title = 'Plot for Standard Means for '+name+' DFA Run ' +str(record)+info
	plt.title(title)
	plt.xlabel('standard accuracy') #approximately accurate threshold proportion of correctly classified DFAs
	plt.ylabel('proportion')
	#textstr = 'Constants'
	plt.savefig(title)


	plt.figure(3)
	n, bins, patches = plt.hist(standpt, num_bins, facecolor='green', alpha=0.5)
	title = 'Plot for Standard all for '+name+' DFA Run '+str(record)+info 
	plt.title(title)
	plt.xlabel('standard accuracy') #approximately accurate threshold proportion of correctly classified DFAs
	plt.ylabel('proportion')
	#textstr = 'Constants'
	plt.savefig(title)
	plt.figure(6)
	plt.title(title)
	plt.plot(np.linspace(0, max(points), 100), kde.gaussian_kde(standpt)(np.linspace(0, 1, 100)))
	plt.xlabel('standard accuracy')
	plt.ylabel('proportion')
	plt.show()
	
	#os.close(file)
