from simuq import QSystem
from simuq import Qubit
from simuq.qutip import QuTiPProvider
# from simuq.ibm.ibm_provider import IBMProvider

n_qubits = 2
qs = QSystem()
q1, q2 = Qubit(qs), Qubit(qs)

J = 4
U = 3

T = 10

H = -J * (q1.X + q2.X) + U * (q1.Z * q2.Z)
qs.add_evolution(H, T)

qpp = QuTiPProvider()
qpp.compile(qs)
qpp.run()
print(qpp.results())
