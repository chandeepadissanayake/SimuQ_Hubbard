from simuq import QSystem
from simuq import Qubit
from simuq.qutip import QuTiPProvider
import numpy as np

n_qubits = 2
qs = QSystem()
q1, q2 = Qubit(qs), Qubit(qs)

J = 1
U_0 = -5
U_f = 5

T = 4
M = 30

H = lambda t: -J * (q1.X + q2.X) + ((1 - t / T) * U_0 + (t / T) * U_f) * (q1.Z * q2.Z)
qs.add_td_evolution(H, np.linspace(0, T, M))

qpp = QuTiPProvider()
qpp.compile(qs)
qpp.run()
print(qpp.results())
