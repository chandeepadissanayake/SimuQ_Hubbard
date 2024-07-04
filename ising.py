"""Performs the simulation of the Ising model with equal interaction strength and external field strength over the
entire lattice. We rely on the classical QuTiP simulator merely for the convenience. Users can choose to utilize
other available vendors as necessary."""

__author__ = "Chandeepa Dissanayake"

import networkx as nx
from simuq import QSystem
from simuq import Qubit
from simuq.qutip import QuTiPProvider
import utils

# In our formulation, we assumed that all neighboring lattice sites have the same interaction strength J. We set J =
# 1 for simplicity.
J = 1
# Similarly, we have assumed that the external magnetic field (h) affects every lattice site equally. We also set h =
# 1 for simplicity.
h = 1

# Create a 3D 2x2 lattice. Note: Change this to 3x3 (or anything higher) and try with classical simulators to realize
# why we need quantum hardware ;)
G = nx.grid_graph(dim=(2, 2, 2))
# Time duration for evolution
T = 1

# Convert the lattice from a coordinate-based index to integer-based index system
G = nx.convert_node_labels_to_integers(G)
# Number of lattice sites in our system.
N = G.number_of_nodes()

# SimuQ Stuff
qs = QSystem()
q = [Qubit(qs) for _ in range(N)]

# Starts building the Hamiltonian. First loop builds the lattice-site interaction term whereas the second builds up
# external field interaction term. We consider all the edges(tubes) in the lattice(visualization), as they denote the
# nearest neighbour interactions.
H = 0
for i, j in G.edges():
    H += -J * q[i].Z * q[j].Z
# Loops over all lattice sites to add the external field interaction terms.
for i in range(N):
    H += -h * q[i].X

# SimuQ Stuff
qs.add_evolution(H, T)


qtpp = QuTiPProvider()
qtpp.compile(qs)
qtpp.run()
results = qtpp.results()

# Display the results; First all probabilities and then the probability of ground state It is evident that the state
# "000000" is the ground state, as flipping any qubit will result in an increment of the energy.
print(results)
print("Probability of obtaining the ground state {state}: {prob}".format(
    state="0" * N,
    prob=results["0" * N]
))

# Visualize the lattice structure in 3D.
utils.visualize_lattice(G, 3)
