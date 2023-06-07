import numpy as np

def computeBCD(p,q):
    """Function that computes the Bhattacharyya distance between two probability distributions"""
    BC = np.sum(np.sqrt(p * q))
    b = -np.log(BC)
    return b

if __name__=="__main__":
    p = np.asarray([0.65, 0.25, 0.07, 0.03])
    s = np.asarray([0.07, 0.25, 0.03, 0.65])
    print("Distance between q and s", computeBCD(p,s))