from qiskit.quantum_info import hellinger_fidelity
import numpy as np

import FuzzyQMEM.quantum_utils as qu
import FuzzyQMEM.distance_quantum_states as qd
import FuzzyQMEM.Circuits as C

import FuzzyQMEM.utils as utils
import statistics as st

import os


def test(num_qubits, path_store, circuits, list_results_dict, num_shots, matrices, name_approach):
    """
    Function that verifies the quality of a mitigation matrix
    :param num_qubits:
    :param path_store:
    :param circuit:
    :param list_results: list of dictionaries - each dictionary represents a count vector
    :param num_shots:
    :param matrices:
    :param name_approach:
    :return:
    """
    lm = []
    lmh = []
    lmed = []
    lmedh = []
    n=0
    for matrix in matrices:
        print("Matrix", str(n))
        list_file_m = []
        list_file_m_h = []
        list_file_med = []
        list_file_med_h = []

        for circuit in circuits:
            print("Circuit", circuit.name )
            best_dis = circuit.getOptimalDistribution(num_shots)
            string_result = ""
            best_dict = qu.convertInDict(best_dis,num_qubits)
            dis_a = []
            dis_h_a = []
            # load test data
            list_results = list_results_dict[circuit.name]
            i = 0
            for results in list_results:
                #print("Execution", str((i + 1)))
                string_result += "Execution" + str((i + 1))
                i += 1

                #print("Output", results)
                string_result += "\nOutput" + str(results)
                # Results with mitigation
                mitigated_counts = matrix.apply(results)

                a_l=qu.convertInList(qu.fillDict(mitigated_counts, num_qubits), num_qubits)
                #print("mitigated", a_l)

                string_result += "\n" + name_approach + " " + str(a_l)
                dis_a.append(qd.computeBCD(np.array(best_dis) / num_shots, np.array(a_l) / num_shots))
                # print(dis_a)
                dict_l = qu.convertInDict(a_l, num_qubits)
                dis_h_a.append(hellinger_fidelity(dict_l, best_dict))
            m_a = sum(dis_a) / (len(dis_a))
            print("Average distance of " + name_approach + " approach", m_a)
            string_result += "\nAverage distance of " + name_approach + " approach" + str(m_a)
            path_file = path_store + "Circuit_" + circuit.name + "_" + str(n)
            if not os.path.exists(path_file):
                os.makedirs(path_file)
            utils.writeArray(path_file + "/Distance", dis_a)
            m_h_a = sum(dis_h_a) / (len(dis_h_a))
            print("Average fidelity of " + name_approach + " approach", m_h_a)
            string_result += "\nAverage fidelity of " + name_approach + " approach" + str(m_h_a)
            utils.writeArray(path_file + "/Fidelity", dis_h_a)
            med_a = st.median(dis_a)
            print("Median distance of " + name_approach + " approach", med_a)
            string_result += "\nMedian distance of " + name_approach + " approach" + str(med_a)
            med_h_a = st.median(dis_h_a)
            print("Median fidelity of " + name_approach + " approach", med_h_a)
            string_result += "\nMedian fidelity of " + name_approach + " approach" + str(med_h_a)
            utils.writeFile(path_file + "/Console.txt", string_result)
            list_file_m.append(m_a)
            list_file_m_h.append(m_h_a)
            list_file_med.append(med_a)
            list_file_med_h.append(med_h_a)
        lm.append(list_file_m)
        lmh.append(list_file_m_h)
        lmed.append(list_file_med)
        lmedh.append(list_file_med_h)
        n += 1
    circuit_labels=[circ.name for circ in circuits]
    approach_labels=[name_approach+"_"+str(k) for k in range(len(matrices))]
    utils.writeListResultsXls(path_store + "ResultsMeanDistance.xlsx", ["Circuits"] + approach_labels,
                              [circuit_labels] + lm)
    utils.writeListResultsXls(path_store + "ResultsMedianDistance.xlsx", ["Circuits"] + approach_labels,
                              [circuit_labels] + lmed)
    utils.writeListResultsXls(path_store + "ResultsMeanFidelity.xlsx", ["Circuits"] + approach_labels,
                              [circuit_labels] + lmh)
    utils.writeListResultsXls(path_store + "ResultsMedianFidelity.xlsx", ["Circuits"] + approach_labels,
                              [circuit_labels] + lmedh)


if __name__=="__main__":
    num_qubits=2
    error = 0.15
    circ = C.RandomCircuit1()
    circ.createCircuit()
    circ2 = C.RandomCircuit2()
    circ.createCircuit()
    circuits=[]
    circuits.append(circ)
    circuits.append(circ2)
    num_shots = 10000
    list_results_dict ={}
    list_results_dict[circ.name] =utils.load_obj("TestData_" + str(error) + "/TestData_" + circ.name)
    list_results_dict[circ2.name]=utils.load_obj("TestData_" + str(error) + "/TestData_" + circ2.name)

    path= "Data/"
    fuzzy_matrix = utils.load_obj(path + "fuzzy_matrix_0")
    fuzzy_matrix2 = utils.load_obj(path + "fuzzy_matrix_1")
    ibm_matrix = utils.load_obj(path + "IBMCalibrationMatrix_0")
    ibm_matrix2 = utils.load_obj(path + "IBMCalibrationMatrix_1")
    test(num_qubits, "FuzzyQMEM/TestFuzzy/", circuits, list_results_dict, num_shots, [fuzzy_matrix, fuzzy_matrix2], "Fuzzy")
    print("\n")
    test(num_qubits, "FuzzyQMEM/TestIBM/", circuits, list_results_dict, num_shots, [ibm_matrix, ibm_matrix2], "IBM")

#plot_histogram([noisy_counts, mitigated_counts], legend=['noisy', 'mitigated'])
#plt.show()