"""Performs the simulation of the 1D Hydrogen Chain (Hubbard Model). We consider a chain with 5 Hydrogen atoms.

The values of z_t and z_u are set arbitrarily. Increase the time period for simulation as required. We rely on the
classical QuTiP simulator merely for the convenience. Users can choose to utilize other available vendors as
necessary.

IMPORTANT: Creator-Annihilator implementation in SimuQ Implementation has an apparent bug in it. Check the PR:
https://github.com/PicksPeng/SimuQ/pull/37. Incorporate the relevant changes in this PR to your installation of SimuQ
to fix."""

__author__ = "Chandeepa Dissanayake"

import networkx as nx
from simuq import QSystem, Fermion
import helpers
import utils


# The number of Hydrogen atoms in the chain.
N = 2
# The hopping integral. Taken to be positive.
z_t = 1
# Initial and Final values for On-site interaction strength. Can be either positive or negative.
# For further specifications on simulating a Hubbard system to evaluate phase changes:
z_u0 = -5
z_uf = 5
# Time duration for evolution
T = 4
# Number of discretization steps
M = 30

# Create the 1D Hydrogen Chain with N sites.
G = nx.Graph()
# Edges denote interactions between neighbouring sites. Since this is a chain, neighbours are right next to each
# other on 1D plane.
G.add_edges_from([(i + 1, i + 2) for i in range(N - 1)])
# Convert the lattice from a coordinate-based index to integer-based index system
G = nx.convert_node_labels_to_integers(G)

# SimuQ Stuff
qs = QSystem()
# We need 2N Fermions as each site can have 1 spin-up fermion and 1 spin-down fermion.
f = [Fermion(qs) for _ in range(2 * N)]

# Starts building the Hamiltonian.
H_t = 0
H_u = 0
for i, j in G.edges():
    i_up, i_down = f[i * 2], f[(i * 2) + 1]
    j_up, j_down = f[j * 2], f[(j * 2) + 1]

    H_t += (i_up.c * j_up.a + j_up.c * i_up.a) + (i_down.c * j_down.a + j_down.c * i_down.a)
    H_u += i_up.c * i_up.a * i_down.c * i_down.a

# Build the Time Dependent Hamiltonian
H = lambda t: -z_t * H_t + ((1 - t / T) * z_u0 + (t / T) * z_uf) * H_u

# Simulate the Hamiltonian H over time period T using QuTiP simulator
results = helpers.simulate_on_qutip(qs, H, T, time_dependent=True, M=M)
# Print the results in general format.
helpers.print_simulator_results(results, 2 * N)

# Visualize the lattice structure in 3D.
utils.visualize_lattice(G, 1)
