import pandas as pd
import numpy as np
#from datetime import date, timedelta


def nameToFileName(name):
    """
    ARGS:
    name: string containing the name of the file
    -----------------------------------------------
    RETURNS:
    string with name on format accepted by computer
    """
    return '/'+name+'.csv'


def fileNameToName(fileName):
    """
    ARGS:
    name: string with name on format accepted by computer
    -----------------------------------------------
    RETURNS:
    string containing the name of the file
    """
    return fileName[1:-4]


def addEmpty(df, startDate, endDate, featureToAnalyze, daily):
    """
    ARGS:
    df: pandas dataframe
    startDate: string, date to begin filling of zeros from (format 'm/d/yyyy')
    endDate: string, date to end filling of zeros from (format 'm/d/yyyy')
    featureToanalyze: list, only entry is string with name of index to analyze
    daily: bool, set false if df does not contain day-vector
    RETURNS:
    pandas dataframe where non-existing dates have been given an entry with zero-values
    """
    dateIndex = pd.period_range(start=startDate, end=endDate, freq=('M', 'D')[daily])
    #Make dataframe with all dates as index and temporary column containing zeros
    df_dates = pd.DataFrame(0, index=dateIndex, columns=np.append('tempCol', df.columns))
    splitIndex = (lambda d: (d.year, d.month, d.day)) if daily else (lambda d: (d.year, d.month))
    df_dates=df_dates.assign(Year=dateIndex.year)
    df_dates=df_dates.assign(Month=dateIndex.month)
    df_dates.set_index(['Year','Month'], inplace=True)
    if daily:
        df_dates=df_dates.assign(Day=dateIndex.day)
        df_dates.set_index(['Day'], inplace=True, append=True)
    #Reset index for later merging
    df_dates.reset_index(inplace=True)
    if len(featureToAnalyze)!=0:
        #Make dataframe containing identifier and all other (onehot encoded) columns
        df_id=pd.DataFrame(0, index=df.index.get_level_values(featureToAnalyze[0]).unique(), columns=np.append('tempCol', df.columns))
        df_id.reset_index(inplace=True)
        df_dates = df_dates.merge(df_id, how='outer')
        #df_empty = df_dates.merge(df_id, how='outer')
    del df_dates['tempCol']
    df_dates.set_index(df.index.names, inplace=True)
    #Update df to containt zeros where there is nothing happening
    df = pd.concat([df, df_dates[~df_dates.index.isin(df.index)]])
    df.sort_index(inplace=True)
    return df.fillna(0)

def nonEmptyIntersection(listToCheck, listToCheckIn):
    """
    ARGS:
    listToCheck: list/array
    listToCheckIn: list/array
    RETURNS:
    bool, True if at least one of the entries in listToCheck are also in listToCheckIn
    list, all entries in listToCheck that are also in listToCheckIn
    """
    return len(set(listToCheck).intersection(listToCheckIn)) != 0, list(set(listToCheck).intersection(listToCheckIn))


def addColumnsForColumns(df, f, name):
    """
    ARGS:
    df: pandas dataframe
    f: function to do on each column
    name: string, describes result from function
    RETURNS:
    pandas dataframe where each column is the result of 'function' beeing done on each column in df
    """
    # step 1: flatten array
    df_asArray = df.values.flatten()
    # Step 2: make array with boolean for wanted condition, turn to int
    # 1 if value is negative, 0 else
    # negative_array = (df_asArray < 0).astype(int)
    function_array = f(df_asArray).astype(int)
    # Step 3: make column-names
    columnNames = name + '_'+df.columns
    # Step 4: make dataframe with wanted values
    return pd.DataFrame(np.reshape(function_array, (len(df.index.tolist()), len(df.columns.tolist()))),
                        columns=columnNames, index=df.index)

def getIntersectingAndUniqueRows(df, df_old):
    """
    ARGS:
    df: pandas dataframe
    df_old: pandas dataframe
    ----------------------------
    RETURNS:
    pandas dataframe containing rows from df with id's in both df and df_old
    pandas dataframe containing rows from df_old with id's in both df and df_old
    pandas dataframe containing rows from df with id's not in df_old
    pandas dataframe containing rows from df_old with id's not in df
    """
    commonIndexes=df_old.index.intersection(df.index.values)
    return df.loc[commonIndexes.values], df_old.loc[commonIndexes.values], df[~df.index.isin(commonIndexes)], df_old[~df_old.index.isin(commonIndexes)]



####################################################################################################################
#############THE CODE BELOW IS NOT USED IN THE PROGRAM
####################################################################################################################

