"""
File name: SIRV_simulator.py
Description: This file contains the main function used for driving a simulation,
    "SIRV_cluster_simulator", along helper functions for the simulator
Author: Chris VanKerkhove
"""
import math
import numpy as np
import random
from classes import State, Agent


#Helper Functions for the Simulator
def infect_entity(sim_state, key):
    """
    Helper function for the simulator that executes the process for
    infecting a given class. NO return value, class variables are updated

    Arg(s):
        sim_state: An instance of class State
        key: String representation of the entitie's class
    """
    i = np.random.randint(0, len(sim_state.S[key]))
    ent = sim_state.S[key].pop(i)
    sim_state.infected.append(ent)
    #urv for if the patient shows symptoms or not
    prob = np.random.uniform()
    #patient is symptomatic
    if prob < sim_state.p[key]:
        ent.state = 'I_s'
        sim_state.I_sym.append(ent)
        sim_state.V[key].remove(ent)
        sim_state.V_tot.remove(ent)
    #patient is assymptomatic
    else:
        ent.state = 'I_a'
        sim_state.I[key].append(ent)

def calculate_rate(sim_state, key):
    """
    Calculates the rate of infection across a given class
    Arg(s):
        sim_state: an instance of class State
        key: String representation of the entitie's class
    Returns:
        Rates for C1, C2, C3, C4, β_tot (respectively)
    """
    ###Ways for C1 to get infected
    #number of (key,1) pairs
    n_pair_1 = len(sim_state.S[key]) * len(sim_state.I['C1'])
    #number of (key,2) pairs
    n_pair_2 = len(sim_state.S[key]) * len(sim_state.I['C2'])
    #number of (key,3) pairs
    n_pair_3 = len(sim_state.S[key]) * len(sim_state.I['C3'])
    #number of (key,4) pairs
    n_pair_4 = len(sim_state.S[key]) * len(sim_state.I['C4'])
    #number of pairs with C1 and symptomatic people
    n_pair_1a = len(sim_state.S['C1']) * len(sim_state.I_sym)

    #populating the rates according to the number of pairs of people
    n = int(key[1]) - 1
    #infection rate on key from class 1
    λ_1 = sim_state.λ[n][0]
    #infection rate on key from class 2
    λ_2 = sim_state.λ[n][1]
    #infection rate on key from class 3
    λ_3 = sim_state.λ[n][2]
    #infection rate on key from class 4
    λ_4 = sim_state.λ[n][3]
    λ_1a = sim_state.λ_s


    #rate that the class key is infected
    λ_key = λ_1 * n_pair_1 + λ_2 * n_pair_2 + λ_3 * n_pair_3 + λ_4 * n_pair_4 + (λ_1a * n_pair_1a * (key == 'C1'))

    return λ_key


