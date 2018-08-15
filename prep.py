import pandas as pd
import numpy as np

import functions as F

from sklearn.preprocessing import LabelEncoder

def vectorizeDates(df, column, makeDay):
    """
    ARGS:
    df: pandas dataframe
    columnToVectorize: list/array containing name of column in df to vectorize
    makeYear: boolean, weather to make a year-vector
    makeMonth: boolean, weather to make a month-vector
    makeDay: boolean, weather to make a day-vector
    -----------------------------------------------------
    Returns df where column in columnToVectorize[0] have been vectorized to year, month, (day)-vector
    """
    #Convert to datetime
    date=pd.to_datetime(df[column[0]])
    df=df.assign(Year=date.dt.year.values)
    df.set_index(['Year'], inplace=True)
    print(column[0]+" Year ready")
    df=df.assign(Month=date.dt.month.values)
    df.set_index(['Month'], inplace=True, append=True)
    print(column[0]+" Month ready")
    if makeDay:
        df=df.assign(Day=date.dt.day.values)
        df.set_index(['Day'], inplace=True, append=True)
        print(column[0]+" Day ready")
    #Drop old date-columns
    df=df.drop(columns=column)
    return df


def labelEncode(df_objects):
    """
    ARGS:
    df_objects: pandas dataframe with non-numerical entries
    ------------------------------------------------
    RETURNS:
    pandas dataframe with entries in df_objects label-encoded
    """
    array_labelEncoded = LabelEncoder().fit_transform(df_objects.values.flatten())
    return pd.DataFrame(np.reshape(array_labelEncoded, (len(df_objects.index.tolist()), len(df_objects.columns.tolist()))),
        columns=df_objects.columns, index=df_objects.index)


def onehotEncode(df, columns):
    """
    ARGS:
    df: pandas dataFrame
    columns: list/array, columns in df to encode
    -----------------------
    RETURNS:
    pandas dataFrame with selected columns one-hot encoded
    """
    #Make sure no numerical values are in columns
    columns_nonNumerical=df[columns].select_dtypes(include=['object', 'bool']).columns.tolist()
    if not F.nonEmptyIntersection(columns_nonNumerical, columns)[0]:
        print("Given columns with numerical values. Columns with numeric values will not be onehot-encoded.")
    return pd.get_dummies(df, columns=columns_nonNumerical)

def removeMissingValueFeatures(df, nanTreshold):
    """
    ARGS:
    df: pandas dataframe to remove features from
    nanTreshold: float, amount of feature that must be missing values for it to be deleted
    --------------------------------------------------
    RETURNS:
    pandas dataframe with only features containing less than treshold*rows are kept
    list of features removed from df
    pandas Series with number of missing values for each row in df
    """
    df_temp=df.loc[:, df.isnull().sum()<(nanTreshold*df.shape[0])]
    return df_temp, list(set(df.columns.tolist()).difference(df_temp.columns.tolist())), df.isnull().sum(axis=1)

def replaceMissingValues(df, columns, replaceType='median'):
    """
    ARGS:
    df: pandas dataframe to replace missing values in
    columns: list, columns in df to replace missing values in. If dtype of a column is not numerical, it won't be processed
    replaceType: string, weather to replace to missing values with the median or the mean of each feature
    --------------------------------------------------
    RETURNS:
    pandas dataframe were missing values in each column in 'columns' have been replaced with mean/median of that column
    number of missing values found (and replaced)
    """
    #Make sure only numerical values are in columns
    columns_num=df[columns].select_dtypes(exclude=['object', 'bool']).columns.tolist()
    missingValues=df[columns_num].isnull().values.sum()
    if replaceType=='median':
        df[columns_num]=df[columns_num].fillna(df[columns_num].median())
    elif replaceType == 'mean':
        df[columns_num].fillna(df[columns_num].mean())
    return df, missingValues


####################################################################################################################
#############THE CODE BELOW IS NOT USED IN THE PROGRAM
####################################################################################################################

def replaceNaN(df, columns, value):
    """
    ARGS:
    df: pandas dataframe
    columns: list, columns to replace NaN in
    value: optional, value to replace NaN with
    -------------------------------------
    RETURNS:
    pandas dataframe where NaN-entries in columns have been replaced with value
    """
    df[columns].fillna(value=value, inplace=True)
    return df