###NEEDs WORK
def printAllColumns(df, interval):
    for c in range(0, len(df.columns.tolist()), interval):
        endIndex=c+interval
        if endIndex>len(df.columns.tolist()):
            endIndex=len(df.columns.tolist())
        print(df.iloc[:, c:endIndex])

def flattenDf(df):
    """
    ARGS:
    df: pandas dataframe to flatten
    -----------------------------------------
    RETURNS:
    numpy array of flattened df
    list of indexes in df
    list of column-names in df
    list of index-names in df
    """
    return df.values.flatten(), df.index.tolist(), df.columns.tolist(), df.index.names

def reshapeArrayAsDf(df_original, array, indexes, columns, indexNames):
    """
    ARGS:
    df_original: pandas dataframe with correct column-names and indexes
    array: numpy array to reshape into pandas dataframe
    indexes: indexes to set for df
    columns: columns to set for df
    indexNames: names of indexes in original df
    -------------------------------------------------------
    RETURNS:
    pandas dataframe from array reshaped to dimensions
    """
    df=pd.DataFrame(np.reshape(array, (len(indexes), len(columns))), columns=columns)
    for indexName in indexNames:
        df.loc[:,indexName]=df_original.index.get_level_values(indexName)
    df.set_index(indexNames, inplace=True)
    return df


###NEEDs WORK
def testSetAllMonths(df, test_month, include2018):
    """
    ARGS:
    df: pandas dataframe
    test_month: int, the month of the year to check for anomalies
    include2018: bool, whether to include the year 2018 (DON'T THINK I NEED, 2018 EMPTY AFTER JUNE)
    ----------------------------------------
    RETURNS:
    pandas dataframe containing only the chosen LCC and entries for the test-month (every year) sorted by year
    pandas dataframe containing all other months
    """
    if not (include2018):
        df=df.loc[df.index.get_level_values('LoadDateYear')!=2018]
    return df.loc[df.index.get_level_values('LoadDateMonth')==test_month], df.loc[df.index.get_level_values('LoadDateMonth')!=test_month]

###NEEDs WORK
def testSetPreviousMonths(df, test_month, test_year, numberOfMonths):
    """
    ARGS:
    df: pandas dataframe with only the chosen LoadCountryCode, index0: Year, index1: Month
    test_month: month to currently check for anomalies
    test_year: year to currently check for anomalies
    numberOfMonths: number of entries (months) wanted in test-set
    -----------------------------------------------------------
    RETURNS:
    pandas dataframe containing only the chosen LCC with current test-entry and previous entries (by date), numberOfMonths entries in total
    """
    #Assure df is sorted by date
    df.sort_index(level=[0,1], axis=0, inplace=True)
    #Find row with test-entry
    testEntry_row=np.where(np.logical_and(df.index.get_level_values('LoadDateYear').values==test_year, df.index.get_level_values('LoadDateMonth').values==test_month))
    start_row=testEntry_row[0][0]-numberOfMonths
    if numberOfMonths>testEntry_row[0][0]:
        start_row=0
        print("Number of requested entries too large. Returning first row to test-entry-row.")
    return df.iloc[start_row:testEntry_row[0][0]]


def nameToExcelName(name):
    """
    ARGS:
    name: string containing the name of the file
    -----------------------------------------------
    RETURNS:
    string with name on format accepted by computer
    """
    return name+'.xlsx'

def getNumberOfYearsForMonths(df):
    """
    ARGS:
    df: pandas dataframe with year- and month-vector
    -------------------------
    RETURNS:
    numpy array containing number of years for months. Index 0 - january, index 11 - december
    """
    return df.groupby(['Month']).aggregate('count').iloc[:,0].values/len(df.index.get_level_values('id').unique())



def getDateRows(df, date, includeDays):
    """
    NEEDS YEAR, MONTH, AND DAY
    ARGS:
    df: pandas dataframe
    date: list with date on format [year, month, day] 
    -------------------------------------------------
    RETURNS:
    pandas dataframe with rows that have 'date' as index
    """

    yearBool_list=df.index.get_level_values('Year').values==date[0]
    monthBool_list=df.index.get_level_values('Month').values==date[1]
    yearMonthBool_list=np.logical_and(yearBool_list, monthBool_list)
    if includeDays:
        dayBool_list=df.index.get_level_values('Day').values==date[2]
        return df.iloc[np.where(np.logical_and(yearMonthBool_list, dayBool_list))]
    else:
        return df.iloc[np.where(yearMonthBool_list)]