###SIMULATOR:
def SIRV_cluster_simulator(T,infect, λ, λ_s, β, n, p, λ_v, n_v):
    """
    Simulates an epidemic clustered with the functionality of vaccinations
    over a arbitrary time range

    Arg(s):
        T: Amount of time to simulate over
        infect: String input that is the class of the infected entity
        λ: meet rate 2x2 matrix
        λ_s: meet rate for symptomatic and C1
        beta: recovery rate
        n: dict of the size of each class
        p: dict of probabilities an infected agent is symptomatic
        λ_v: rate a vaccination event happens
        n_v: the number of people in a group that are vaccinated during a vaccination event (default is one)

    """
    #initializing the state of the system based on the inputs
    sim_state = State(λ, λ_s, β, n, p, λ_v, n_v)

    for key, value in n.items():
        for i in range(n[key]):
            agent = Agent(key)
            sim_state.S[key].append(agent)
            sim_state.V[key].append(agent)
            sim_state.V_tot.append(agent)
            if key == 'C1':
                sim_state.medical_class.append(agent)
            elif key == 'C2':
                sim_state.essential_nm.append(agent)
            elif key == 'C3':
                sim_state.high_risk_ne.append(agent)
            else:
                sim_state.low_risk_ne.append(agent)

    #infecting a single person of classs 'infect'
    ent = sim_state.S[infect].pop(0)
    ent.state = 'I_a'
    sim_state.I[infect].append(ent)
    sim_state.infected.append(ent)

    count = 0
    while count < T:
        #retrieving rate values across classes
        λ_C1 = calculate_rate(sim_state, 'C1')
        λ_C2 = calculate_rate(sim_state, 'C2')
        λ_C3 = calculate_rate(sim_state, 'C3')
        λ_C4 = calculate_rate(sim_state, 'C4')
        #total recovery rate
        β_tot = β * (len(sim_state.I['C1']) + len(sim_state.I_sym) + len(sim_state.I['C2']) + \
                                         len(sim_state.I['C3']) + len(sim_state.I['C4']))
        #total vaccination rate
        if len(sim_state.V_tot) > 0:
            λv_tot = (λ_v/ n_v)
        else:
            λv_tot = 0

        λ_tot = λ_C1 + λ_C2 + λ_C3 + λ_C4 + β_tot + λv_tot

        #case if virus is erradicated
        if λ_tot == 0:
            break

        λ_rand = np.random.exponential(1/λ_tot)
        count += λ_rand
        U = np.random.uniform()

        ###CASE 1: A susceptible person from C1 is infected
        if U < λ_C1 / λ_tot:
            infect_entity(sim_state, 'C1')

        ###CASE 2: A susceptible person from C2 is infected
        elif U < (λ_C1 + λ_C2) / λ_tot:
            infect_entity(sim_state, 'C2')

        ###CASE 3: A susceptible person from C3 is infected
        elif U < (λ_C1 + λ_C2 +λ_C3) / λ_tot:
            infect_entity(sim_state, 'C3')

        ###CASE 4: A susceptible person from C4 is infected
        elif U < (λ_C1 + λ_C2 +λ_C3+ λ_C4) / λ_tot:
            infect_entity(sim_state, 'C4')

        ###Case 5: An entity (or batch) is vaccinated
        elif U < (λ_C1 + λ_C2 + λ_C3 + λ_C4 + λv_tot) / λ_tot:
            #all people available for vaccination
            n = min(n_v, len(sim_state.V_tot))
            for i in range(n):
                i = np.random.randint(0, len(sim_state.V_tot))
                ent = sim_state.V_tot.pop(i)
                sim_state.V[ent.C].remove(ent)
                if ent in sim_state.S[ent.C]:
                    sim_state.S[ent.C].remove(ent)
                    ent.state = "R_v"
                else:
                    sim_state.I[ent.C].remove(ent)
                    sim_state.infected.remove(ent)
                    ent.state = 'R'
                sim_state.R.append(ent)


        ###Case 6: A person recovers
        else:
            i = np.random.randint(0, len(sim_state.infected))
            ent = sim_state.infected.pop(i)
            sim_state.R.append(ent)
            #if the recovered person is from assymptomatic
            if ent.state == 'I_a':
                sim_state.I[ent.C].remove(ent)
                sim_state.V[ent.C].remove(ent)
                sim_state.V_tot.remove(ent)
            #if the recovered person is symptomatic
            else:
                sim_state.I_sym.remove(ent)
            ent.state = 'R'

        #recording data
        sim_state.times.append(count)
        sim_state.num_inf.append(len(sim_state.infected))
        #counting infected showing symptoms for all classes
        C1 = sim_state.n['C1'] - (len(sim_state.S['C1']))
        C2 = sim_state.n['C2'] - (len(sim_state.S['C2']))
        C3 = sim_state.n['C3'] - (len(sim_state.S['C3']))
        C4 = sim_state.n['C4'] - (len(sim_state.S['C4']))

        for ent in sim_state.R:
            if ent.C == 'C1':
                C1 -= 1
            elif ent.C == 'C2':
                C2 -= 1
            elif ent.C == 'C3':
                C3 -= 1
            else:
                C4 -= 1

        sim_state.C1_inf.append(C1)
        sim_state.C2_inf.append(C2)
        sim_state.C3_inf.append(C3)
        sim_state.C4_inf.append(C4)

    return sim_state
