import matplotlib.pyplot as plt
import DfaSearchSim
from os import listdir

NUM_Q_MIN = 20
NUM_DFA = 10

def run_thresholdacc_sim():
    '''
    Wrapper function to run Monte Carlo simulation with different threshold accuracies (q_min)
    Could expand to vary more than just parameter q_min
    '''
    q_min_l = []
    approx_dfa_l = []

    for i in range(NUM_Q_MIN):
        q_min = i/NUM_Q_MIN
        DfaSearchSim.Q_MIN = q_min
        q_min_l.append(q_min)
        dfaSum = 0
        for j in range(NUM_DFA):
            dfaSum += DfaSearchSim.sim()
        dfaSum = dfaSum/NUM_DFA
        approx_dfa_l.append(dfaSum)
        print(i)

    return q_min_l, approx_dfa_l


if __name__ == "__main__":
    
#    q_min_l, approx_dfa_l = run_thresholdacc_sim()
#    plt.scatter(q_min_l, approx_dfa_l)
#    plt.title('Proportion of Randomly-Sampled DFAs that are Approximately Accurate')
#    plt.xlabel('q_min') #approximately accurate threshold proportion of correctly classified DFAs
#    plt.ylabel('approximately accurate proportion')
#    textstr = 'Constants'
#    textstr2 = 'NUM_Q_MIN = ' + str(NUM_Q_MIN) + ' \n' + 'NUM_DFA = ' + str(NUM_DFA) + ' \n' + 'NUM_STATES = ' + str(DfaSearchSim.NUM_STATES) + ' \n' + 'NUM_SYM = ' + str(DfaSearchSim.NUM_SYM) + ' \n' + 'NUM_EXAMPLES = ' + str(DfaSearchSim.NUM_EXAMPLES) + ' \n' + 'STR_LENGTH = ' + str(DfaSearchSim.STR_LENGTH) + ' \n' + 'NUM_SIM = ' + str(DfaSearchSim.NUM_SIM) + ' \n' + 'Q_MIN = ' + str(DfaSearchSim.Q_MIN) + ' \n'
#    plt.text(0.92, 0.8, textstr, fontsize=14, fontweight='bold', transform=plt.gcf().transFigure)
#    textstr = 'Constants'
#    plt.text(0.92, .3, textstr2, fontsize=14, transform=plt.gcf().transFigure)
    
    # Make 1-d histogram of actual accuracies of test DFAs
    accuracy_l = DfaSearchSim.sim2()
    plt.hist(accuracy_l)
    
#    plt.figure(figsize = (10, 4.8))
#    i = 1
#    while i != -1:
#        print(listdir())
#        if 'dfaGraph' + str(i) + '.jpg' not in listdir():
#            plt.savefig('dfaGraph'+ str(i)+ '.jpg')
#            i = -1
#        else: i += 1