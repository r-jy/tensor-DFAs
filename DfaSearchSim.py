'''Contains functions to Monte Carlo sample DFAs to investigate what proportion approximate the true DFA'''
import TensorGenerator
import random
import AcceptingStringGenerator
import numpy as np

NUM_STATES = 5 # number of states in target DFA (and randomly sampled test DFAs)
NUM_SYM = 2 # number of symbols in alphabet of language accepted DFAs in search space
NUM_EXAMPLES = 100 # number of training examples (WARNING: might not work as intended if this is odd)
STR_LENGTH = AcceptingStringGenerator.STRING_LENGTH # length of strings in training data
NUM_SIM = 100 # number of random DFAs to test on training data
Q_MIN = .3 # proportion of strings in training data that must be correctly classified as acccepting or rejecting for a DFA to be considered approximately correct


# 1. Randomly generate DFA and training data
# TODO check connectivity

def get_dfa(state_num, sym_num):
    '''
    Randomly generates a DFA with state_num states and sym_num symbols in its alphabet

    Returns
    -------
    TensorGenerator object (which is a DFA tensor)
    '''
    return TensorGenerator.TensorGenerator(state_num, sym_num)


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
    training_data = {}

    # Generate NUM_EXAMPLES/2 random strings
    # We're assuming these will probably not be accepted so we'll have a 50/50 dist acc/rej strings
    for datum in range(NUM_EXAMPLES//2):
        # Randomly generate string
        datum_str = ''
        for i in range(STR_LENGTH):
            datum_str += str(random.randint(0,NUM_SYM-1)) # make a list of characters to test
        accepted = target_tens.checkAccepting([int(i) for i in datum_str])
        training_data[datum_str] = accepted

    # Generate NUM_EXAMPLES/2 accepted strings
    accepted_str = AcceptingStringGenerator.count_wrapper(target_tens)
    if len(accepted_str) > 0:
        for datum in range(NUM_EXAMPLES//2):
            datum_str = random.choice(accepted_str)
            training_data[datum_str] = True

    return training_data


# 2. Randomly sample DFAs and test whether it accepts training data


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


def generator():
    sampleSet = {}
    numSample = NUM_EXAMPLES
    while len(sampleSet) < numSample:

        sample = tuple([np.random.randint(2) for i in range(np.random.randint(STR_LENGTH))])

        if len(sample) > 0:
            s = "".join(map(str, sample))
            result = int(int(s, 2) % 5 == 0)
        else:
            s = ''
            result = 1

        sampleSet[s] = result

    return sampleSet


def sim():
    '''
    Returns proportion of DFAs with n or fewer states that are approximately
    correct (within Q_MIN accuracy)
    '''

    target_tens = get_dfa(NUM_STATES, NUM_SYM) # Randomly generate a target DFA, from which we will get training data
    training_data = get_examples(target_tens)
    #training_data = generator() # TODO uncomment if you want divisibility-by-5 target DFA. Can also change generator function to be divisibility-by-[any number]

    accurate = 0
    inaccurate = 0

    for i in range(NUM_SIM):
        test_dfa = get_dfa(NUM_STATES, NUM_SYM)
        accuracy = test_accuracy(test_dfa, training_data)

        if accuracy >= Q_MIN: accurate += 1
        else: inaccurate += 1

    return accurate/(accurate + inaccurate)

