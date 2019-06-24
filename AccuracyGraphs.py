import matplotlib.pyplot as plt
import DfaSearchSim
from os import listdir
import scipy.stats as st
from statsmodels.stats.proportion import proportion_confint
import numpy as np

NUM_Q_MIN = 40
NUM_DFA = 10


def run_sim():
    '''
    Wrapper function to run Monte Carlo simulation with different threshold accuracies (q_min)
    Could expand to vary more than just parameter q_min
    '''
    q_min_l = []  # list to keep track of threshold accuracy
    low_bound_l = []
    mean_l = []
    up_bound_l = []  # list of DFAs that approximate a target DFA within q_min accuracy
    
    for i in range(NUM_Q_MIN + 1):
        q_min = i / NUM_Q_MIN  # normalize to be a proportion between 0 and 1
        DfaSearchSim.Q_MIN = q_min  # set value of Q_MIN in simulation module
        q_min_l.append(q_min)
        
        temp_prop_l = []
        for j in range(NUM_DFA):
            temp_prop_l.append(DfaSearchSim.sim())
        
        
        # print marker to see progress of program
        print("--------------------------------------")
        print("	Q min  " + str(i))
        print("--------------------------------------")
    
        mu = np.mean(temp_prop_l)
        conf_int = st.t.interval(0.95, len(temp_prop_l)-1, loc=mu, scale=st.sem(temp_prop_l))
        
        low_bound_l.append(conf_int[0])
        mean_l.append(mu)
        up_bound_l.append(conf_int[1])
    
    return q_min_l, low_bound_l, mean_l, up_bound_l


if __name__ == "__main__":
     # UNCOMMENT IF YOU WANT 1-D HISTOGRAM OF ACTUAL ACCURACIES OF TEST DFA (PDF)
     accuracy_l = DfaSearchSim.sim2()
     plt.hist(accuracy_l, density=True)
     kde = st.gaussian_kde(accuracy_l, bw_method='silverman')
     plt.plot(np.linspace(0, 1, 100), kde(np.linspace(0, 1, 100)))

#    # UNCOMMENT IF YOU WANT PLOT OF Q_MIN VS # TEST DFA W/ ACCURACY > Q_MIN (CDF)
#    # actual plotting (this is all you really need)
#    q_min_l, low_bound_l, mean_l, up_bound_l = run_sim()
#    
#    plt.plot(q_min_l, low_bound_l)
#    plt.plot(q_min_l, mean_l)
#    plt.plot(q_min_l, up_bound_l)
##    error1 = [proportion_confint(approx_dfa_l[i]*DfaSearchSim.NUM_SIM, DfaSearchSim.NUM_SIM, alpha=0.05, method='normal') for i in range(NUM_Q_MIN+1)]
##    error = [(conf_int[1] - conf_int[0])/2 for i, conf_int in enumerate(error1)]
##    plt.errorbar(q_min_l, approx_dfa_l, yerr=error)
#
#    # add axes labels and title
#    plt.title('Proportion of Randomly-Sampled DFAs that are Approximately Accurate')
#    plt.xlabel('q_min') #approximately accurate threshold proportion of correctly classified DFAs
#    plt.ylabel('approximately accurate proportion')
#
#    # add sidebar showing the values of relevant constants
#    textstr = 'Constants'
#    textstr2 = 'Number of q_min tested: ' + str(NUM_Q_MIN) + ' \n' + \
#               'Number of states in DFA: ' + str(DfaSearchSim.NUM_STATES) + ' \n' + \
#               'Cardinality of alphabet: ' + str(DfaSearchSim.NUM_SYM) + ' \n' + \
#               'Number of test examples: ' + str(DfaSearchSim.NUM_EXAMPLES) + ' \n' + \
#               'Length of test examples: ' + str(DfaSearchSim.STR_LENGTH) + ' \n' + \
#               'Number of simulations per graph point: ' + str(DfaSearchSim.NUM_SIM) # 'Points per q_min: ' + str(NUM_DFA) + ' \n' + \
#    plt.text(0.92, 0.8, textstr, fontsize=14, fontweight='bold', transform=plt.gcf().transFigure)
#    plt.text(0.92, .3, textstr2, fontsize=14, transform=plt.gcf().transFigure)


    # # THIS IS KYLE'S CODE. IT IS NOT COMPATIBLE WITH THE CURRENT run_sim FUNCTION
    # plt.figure(1)
    # plt.scatter(individual_dis[20][0], individual_dis[20][1])
    # plt.title('distribution for a specific q_min')
    # plt.xlabel('q_min') #approximately accurate threshold proportion of correctly classified DFAs
    # plt.ylabel('approximately accurate proportion')
    # plt.show()


    # # JUST NEVER UNCOMMENT THIS. :)
    # plt.figure(figsize = (10, 4.8))
    # i = 1
    # while i != -1:
    # 	print(listdir())
    # 	if 'dfaGraph' + str(i) + '.jpg' not in listdir():
    # 		plt.savefig('dfaGraph'+ str(i)+ '.jpg')
    # 		i = -1
    # 	else: i += 1
