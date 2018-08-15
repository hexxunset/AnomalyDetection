import numpy as np

import globalConstants as GC

from sklearn.ensemble import IsolationForest


def iForest():
    print("Welcome to iForest")
    """
    RETURNS:
    Isolation Forest class from sklearn with settings defined by global constants
    """
    print("Bye from iF")
    return IsolationForest(n_estimators=GC.N_ESTIMATORS,
                 max_samples=GC.MAX_SAMPLES,
                 max_features=GC.MAX_FEATURES,
                 random_state=GC.RNG)

def addPredictions(df, scoreColumn):
    """
    ARGS:
    df: pandas dataframe containing test-data and anomaly-score for each sample
    scoreColumn: string, name of column to check againts treshold
    --------------------------------------
    RETURNS:
    pandas dataframe with column containing predictions of each sample (normal=1, abnormal=0) based on the treshold in global constants
    """
    #Setting all samples with anomaly-score/relative height less than the treshols to be anomalies
    predNormal=np.where(df[scoreColumn]<(GC.TRESHOLD), 0, 1)
    df=df.assign(predNormal=predNormal)
    return df



####################################################################################################################
#############THE CODE BELOW IS NOT USED IN THE PROGRAM
####################################################################################################################

def getAveragePathLength(n, anomScore):
    """
    ARGS:
    n: Number of samples in test-set
    anomScore: Anomaly-score of each sample in test-set
    --------------------------------------------
    RETURNS:
    Average height of each sample from the anomaly score
    Matematical estimation of what the average height should be, given the number of samples
    """
    #Harmonic number
    H=lambda i : np.log(i)+0.5772156649
    #Estimation of what the average height should be
    c = lambda n : 2*H(n-1)-(2*(n-1)/n)
    #Original score from paper
    s=0.5-anomScore
    return(-1*(c(n)*np.log(s))/np.log(2)), c(n)

def makeAnomalyScore(n, x):
    """
    ARGS:
    n: Number of samples in test-set
    x: Average height for a sample over an ensemble of trees
    --------------------------------------------
    RETURNS:
    Anomaly score for sample as if would be if given by Sklearns implementation
    Matematical estimation of what the average height should be, given the number of samples
    """
    # Harmonic number
    H = lambda i: np.log(i) + 0.5772156649
    # Estimation of what the average height should be
    c = lambda n: 2 * H(n - 1) - (2 * (n - 1) / n)
    # Original score from paper
    s = 2**(-x/(c(n)))
    return 0.5-s, c(n)