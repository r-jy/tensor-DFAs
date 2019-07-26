'''
Contains functions to generate strings that are accepted by a DFA.
These strings will then be used to train and test a DFA learner

Note that we are assuming it is okay to cap the length of the strings.
This makes sense practically, but Angluin suggested in her passive
learning paper that it might not be.

Ask Kate if you have questions :)
'''
import copy
from numpy import random

global STRING_LENGTH
STRING_LENGTH = 11 # length of accepting strings to generate # TODO should I make this MAX_LENGTH? (max string length)

def get_strings(tensor, str_len):
    '''
    Parameters
    ----------
    tensor: tensor attribute of object of TensorGenerator class
      tensor representation of DFA
    str_len: int
      size of walk, which is the maximum length of strings that will be generated

    Returns
    -------
    set of walks from initial state 0 to acc_state with str_len edges

    Warnings
    --------
    Assume initial state is 0
    '''
    num_states = len(tensor[0]) # number of states in the DFA
    alphabet_size = len(tensor) # number of symbols in alphabet

    # Initialize table to be filled up using DP. The value string_table[source][dest][e] will
    # store the possible walks from source to dest with exactly e edges
    cell_content = set()
    row = [copy.deepcopy(cell_content) for i in range(str_len + 1)]
    matrix = [copy.deepcopy(row) for i in range(num_states)]
    string_table = [copy.deepcopy(matrix) for i in range(num_states)]

    # Now fill in table
    for e in range(str_len + 1): # Loop for number of state transitions from 0 to str_len#
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

def count_wrapper(dfa_tensor):
    '''Return a list of all STRING_LENGTH accepting strings for dfa_tensor

    Parameters
    ----------
    dfa_tensor: TensorGenerator object
      tensor for which to find accepting strings

    Returns
    -------
    list of accepting strings of length STRING_LENGTH
    '''
    string_table = get_strings(dfa_tensor.tensor, STRING_LENGTH)
    strings = [string for accept_state in dfa_tensor.accept for string in string_table[0][accept_state][STRING_LENGTH]]

    # for accepting_state in dfa_tensor.accept:  # Find strings for every possible accepting state # TODO Hardcoded {4,5,6} # dfa_tensor.accept {0,1}
    #     strings.extend(string_table[0][accepting_state][STRING_LENGTH])
    return strings


def count_wrapper2(dfa_tensor, str_length = STRING_LENGTH):
    string_table = get_strings(dfa_tensor.tensor, str_length)
    strings = [string for accept_state in dfa_tensor.accept for length in range(str_length) for string in string_table[0][accept_state][length]]
    # for accepting_state in dfa_tensor.accept:  # Find strings for every possible accepting state # TODO Hardcoded {4,5,6} # dfa_tensor.accept {0,1}
    #     tens = dfa_tensor.tensor # TODO hardcoded dfa_tensor.tensor [[[0, 1, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 0, 1], [0, 0, 1]]]
    #     for length in range(str_length):
    #         for string in get_strings(tens, accepting_state, length):
    #             strings.append(string)
    return strings

if __name__ == "__main__":
    import TensorGenerator
    a = TensorGenerator.TensorGenerator(2, 3)
    b = count_wrapper(a)
