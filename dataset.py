import csv
import pandas as pd
import os

import functions as F

#Current working directory
DATAPATH=os.getcwd()

def readFile_csv(file, index_col=None):
    """
    Args:
    file: string, path in current folder to file
    index_col: columns in file to use as index in pandas dataframe
    -------------------------------------
    Returns:
    pandas dataframe containing file
    """
    #Loading dataset
    filePath=DATAPATH+file
    df = pd.read_csv(filePath, na_values=" ", index_col=index_col)
    print(F.fileNameToName(file), " loaded.")
    return df


def writeToFile_csv(df, filename='/saved_dataset.csv', index=False):
    """
    Args:
    df: pandas dataframe
    filename: what to call the file. Default is set to avoid accidently overwriting existing files
    index: weather or not to save index
    -------------------------------------
    Saves dataframe to .csv-file in current path
    """
    #Convert non-dataframe to dataframe
    if not(isinstance(df, pd.DataFrame)):
        df=pd.DataFrame(df)
    #Where to save file
    filePath=DATAPATH+filename
    df.to_csv(filePath, index=index)
    print(F.fileNameToName(filename), ' saved.')


####################################################################################################################
#############THE CODE BELOW IS NOT USED IN THE PROGRAM
####################################################################################################################
def readFile_excel(file):
    """
    Args:
    file: string, path in current folder to file
    -------------------------------------
    Returns:
    pandas dataframe containing file
    """

    df = pd.read_excel(DATAPATH + file)
    print(F.fileNameToName(file), " loaded.")
    return df


def writeToFile_excel(df, index, filename='newSheet.xlsx'):
    """
    ARGS:
    df: pandas dataframe to save to Excel
    filename: string with desired name of file
    ---------------------------------------------
    Writes df to Excel-file with name filename
    """
    engine = 'xlsxwriter'
    df.to_excel(filename.format(engine), engine=engine, index=index)