import numpy as np

from time import time

from qiskit import IBMQ, Aer
from qiskit.circuit import QuantumCircuit, ParameterVector
from qiskit.circuit.library import EfficientSU2, RealAmplitudes
from qiskit.opflow import QFI, StateFn, PauliExpectation, CircuitSampler

from surfer.qfi import OverlapQFI, ReverseQFI

num_qubits = 27
coupling_map = [
    (0, 1), (4, 7), (10, 12), (15, 18), (21, 23), (24, 25),
    (22, 19), (16, 14), (11, 8), (5, 3),
] + [
    (1, 4), (7, 6), (12, 13), (18, 17), (23, 24), (25, 26),
    (19, 20), (14, 11), (8, 9), (3, 2)
] + [
    (7, 10), (12, 15), (18, 21), (25, 22), (19, 16),
    (13, 14), (8, 5), (2, 1)
]
reps = 1

circuit = RealAmplitudes(num_qubits=10, reps=reps, entanglement="pairwise").decompose()
# circuit = RealAmplitudes(num_qubits, reps=reps, entanglement=coupling_map).decompose()

parameters = circuit.parameters
values = np.zeros(circuit.num_parameters)

for i in range(circuit.num_qubits):
    values[~i] = np.pi / 2

# start = time()
# qfi = ReverseQFI(do_checks=False).compute(circuit, values)
# time_taken = time() - start

# print(time_taken)
# print(qfi)

start = time()
qfi = OverlapQFI(clifford=True).compute(circuit, values)
time_taken = time() - start

print(time_taken)
print(qfi)
# np.save("qfi_cliff_realamp_plus_kolkata.npy", qfi)
# np.save("qfi_cliff_realamp_+_kolkata.npy", qfi)
