'''
Contains functions to generate strings that are accepted by a DFA.
These strings will then be used to train and test a DFA learner

*** RIGHT NOW THERE IS A BUG WHERE THE STRINGS ARE NOT THE CORRECT LENGTHS
'''

STRING_LENGTH = 2 # length of accepting strings to generate # TODO should I make this MAX_LENGTH? (max string length)

def get_strings(tensor, acc_state, str_len):
    '''
    Parameters
    ----------
    tensor: tensor attribute of object of TensorGenerator class
      tensor representation of DFA
    init_state: int
      initial state (also index of initial state)
    acc_state: int
      accepting state (also index of accepting state)
    str_len: int
      size of walk, which is the length of strings that will be generated

    Returns
    -------
    set of walks from initial state 0 to acc_state with str_len edges # TODO change to actual walks

    Warnings
    --------
    Assume initial state is 0
    '''
    init_state = 0
    num_states = len(tensor[0]) # number of states in the DFA
    alphabet_size = len(tensor) # number of symbols in alphabet

    # Initialize table to be filled up using DP. The value string_table[source][dest][e] will
    # store the possible walks from source to dest with exactly e edges
    string_table = [[[set()] * (str_len + 1)] * num_states] * num_states
    print(string_table)

    for e in range(str_len + 1): # Loop for number of state transitions from 0 to str_len
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
                                print(str_l)
                                for string in str_l.copy():
                                    print(string + str(sym))
                                    string_table[source][dest][e].add(string + str(sym))

    return string_table[init_state][acc_state][str_len]


def count_wrapper(dfa_tensor):
    for accepting_state in dfa_tensor.accept:  # Find strings for every possible accepting state
        # COULD DO-- for i in range(self.MAX_LENGTH): # Find strings of every possible length up to MAX_LENGTH
        strings = get_strings(dfa_tensor.tensor, accepting_state, STRING_LENGTH)
        print(strings)  # TODO change to actual strings instead of number of strings
