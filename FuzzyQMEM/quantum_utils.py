from itertools import product
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error
from qiskit.ignis.mitigation.measurement.filters import MeasurementFilter

import FuzzyQMEM.Circuits as C
import numpy.linalg as la


import numpy as np
import matplotlib.pyplot as plt
from qiskit import (execute, Aer, IBMQ)



def createCalibrationMatrix(cal_results, state_labels):
    """
    Function that returns a MeasurementFilter object containing the calibration matrix from which it is possible to compute mitigation matrix
    :param cal_results: list of lists - each list is the count of the execution of one of the basis states
    :param state_labels: list of strings - each string is the label of a basis state
    :return: a MeasurementFilter object containing the calibration matrix
    """
    def convertResultsInMatrix(list_results):
        shots = sum(list_results[0])
        col = [x / shots for x in list_results[0]]
        for i in range(1, len(list_results)):
            col = np.vstack((col, [x / shots for x in list_results[i]]))
        return col
    calibration_matrix=convertResultsInMatrix(cal_results)
    meas_filter=MeasurementFilter(calibration_matrix, state_labels)
    #print("Analitycal Calibration matrix\n", meas_filter.cal_matrix)
    #print("Analytical Mitigation matrix\n", la.inv(meas_filter.cal_matrix))
    return meas_filter


def getMitigationMatrix(cal_matrix):
    return la.inv(cal_matrix)


def createStateLabels(num_qubits):
    s=['0','1']
    sp=product(s, repeat=num_qubits)
    labels=[''.join(x) for x in sp ]
    return labels



def get_noise(p):
    error_meas = pauli_error([('X', p), ('I', 1 - p)])

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_meas, "measure")  # measurement error is applied to measurements

    return noise_model

def executeTestCircuit(circuit,backend, noise_model,shots=10000):
    results = execute(circuit, backend=backend, shots=shots, noise_model=noise_model).result()
    # noisy_counts = results.get_counts()
    # print("noisy",noisy_counts)
    # print(np.array(list(results.get_counts(0).values())).reshape(4,1)/10000)
    # return noisy_counts
    return results





def getDistributionStates(dict, num_qubits):
    num_shots=sum(dict.values())
    dis=[]
    keys=createStateLabels(num_qubits)
    for k in keys:
        if k in dict.keys():
            dis.append(dict[k]/num_shots)
        else:
            dis.append(0)
    return dis

def createBackend(real=False, token="", hub="", group="", project="", name=""):
    if real==False:
        return Aer.get_backend('qasm_simulator')  # per simulazioni

    IBMQ.save_account(token, overwrite=True)
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub=hub, group=group, project=project)
    backend = provider.get_backend(name)
    return backend

def convertInDict(r, num_qubits):
    states=createStateLabels(num_qubits)
    dict={}
    for i in range(len(states)):
        dict[states[i]]=int(r[i])
    return dict

def convertInList(dict, num_qubits):
    a=[]
    states = createStateLabels(num_qubits)
    for l in states:
        if l in dict.keys():
            a.append(round(dict[l]))
        else:
            a.append(0)
    return a




def fillDict(orig_dict, num_qubits):
    dict={}
    state_labes=createStateLabels(num_qubits)
    for s in state_labes:
        if s not in orig_dict.keys():
            dict[s] = 0
        else:
            dict[s] = orig_dict[s]
    return dict


def round_dict(dict):
    d={}
    for i in dict.keys():
        d[i]=int(round(dict[i]))
    return d


def plot_results(name, results, ideal_results, mitigated_results=None):
    # the histogram of the data
    labels = list(ideal_results.keys())
    results_values = list(fillDict(results.get_counts(0), len(labels[0])).values())
    ideal_values = list(ideal_results.values())
    num_shots = sum(results_values)
    results_values = [x / num_shots for x in results_values]
    ideal_values = [x / num_shots for x in ideal_values]
    width = 0.25
    X_axis = np.arange(len(labels))
    fig = plt.figure(figsize=(5, 4))
    plt.bar(X_axis, results_values, color='salmon',
            width=width, edgecolor='ghostwhite', label='Noisy')
    step_w=width
    if mitigated_results is not None:
        mitigated_values = list(mitigated_results.values())
        mitigated_values = [x / num_shots for x in mitigated_values]
        plt.bar(X_axis + width, mitigated_values, color='cornflowerblue',
                width=width, edgecolor='ghostwhite',
                label='Mitigated')
        step_w=2*width
    plt.bar(X_axis + step_w, ideal_values, color='mediumseagreen',
            width=width, edgecolor='ghostwhite',
            label='Ideal')
    plt.xlabel('State')
    plt.ylabel('Probability')
    plt.title('Circuit ' + name)
    #plt.legend(loc='upper right', bbox_to_anchor=(1.01, 1.015))
    plt.legend(loc='upper right', bbox_to_anchor=(1.35, 1.015))

    step=X_axis + width / 2
    if mitigated_results is not None:
        step=X_axis + width
    plt.xticks(step, labels)
    #plt.ylim(0,1.19)
    #fig=plot_histogram([results.get_counts(0), ideal_results], legend=['noisy', 'ideal'])
    plt.show()



def getTestCase(letter):
    if letter == 'a':
            return C.RandomCircuit1()
    if letter == 'b':
            return C.RandomCircuit2()
    if letter == 'c':
            return C.RandomCircuit3()
    if letter == 'd':
            return C.RandomCircuit4()
    if letter == 'e':
            return C.BellStateCircuit2Q()


if __name__=="__main__":
    backend = Aer.get_backend('qasm_simulator')
    num_shots = 10000
    #a = C.BellStateCircuit2Q()
    a = C.RandomCircuit1()
    a.createCircuit()
    results=executeTestCircuit(a.circuit,backend, None, shots=num_shots)
    print(results.get_counts(0))

    ideal_results=convertInDict(a.getOptimalDistribution(num_shots), num_shots)
    plot_results(a.name,results, ideal_results)
