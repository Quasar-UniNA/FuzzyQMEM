from qiskit import Aer
import FuzzyQMEM.quantum_utils as qu
import FuzzyQMEM.utils as utils
import FuzzyQMEM.Circuits as C
import os

def createTestData( directory_name,circuit, backend, noise_model, testDatasize, num_shots):
    string_result=""
    list_results=[]
    for i in range(testDatasize):
        print("Execution", str((i + 1)))
        string_result += "Execution" + str((i + 1))
        # example
        results = qu.executeTestCircuit(circuit.circuit, backend, noise_model, shots=num_shots)
        print("Output", results.get_counts(0))
        string_result += "\nOutput" + str(results.get_counts(0))
        list_results.append(results.get_counts(0))
    utils.save_obj(list_results,  directory_name+"/TestData_"+circuit.name)
    return list_results



if __name__=="__main__":
    num_qubits = 2
    error = 0.15
    noise_model = qu.get_noise(error)
    backend = Aer.get_backend('qasm_simulator')
    circ = C.RandomCircuit1()
    circ.createCircuit()
    state_labels = qu.createStateLabels(num_qubits)
    num_shots = 10000
    testDatasize=1000
    directory_name = "TestData_0.15"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    createTestData( directory_name,circ, backend, noise_model, testDatasize, num_shots)



