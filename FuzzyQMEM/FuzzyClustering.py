import skfuzzy as fuzz
import FuzzyQMEM.utils as utils
import numpy as np

def fuzzyClustering(path, index_run, state_label, alldata, iter, list_k):
    """
    Function that performs the Fuzzy C-means procedure on a set of data related to a certain computational basis circuit
    :param path: path where a file containing fpcs will be stored
    :param index_run: integer number representing the index of the run executed
    :param state_label: string indicating the state of the circuit related to data
    :param alldata: data to be clusterized. Data are represented by a numpy matrix with features on rows.
    :param iter: number of iterations to be performed by the Fuzzy c-means
    :param list_k: list of integers representing the tested number of clusters
    :return: the best U matrix, the best number of clusters, the best fpc and the best centroids
    """
    fpcs=[]
    list_m=[]
    list_c=[]
    for ncenters in list_k:
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata, ncenters, 2, error=0.005, maxiter=iter)
        list_c.append(cntr)
        # Store fpc values for later
        fpcs.append(fpc)
        # Plot assigned clusters, for each data point in training set
        #cluster_membership = np.argmax(u, axis=0)
        #print(cluster_membership)
        list_m.append(u)
    index=fpcs.index(max(fpcs))
    chunked_array = np.array_split(fpcs, len(fpcs))
    fpcs_xsl = [list(array) for array in chunked_array]
    utils.writeMatrixXls(path+"FPC_"+state_label+"_"+str(index_run)+".xlsx", list_k, fpcs_xsl)
    return list_m[index], list_k[index], fpcs[index], list_c[index]