import numpy as np
import pandas as pd

def compareEntriesInDataFrame(df_old, df_new, oldColumnName, newColumnName):
    """
    ARGS:
    df_old: pandas dataframe
    df_new: pandas dataframe, same index and same columns as df_old
    oldColumnName: string, name for column with values from df_old that did not match
    newColumnName: string, name for column with values from df_new that did not match
    RETURNS:
    pandas dataframe containing rows and columns where entries in df_old and df_new does not match,
    the values that did not match in df_old, and the values that did not match in df_new
    """
    #Find index-values for where df_old and df_new does not have the same entries
    #notEqualIndexes = np.where(np.not_equal(df_old.values, df_new.values)) DOES NOT GENERALIZE WELL ENOUGH
    notEqualIndexes = np.where(~((df_old.values == df_new.values) | ((df_old.values != df_old.values) & (df_new.values != df_new.values))))
    #Get column- and row-names for where df_old and df_new does not have the same entries
    #notEqualColumns = df_new.iloc[:, notEqualIndexes[1]].columns.tolist()
    #notEqualRows = df_new.iloc[notEqualIndexes[0]].index.tolist()
    #Values in df_old and df_new that did not match
    #oldDfValues = df_old.values[notEqualIndexes[0], notEqualIndexes[1]]
    #newDfValues = df_new.values[notEqualIndexes[0], notEqualIndexes[1]]
    return pd.DataFrame({'ID': df_new.iloc[notEqualIndexes[0]].index.tolist(), 'Column': df_new.iloc[:, notEqualIndexes[1]].columns.tolist(), oldColumnName: df_old.values[notEqualIndexes[0], notEqualIndexes[1]], newColumnName: df_new.values[notEqualIndexes[0], notEqualIndexes[1]]})


def findEntriesNotTheSame(df):
    """
    ARGS:
    df: pandas dataframe
    RETURNS:
    pandas dataframe that contains which rows does not have the correct value
    (first value is taken to be correct), what the value should be, and what the value currently is
    """
    #max_list = np.array([])
    correct_values=np.array([])
    index_names=np.array([])
    column_names=np.array([])
    error_values=np.array([])
    for column in df.columns:
        import time
        #max_list = np.append(max_list, df[column].value_counts().index[0])
        #print(max_list)
        #Find out what the values should be
        correctValue=df[column].value_counts().index[0]
        print(correctValue)
        #Find where values are not correct
        error_series=df[column].loc[df[column]!=correctValue]
        #Id for non-correct entries in column
        indexes=error_series.index.values
        #List of column-name so it has correct dimension
        columns=np.array([column]*len(indexes))
        correctValue=np.array([correctValue]*len(indexes))
        #Entries that are wrong
        errors=error_series.values
        correct_values=np.append(correct_values, correctValue)
        index_names=np.append(index_names, indexes)
        column_names=np.append(column_names, columns)
        error_values=np.append(error_values, errors)
    #Arange column-names and sort by columns
    return pd.DataFrame({'Column':column_names, 'ID':index_names, 'correctValue':correct_values, 'currentValue':error_values})

def deleteSameEntriesByPrecision(df, columns, precision=5):
    """
    ARGS:
    df: pandas dataframe
    columns: list of column-names in df, must be numbers
    precision: number of decimals to round to
    -------------------------------------
    RETURNS:
    pandas dataframe where column-names in 'columns' have been rounded to 'precision' number of decimals
    """
    return df[columns].round(decimals=precision)
