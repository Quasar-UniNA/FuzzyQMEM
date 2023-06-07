from qiskit import QuantumRegister, Aer, execute
from qiskit.ignis.mitigation.measurement import (complete_meas_cal,CompleteMeasFitter)
import FuzzyQMEM.utils as utils
import FuzzyQMEM.quantum_utils as qu



def createIBMCalibrationMatrix(num_qubits=2, backend=None, noise_model=None):
    """
    Function that returns a calibration matrix by running computational basis state circuits on the given backend
    :param num_qubit: the number of qubits of the quantum register to mitigate
    :param backend: processor
    :param noise_model: noise model
    :return:
    """
    qr = QuantumRegister(num_qubits)
    meas_calibs, state_labels = complete_meas_cal(qr=qr, circlabel='mcal')
    # Execute the calibration circuits without noise
    job = execute(meas_calibs, backend=backend, shots=1000, noise_model=noise_model)
    cal_results = job.result()
    meas_fitter = CompleteMeasFitter(cal_results, state_labels, circlabel='mcal')
    return meas_fitter.filter, state_labels


def createIBMCalibrationMatrices(num_qubits=2, num_runs=1, path="", backend=None, noise_model=None):
    for i in range(num_runs):
        meas_fitter, s=createIBMCalibrationMatrix(num_qubits,backend,noise_model)
        utils.save_obj(meas_fitter,path+"IBMCalibrationMatrix"+"_"+str(i))


def createCalibrationMatrix(cal_results, state_labels):
    """
    Function that returns a calibration matrix starting from vector counts related to basis states
    :param cal_results: list of lists - each list is the count of the execution of one of the basis states
    :param state_labels: list of strings - each string is the label of a basis state
    :return: a MeasurementFilter object containing the calibration matrix
    """
    return qu.createCalibrationMatrix(cal_results, state_labels)

if __name__=="__main__":
    error=0.15
    num_runs=2
    num_qubits = 2
    noise_model = qu.get_noise(error)
    backend = Aer.get_backend('qasm_simulator')
    path="Data/"
    createIBMCalibrationMatrices(num_qubits, num_runs, path, backend, noise_model)
    meas_fitter = utils.load_obj(path+"IBMCalibrationMatrix_" +str(1))
    print(meas_fitter.cal_matrix)

