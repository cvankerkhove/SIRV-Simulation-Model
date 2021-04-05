"""
File name: classes.py
Description: This file contains the class constructors for class "State" and
    "Agent." These classes are using for storing information about the State of a
    given simulation.
Author: Chris VanKerkhove
"""

class State:
    #This class provides useful class variables for storing information
    #about a simulation
    def __init__(self, λ, λ_s, β, n, p, λ_v, n_v):
        #list of agents in classes C1, C2, C3, C4 respectively:
        #medical workers
        self.medical_class = []
        #essential non-medical workers
        self.essential_nm = []
        #non-essential high-risk
        self.high_risk_ne = []
        #non-essential low-risk
        self.low_risk_ne = []
        #dictionary with each item containing a list of susceptible entities across classes
        self.S = {'C1': [], 'C2': [], 'C3': [], 'C4': []}
        #dictionary with each item containing a list of infected entities across classes
        self.I = {'C1': [], 'C2':[], 'C3': [], 'C4': []}
        #dictionary with each item containing a list of entities available for vaccination
        self.V = {'C1': [], 'C2': [], 'C3': [], 'C4': []}

        #Infected symptomatic across all classes
        self.I_sym = []
        #recovered across all classes
        self.R = []
        #Total agents infected
        self.infected = []
        #Total agents available for Vaccination
        self.V_tot = []
        #times when vaccination ovccurs
        self.vac_time = []

        #dict of probabilities an infected agent is symptomatic
        #{'C1': 0, 'C2': 0, 'C3', 0, 'C4': 0}
        self.p = p
        #dict of the size of each class
        #{'C1': 0, 'C2': 0, 'C3', 0, 'C4': 0}
        self.n = n
        #meet rate matrix
        self.λ = λ
        #sympotic meet rate with medical works
        self.λ_s = λ_s
        #recovery rate
        self.β = β
        #vaccination rate
        self.λ_v = λ_v
        #number of people in a group vaccinated for each arrival
        self.n_v = n_v

        #lists for recording data at events
        self.times = []
        self.num_inf = []
        self.C1_inf = []
        self.C2_inf = []
        self.C3_inf = []
        self.C4_inf = []
        self.int_time = []

class Agent:
    #this class is required for keeping track of unique entities through the sim.
    def __init__(self, c):
        """
        Arg(s):
            c: string representation of this class type
        """
        #string representation of the state of the person ('S', 'I_a', 'I_s', 'R')
        self.state = 'S'
        self.C = c
