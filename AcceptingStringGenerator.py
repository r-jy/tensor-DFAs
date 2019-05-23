'''
Contains functions to generate strings that are accepted by a DFA.
These strings will then be used to train and test a DFA learner

*** RIGHT NOW PROGRAM GENERATES NUMBER OF STRINGS, NOT STRINGS THEMSELVES
'''

STRING_LENGTH = 1 # length of accepting strings to generate # TODO should I make this MAX_LENGTH? (max string length)

def count_walks(symbol_adj_matrix, init_state, acc_state, str_len):
    '''
    Parameters
    ----------
    symbol_adj_matrix: element of tensor attribute of object of TensorGenerator class
      adjacency matrix representation of DFA states and transitions for one symbol in alphabet
    init_state: int
      initial state (also index of initial state)
    acc_state: int
      accepting state (also index of accepting state)
    str_len: int
      size of walk, which is the length of strings that will be generated

    Returns
    -------
    int number of walks from init_state to acc_state with str_len edges # TODO change to actual walks
    '''
    num_states = len(symbol_adj_matrix) # number of states in the DFA

    # Initialize table to be filled up using DP. The value count[source][dest][e] will
    # store count of possible walks from source to dest with exactly e edges
    count = [[[0] * (str_len + 1)] * num_states] * num_states

    for e in range(str_len + 1): # Loop for number of state transitions from 0 to str_len
        for source in range(num_states):  # for source
            for dest in range(num_states):  # for destination

                # from base cases
                if (e == 0) and (source == dest):
                    count[source][dest][e] = 1
                if (e == 1) and (symbol_adj_matrix[source][dest] == 1):
                    count[source][dest][e] = 1

                # go to adjacent only when number of edges is more than 1
                if e > 1:
                    for a in range(num_states):  # adjacent of source state
                        if symbol_adj_matrix[source][a]:  # if there is a transition from source state to a^th state
                            count[source][dest][e] += count[a][dest][e - 1]

    return count[init_state][acc_state][str_len]


def count_wrapper(dfa_tensor):
    for sym in range(dfa_tensor.symbol):  # Do this for every transition symbol in the alphabet
        for accepting_state in dfa_tensor.accept:  # Find strings for every possible accepting state
            # COULD DO-- for i in range(self.MAX_LENGTH): # Find strings of every possible length up to MAX_LENGTH
            num_walks = count_walks(dfa_tensor.tensor[sym], 0, accepting_state, STRING_LENGTH)
            print(num_walks)  # TODO change to actual strings instead of number of strings
