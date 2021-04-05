"""
File name: sanbox.py
Description: This file can be directly run to execute a simulation with modifiable
    inputs (the first variables shown below). When run, a graph displaying the
    state of the simulation will also be displayed.
Author: Chris VanKerkhove
"""
from SIRV_simulator import SIRV_cluster_simulator
import matplotlib.pyplot as plt
import time
#Animation
from IPython import display

#time period to simulate over
T = 1000000000
#high meeting rate
h = 1.32
#low meeting rate
l = 0.32
#rate matrix of 4 classes (must be symmetric)
λ = [[h,h,l,l],[h,h,h,h],[l,h,l, l], [l,h,l,l]]
#meet rate symptomatic entities have with C1 (medical)
λ_s = 1
#rate of recovery
β = 3.64
#number of entities in each class
n = {'C1': 16, 'C2': 16 , 'C3': 16, 'C4': 275}
#probability an entity becomes symptomatic when infected
p = {'C1': 0.8, 'C2': 0.65, 'C3': 0.65, 'C4': 0.60}
#vaccination rate
λ_v = 500
#vaccination batch size i.e. how many people are being vaccinated during a single vaccination event
n_v = 50



sim = SIRV_cluster_simulator(T,'C2', λ, λ_s, β, n, p, λ_v, n_v = n_v)
#list of event times
t = sim.times
#list of total infected at each event time
inf_tot = sim.num_inf
#list of infection over time for all Classes
C1 = sim.C1_inf
C2 = sim.C2_inf
C3 = sim.C3_inf
C4 = sim.C4_inf

#total Number of Entities that got sick
vac = 0
class_inf = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
for ent in sim.R:
    if ent.state == 'R_v':
        vac -= 1
    else:
        class_inf[ent.C] += 1
print('Total Amount of entities that got infected across simulation: ', len(sim.R) + vac)
print('Amount of C1 entities that got infected across simulation: ', class_inf['C1'])
print('Amount of C2 entities that got infected across simulation: ', class_inf['C2'])
print('Amount of C3 entities that got infected across simulation: ', class_inf['C3'])
print('Amount of C4 entities that got infected across simulation: ', class_inf['C4'])


###Code for Live Code of Simulation###
for i in range(0, len(t), 5):
  display.clear_output(wait=True)

  plt.plot(t[0:i], inf_tot[0:i])
  plt.plot(t[0:i], C1[0:i], color='orange')
  plt.plot(t[0:i], C2[0:i], color='green')
  plt.plot(t[0:i], C3[0:i], color='red')
  plt.plot(t[0:i], C4[0:i], color='purple')

  plt.title('All Classes')
  plt.xlabel('Event Times')
  plt.ylabel('Infection Count')

  plt.show()
  time.sleep(0)
