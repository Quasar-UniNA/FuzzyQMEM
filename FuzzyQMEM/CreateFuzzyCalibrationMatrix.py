import numpy as np
import FuzzyQMEM.utils as utils
import FuzzyQMEM.FuzzyClustering as sk
import FuzzyQMEM.quantum_utils as qu




def getUncertainRepresentativeExecution(alldata, u_mat):
    """
    Return the best count vector starting from all data related to a certain basis state circuit
    :param alldata: count vectors related to a certain basis state circuit.  Data are represented by a numpy matrix with features on rows.
    :param u_mat: U matrix obtained after applying fuzzy clustering
    :return:
    """
    k = len(u_mat)
    mem_u=[1/k]*k
    size_ex=len(u_mat[0])
    list_diff = []
    for i in range(size_ex):
        dis= [u_mat[x][i] for x in range(k)]
        diff = abs(np.array(mem_u) - np.array(dis))
        tot =sum(diff)
        list_diff.append(tot)
    index = list_diff.index(min(list_diff))
    chosen_execution=alldata[:,index]
    #print("Chosen index", index)
    #print("Chosen execution",chosen_execution)
    return chosen_execution


def createFuzzyBasedMitigationMatrices(state_labels, iter, list_k, list_dict_data, num_runs=1, path=""):
    """
    Function that creates a list of one or more mitigation matrices according to the number of runs
    :param state_labels: a list of string - each string represents the label related to a basis state
    :param iter: the number of iterations of the fuzzy clustering
    :param list_k: list of integers representing the tested number of clusters
    :param list_dict_data: list of dictionaries - each dictionary contains data to be clusterized labelled with basis state
    :param num_runs: number of runs to do
    :param path: path where there is the data
    :return:
    """
    list_obj=[]
    for j in range(num_runs):
        fitter = createFuzzyBasedCalibrationMatrix(state_labels,j,  iter, list_k, list_dict_data[j], path)
        list_obj.append(fitter)
    return list_obj



def createFuzzyBasedCalibrationMatrix(state_labels,index_run,  iter, list_k, dict_data, path):
    """
    Function that creates a list of one or more mitigation matrices according to the number of runs
    :param state_labels: a list of string - each string represents the label related to a basis state
    :param index_run: index of the run to repeat operation
    :param iter: the number of iterations of the fuzzy clustering
    :param list_k: list of integers representing the tested number of clusters
    :param dict_data: dictionary containing data to be clusterized labelled with basis state
    :param path: path where a file representing the MeasurementFilter object is stored
    :return:a MeasurementFilter object that contains a calibration matrix from which it is possible to build a mitigation matrix
    """
    cal_results = []
    for s in state_labels:
            alldata=dict_data[s]
            u_mat, k, fpc, nctr=sk.fuzzyClustering(path, index_run, s, alldata, iter, list_k)
            #SET STRATEGY
            res=getUncertainRepresentativeExecution(alldata, u_mat)
            #dict=convertInDict(res, state_labels)
            #cal_results.append(dict)
            cal_results.append(res)
    fitter=qu.createCalibrationMatrix(cal_results, state_labels)
    utils.save_obj(fitter, path+"fuzzy_matrix"+"_"+str(index_run))
    return fitter



if __name__=="__main__":
    num_qubits=2
    iter=10
    num_runs=2
    number_instances=20
    path="Data/"
    state_labels=qu.createStateLabels(num_qubits)
    dict_data={}
    for j in range(num_runs):
        for s in state_labels:
            dict_data[s] = utils.load_obj(path + "Alldata_" + str(number_instances) + "_" + s + "_" + str(j))
        meas_filter_fuzzy = createFuzzyBasedCalibrationMatrix(state_labels, j, iter, [2,3,4], dict_data, path)
        print(meas_filter_fuzzy.cal_matrix)
        print(qu.getMitigationMatrix(meas_filter_fuzzy.cal_matrix))
        meas_filter_fuzzy2 = utils.load_obj(path+"fuzzy_matrix_" + str(j))
        print(qu.getMitigationMatrix(meas_filter_fuzzy2.cal_matrix))




