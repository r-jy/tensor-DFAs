import matplotlib.pyplot as plt
import DfaSearchSim

NUM_Q_MIN = 100

def run_sim():
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
        approx_dfa_l.append(DfaSearchSim.sim())

    return q_min_l, approx_dfa_l


if __name__ == "__main__":
    q_min_l, approx_dfa_l = run_sim()
    a = plt.scatter(q_min_l, approx_dfa_l)
    plt.title('Proportion of Randomly-Sampled DFAs that are Approximately Accurate on Training Data')
    plt.xlabel('approximately accurate threshold proportion of correctly classified DFAs')
    plt.ylabel('proportion of DFAs that are approximately accurate')