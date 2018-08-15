import numpy as np

#Define some parameters for the iForest
N_ESTIMATORS=200 #number of trees to grow
MAX_SAMPLES=1.0 #number of samples to draw from X to train each tree
                #if int: draw max_samples. if float: draw float-fraction of X 
                #default: auto
MAX_FEATURES=1.0#0.3 #number of features to draw from X to train each tree
                #if int: draw max_features. if float: draw float-fraction of X
                ##default: 1 
RNG = np.random.RandomState(1994)

#Tresold for prediction of anomalies
TRESHOLD=-0.2

#Treshold for removal of large number of unique strings
UNIQUE_TRESHOLD=0.3

#Treshold for removal of columns with many missing values
NAN_TRESHOLD = 0.5

# Amount of samples to process at a time (Option 1a)
BATCH_SIZE = 100000

#USER VARIABLES
readFile = '' #string
selectOption = '' #string
compareFile = '' #string
keepOrDelete = '' #string
keepColumns = [] #list
deleteColumns = [] #list
renameColumns = {} #dictionary
dateColumn = [] #list
includeDays = False #bool
startDate = [] #list
endDate = [] #list
identifierColumn=[] #list
dateInternalCheck=[] #list
numberThatIsReallyWordColumns = [] #list
featureToAnalyze=[] #list
testMonthsSeparatly = True #bool
onlyUserColumns = True #bool
