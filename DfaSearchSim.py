'''Contains functions to Monte Carlo sample DFAs to investigate what proportion approximate the true DFA'''
import TensorGenerator
import random
import AcceptingStringGenerator
import numpy as np
import CompareDFAGenerator as cdg

NUM_STATES = 5 # number of states in target DFA (and randomly sampled test DFAs)
NUM_SYM = 2 # number of symbols in alphabet of language accepted DFAs in search space
NUM_EXAMPLES = 500 # number of training examples (WARNING: might not work as intended if this is odd)
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
    dfa = TensorGenerator.TensorGenerator(state_num, sym_num)

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
    print(target_tens.tensor)

    # MAKE SURE DFA ACCEPTS SOMETHING
    # tensor_success = False
    # while tensor_success is False:
    #     if (list(test_data.values()).__contains__(True)):
    #         tensor_success = True
    #     else:
    #         target_tens = get_dfa(NUM_STATES, NUM_SYM)
    #         test_data = get_examples(target_tens)


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

    target_tens = get_dfa(NUM_STATES, NUM_SYM) # Randomly generate a target DFA, from which we will get training data
    test_data = get_examples(target_tens)
    #test_data = generator() # TODO uncomment if you want divisibility-by-5 target DFA. Can also change generator function to be divisibility-by-[any number]

    accuracy_l = []

    for i in range(num_test_dfa):
        test_dfa = get_dfa(NUM_STATES, NUM_SYM)
        accuracy = standard_accuracy(test_dfa, test_data)
        accuracy_l.append(accuracy)

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