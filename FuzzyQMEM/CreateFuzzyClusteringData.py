from qiskit.ignis.mitigation.measurement import complete_meas_cal
from qiskit import QuantumRegister, Aer, execute

import numpy as np
import FuzzyQMEM.utils as utils
import FuzzyQMEM.quantum_utils as qu

from tqdm import tqdm
import os


def createData(num_qubits=2, backend=None, noise_model=None, number_of_instances=20, num_runs=1, path=""):
    """
    Function that creates num_runs matrices for each basis circuit. Each matrix contains R rows and C columns where
    R is the number of basis states (features) and C is the number of instances.
    :param num_qubit:
    :param backend:
    :param noise_model:
    :param number_of_instances:
    :param num_runs:
    :param path:
    :return: null
    """
    qr = QuantumRegister(num_qubits)
    meas_calibs, state_labels = complete_meas_cal(qr=qr, circlabel='mcal')
    dict={}
    for s in state_labels:
        dict[s]=list()
    for n in range(num_runs):
        l_gen = tqdm(range(number_of_instances), desc="Number of instances")
        for i in l_gen:
            job = execute(meas_calibs, backend=backend, shots=1000, noise_model=noise_model)
            cal_results = job.result()
            for j in range(len(state_labels)):
                count=cal_results.get_counts(j)
                count_l=qu.convertInList(count, num_qubits)
                dict[state_labels[j]].append(count_l)
        for s in state_labels:
            matrix=np.array(dict[s]).T
            utils.save_obj(matrix, path+"Alldata_"+str(number_of_instances)+"_"+s+"_"+str(n))
    print('Data created!')


if __name__=="__main__":
    path="Data/"
    if not os.path.exists(path):
        os.makedirs(path)
    error=0.15
    num_qubits = 2
    noise_model = qu.get_noise(error)
    backend = Aer.get_backend('qasm_simulator')
    number_instances=20
    num_runs=2
    createData(num_qubits,backend, noise_model, number_instances, num_runs, path)