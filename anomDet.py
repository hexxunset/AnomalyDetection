import pandas as pd
import numpy as np

import globalConstants as GC
import prep as PR
import functions as F
import dataset as DS
import algorithm as AL
import analyze as AN

from userVariables import *

# Get file as pandas dataframe
df = DS.readFile_csv(F.nameToFileName(readFile))

if selectOption=='Option 2':
    df_old = DS.readFile_csv(F.nameToFileName(compareFile))

    
#############################PREPROCESS 1####################################

# bool, list with name(string) of old-columnnames
hasRenameColumns, renameColumnsKeys = F.nonEmptyIntersection(renameColumns.keys(), df.columns.tolist())
# Rename columns if columns in dataframe are set to be renamed
if hasRenameColumns:
    print("-------------------------------------------------------------------------------")
    print("Selected columns (that also exist in file) have been renamed")
    newColumnNames = {renameColumnsKeys: renameColumns[renameColumnsKeys] for renameColumnsKeys in renameColumnsKeys}
    df = df.rename(columns=newColumnNames)
    if selectOption=='Option 2':
        df_old = df_old.rename(columns=newColumnNames)


index = False
#Add index, either ID, date, or both
# bool, list with name(string) of date-column
hasDateColumn, dateColumn= F.nonEmptyIntersection(dateColumn, df.columns.tolist())
# Add columns describing date, added as indexes
if hasDateColumn and selectOption[:8]=='Option 1':
    print("-------------------------------------------------------------------------------")
    print('Adding ', dateColumn[0], ' as date')
    df = PR.vectorizeDates(df, dateColumn, includeDays)
    index = True

# bool, list with name(string) of id-column (for internal checks)
hasIdentifier, identifierColumn = F.nonEmptyIntersection(identifierColumn, df.columns.tolist())
# Add identifier as index to avoid it beeing processed
if hasIdentifier and selectOption!='Option 1a':
    if len(identifierColumn)>1:
        id_name='__'.join(identifierColumn)
        df[id_name]=df[identifierColumn[0]].astype(str)
        del df[identifierColumn[0]]
        if selectOption=='Option 2':
            df_old[id_name]=df_old[identifierColumn[0]].astype(str)
            del df_old[identifierColumn[0]]
        
        for i in range(1,len(identifierColumn)):
            df[id_name]=df[id_name].astype(str)+'__'+df[identifierColumn[i]].astype(str)
            del df[identifierColumn[i]]
            if selectOption=='Option 2':
                df_old[id_name]=df_old[id_name].astype(str)+'__'+df_old[identifierColumn[i]].astype(str)
                del df_old[identifierColumn[i]]
        identifierColumn=[id_name]
    print("-------------------------------------------------------------------------------")
    print('Adding ', identifierColumn[0], ' as identifier')
    df.set_index(identifierColumn[0], inplace=True, append=index)
    print("Number of unique ID's set for ", readFile, 'are: ', len(df.index.unique()))
    print("This should be equal to the number of rows. If the ID's are not unique,")
    print("the program might not work.")
    if selectOption=='Option 2':
        #Does not need to append, should only have identifiercolumns
        df_old.set_index(identifierColumn[0], inplace=True)
        print("Number of unique ID's set for ", compareFile, 'are: ', len(df.index.unique()))
        print("This should be equal to the number of rows. If the ID's are not unique,")
        print("the program might not work.")
    index = True
                

# Indexes in dataframe
indexVector = ['Year', 'Month']
dateFormat = '(%Y, %m)'
if includeDays:
    indexVector = indexVector + ['Day']
    dateFormat = '(%Y, %m, %d)'

# Keep columns selected by user
if keepOrDelete.lower() == 'all':
    print("All columns are kept")
    print("WARNING: Columns with large number of missing values")
    print("or large number of different entries (words)")
    print("will be deleted")

else:
    if keepOrDelete.lower() == 'delete':
        keepColumns = list(set(df.columns.tolist()).difference(deleteColumns))

    keepColumns = keepColumns + dateColumn + featureToAnalyze
    # bool, list with name(string) of columns to keep in df
    hasKeepColumns, keepColumns = F.nonEmptyIntersection(keepColumns, df.columns.tolist())
    # Keep only selected columns
    if hasKeepColumns:
        df = df[keepColumns]
        print("-------------------------------------------------------------------------------")
        print("Columns that will be kept in dataset: ")
        print(df.dtypes)

shapeOfDf=df.shape
print("-------------------------------------------------------------------------------")
print("First 5 rows in " + readFile + " are:")
print(df.head())
print(df.dtypes)
print("This file now has", shapeOfDf[0], "rows and", shapeOfDf[1], "columns")

if selectOption == 'Option 1a' or selectOption == 'Option 1b':
    """
    ******** - 'Option 1': RUNNING THE ANOMALY-DETECTION PROGRAM                     
    """

    ##############################PREPROCESS 1#########################################################################
    # iForest, parameters set by global constants
    IF = AL.iForest()

    # Select only wanted date from dataframe for local anomaly-check to avoid un-necessary computing
    if selectOption=='Option 1b':
        if len(dateInternalCheck)!=0:
            print("-------------------------------------------------------------------------------")
            print("Will run anomaly-check for selected date: ", dateInternalCheck)
            df = F.getDateRows(df, dateInternalCheck, (True if len(dateInternalCheck)==3 else False))
            if df.empty:
                print("There are no entries for the selected date. Select some other date.")
                quit()
        else:
            print("-------------------------------------------------------------------------------")
            print("Please add a date to check for anomalies")
            quit()

    #Ensure that columns are treated by the correct preprocessing-step
    # bool, list with names(strings) of columns that appear to be numeric but are really strings
    hasNumberThatIsReallyWordColumns, numberThatIsReallyWordColumns = F.nonEmptyIntersection(
        numberThatIsReallyWordColumns, df.columns.tolist())

    # Ensure that id's are treated as strings
    if hasNumberThatIsReallyWordColumns:
        df[numberThatIsReallyWordColumns[0]] = df[numberThatIsReallyWordColumns[0]].apply(str)

    #Save preprocessing 1
    #readFile = readFile + '_prep1'
    #DS.writeToFile_csv(df, F.nameToFileName(readFile))

    print('-------------------------------------------------------------------------------')
    print("df after step 1:")
    print(df.shape)
    print(df.dtypes)
    #############################PREPROCESS 2###########################################################################
    # Get list of all columns containing numerical values
    list_numericalColumns = df.select_dtypes(exclude=['object', 'bool']).columns.tolist()

    #Get dataframe containing if each row in each column has missing entry
    f=lambda x:pd.isnull(x)
    df_missing = F.addColumnsForColumns(df, f, 'missing')

    #Get number of total negative entries for each row
    numNeg=(df[list_numericalColumns].values<0).sum(axis=1)
    # Remove columns containing a large number of missing entries
    df, removedColumns, numMiss = PR.removeMissingValueFeatures(df, GC.NAN_TRESHOLD)

    if len(removedColumns)!=0:
        print("-------------------------------------------------------------------------------")
        print("Columns that have been removed because of large number of missing values are: ",removedColumns)

    #Save step 2 to file
    #readFile = readFile + '_prep2'
    #DS.writeToFile_csv(df, F.nameToFileName(readFile), index=index)
    print('-------------------------------------------------------------------------------')
    print("df after step 2:")
    print(df.shape)
    print(df.dtypes)

    ###############################PREPROCESS 3#########################################################################

    # Fill in missing values with the median
    df, numberOfMissingNumericalValues = PR.replaceMissingValues(df, list_numericalColumns)
    if numberOfMissingNumericalValues!=0:
        print("-------------------------------------------------------------------------------")
        print(numberOfMissingNumericalValues, " missing numerical values have been replaced.")

    # Get dataframe containing if each row in each numerical column has negative entry
    f=lambda x : (x<0)
    df_negative=F.addColumnsForColumns(df[list_numericalColumns], f, 'negative')

    if selectOption=='Option 1a':
        # Take the absolute value of numerical entries to avoid cancellation when averaging entries
        df[list_numericalColumns] = np.abs(df[list_numericalColumns].values)

    #Save prep 3
    #readFile = readFile + '_prep3'
    #DS.writeToFile_csv(df, F.nameToFileName(readFile), index=index)

    print('-------------------------------------------------------------------------------')
    print("df after step 3:")
    print(df.shape)
    print(df.dtypes)
    #############################PREPROCESS 4 COMMON####################################################################

    if not onlyUserColumns:
        # Add dataframes from step 2 and step 3
        df=pd.concat([df, df_missing, df_negative], axis=1)

        # Add column describing how many missing values were (originally) in each row
        df = df.assign(numMiss=numMiss)
        #Add column describing how many negative values were (originally) in each row
        df = df.assign(numNeg=numNeg)


    if selectOption=='Option 1a':
        from datetime import datetime
        # If no startDate is given, create startDate with first date-entry in df
        if len(startDate) == 0:
            print("-------------------------------------------------------------------------------")
            print("Getting startDate")
            df.sort_index(level=indexVector, inplace=True)
            # Get first date from indexes in dataset on format understood by program
            startDate = [str(datetime.strptime(str(df.index[0]), dateFormat))]
            print("startDate: ", startDate)

        # If no endDate is given, create endDate with last date-entry in df
        if len(endDate) == 0:
            print("-------------------------------------------------------------------------------")
            print("Getting endDate")
            df.sort_index(level=indexVector, inplace=True)
            # Get last date from indexes in dataset on format understood by program
            endDate = [str(datetime.strptime(str(df.last_valid_index()), dateFormat))]
            print("endDate: ", endDate)        

    # Find out if a feature to analyze is set
    # bool, list with name(string) of feature to analyze-columns (external checks)
    hasFeatureToAnalyze, featureToAnalyze = F.nonEmptyIntersection(featureToAnalyze, df.columns.tolist())

    
    if hasFeatureToAnalyze:
        print("-------------------------------------------------------------------------------")
        print("The average will be taken by date (day/month) for each ",
              len(np.unique(df[featureToAnalyze[0]].values)))
        print("unique values in the selected feature to analyze")
        print(np.unique(df[featureToAnalyze[0]].values))
        # Replace all missing entries in featureToAnalyze-column with 'Unknown' before making it an index
        df = PR.replaceNaN(df, featureToAnalyze[0], 'Unknown')
        # Append the feature to analyze as an index in dataframe
        df.set_index(featureToAnalyze[0], inplace=True, append=True)
        # Add column-name of featureToAnalyze as one of the indexes
        indexVector = indexVector + featureToAnalyze
    print('-------------------------------------------------------------------------------')
    print("df after step 4:")
    print(df.shape)
    print(df.dtypes)


    #############################PREPROCESS 4a####################################

    if selectOption == 'Option 1a':
        

        # Get list of all columns containing objects or bools
        list_objectBoolColumns = df.select_dtypes(include=['object', 'bool']).columns.tolist()

        # Remove object-columns containing large number of unique values
        for objectCol in list_objectBoolColumns:
            if len(df[objectCol].unique()) > GC.UNIQUE_TRESHOLD * df.shape[0]:
                print("-------------------------------------------------------------------------------")
                del df[objectCol]
                print(objectCol," has been removed as it may have to many different entries (words) for the computer to handle")

        # Get updated list of all columns containing objects or bools
        #Columns with large number of unique values removed, featureToAnalyze set
        list_objectBoolColumns = df.select_dtypes(include=['object', 'bool']).columns.tolist()
        list_numericalColumns=df.select_dtypes(exclude=['object', 'bool']).columns.tolist()+['numEntries']

        # Create empty dataframe to contain result from all batches
        df_summedByDate = pd.DataFrame()
        numberOfRows = df.shape[0]
        # Count number of each entry before onehotEncoding
        numEntries = df.groupby(indexVector).aggregate('count').iloc[:, 0].copy()
        numEntries.rename('numEntries', inplace=True)
        for r in range(0, numberOfRows, GC.BATCH_SIZE):
            print("--------------------------------------------")
            print("Processing samples ", r + 1, "-", min(r + GC.BATCH_SIZE, numberOfRows), " of ", numberOfRows,
                  "in total.")
            # Small part of original dataframe
            df_batched = df[r:r + GC.BATCH_SIZE]
            # Onehot encode columns with objects or bools
            df_batched = PR.onehotEncode(df_batched, list_objectBoolColumns)
            # Create dataframe where entries are the mean of entries based on date and possibly featureToAnalyze
            df_batched = df_batched.groupby(indexVector).mean()
            # Add zeros to all rows where there were no entries in the original dataframe
            df_batched = F.addEmpty(df_batched, startDate[0], endDate[0], featureToAnalyze, includeDays)
            # Add each batch of summed entries together
            df_summedByDate = pd.concat([df_summedByDate, df_batched], axis=0)
            # Take the mean of the dataframe indexVector to avoid same date from different batches
            df_summedByDate = df_summedByDate.groupby(indexVector).mean()

        # Add column to summed dataframe describing how many entries there were for each date
        df_summedByDate = pd.concat([df_summedByDate, numEntries], axis=1)
        df_summedByDate.fillna(0, inplace=True)
        df = df_summedByDate


        print('-------------------------------------------------------------------------------')
        print("df after step 4a:")
        print(df.dtypes)
        print(df.shape)

    #############################PREPROCESS 4b####################################
    ###LOOK FOR INTERNAL ANOMALIES
    elif selectOption=='Option 1b':

        # Create updated list of object and bool-columns
        list_objectBoolColumns = df.select_dtypes(include=['object', 'bool']).columns.tolist()
        # Create df with column containing objects or bools, make sure every entry is a string
        df_objects = df[list_objectBoolColumns].astype(str)
        # Label encode columns with object-values
        df_labelEncoded = PR.labelEncode(df_objects)
        # Updating df to overwrite objects and bools with label encoded values
        df[list_objectBoolColumns] = df_labelEncoded
        print("-------------------------------------------------------------------------------")
        print("All words now have their own label")

        #Save step 4b
        #readFile = readFile + '_prep4b'
        #DS.writeToFile_csv(df, F.nameToFileName(readFile), index=index)

        print('-------------------------------------------------------------------------------')
        print("df after step 4b:")
        print(df.dtypes)
        print(df.shape)
    #############################ANALYZE 5#########################################################################
    if ninaDemo:
        df_toCheck=df.loc[df.index.get_level_values('Year')==yearToCheck[0]]
        df=df.loc[df.index.get_level_values('Year')==yearToFit[0]]
        monthsToRun=np.arange(1,min(np.nanmax(df.index.get_level_values('Month')), np.nanmax(df_toCheck.index.get_level_values('Month')))+1)
        df_toCheck=df_toCheck.loc[np.isin(df_toCheck.index.get_level_values('Month').values, monthsToRun)]
        df=df.loc[np.isin(df.index.get_level_values('Month').values, monthsToRun)]
        
    #Make loop run once
    month_list=['hello']
    if testMonthsSeparatly and selectOption=='Option 1a':
        # Make list of all unique months in dataframe to fit
        print('-------------------------------------------------------------------------------')
        print("Will fit dataset to each month separatly")
        month_list = np.unique(df.index.get_level_values('Month').values)

    #Make loop run once
    uniqueFeature_list=['hoho']
    if hasFeatureToAnalyze:
        print('-------------------------------------------------------------------------------')
        print("Will fit dataset to each unique value in feature to analyze-column")
        # Make list of all unique feature-to-analyze-values
        uniqueFeature_list = np.unique(df.index.get_level_values(featureToAnalyze[0]).values)
    #Pandas dataframe to hold results
    df_anomalyScore = pd.DataFrame()
    df_anomalyScore_numerical=pd.DataFrame()
    if ninaDemo:
        df_toCheck_anomalyScore=pd.DataFrame()
    i=0
    for month in month_list:
        for feature in uniqueFeature_list:
            #If everything is fitted together
            df_temp = df.copy()
            df_temp_numerical = df[list_numericalColumns].copy()
            print(df_temp.dtypes)
            print(df_temp_numerical.dtypes)
            #If a feature to analyze is set and this needs separate fitting
            if hasFeatureToAnalyze:
                #Make dataframe contain only the current identifier
                df_temp=df_temp.loc[df_temp.index.get_level_values(featureToAnalyze[0]) == feature]
                df_temp_numerical=df_temp_numerical.loc[df_temp_numerical.index.get_level_values(featureToAnalyze[0])==feature]
            if testMonthsSeparatly and selectOption=='Option 1a':
                #Make dataframe contain only the current month
                df_temp = df_temp.loc[df_temp.index.get_level_values('Month') == month]
            # Fitting the model to the dataset
            IF.fit(df_temp)
            # Add column with anomaly-score for each sample
            df_temp = df_temp.assign(anomalyScore=np.round(IF.decision_function(df_temp), decimals=3))
            # Add processed samples together
            df_anomalyScore = pd.concat([df_anomalyScore, df_temp], axis=0)
            if not df_temp_numerical.empty:
                # Fitting the model to the numerical dataset
                IF.fit(df_temp_numerical)
                # Add column with anomaly-score for each sample
                df_temp_numerical = df_temp_numerical.assign(anomalyScore=np.round(IF.decision_function(df_temp_numerical), decimals=3))
                df_anomalyScore_numerical=pd.concat([df_anomalyScore_numerical, df_temp_numerical], axis=0)
            if ninaDemo:
                df_toCheck_temp=df_toCheck.copy()
                if hasFeatureToAnalyze:
                    df_toCheck_temp=df_toCheck_temp.loc[df_toCheck_temp.index.get_level_values(featureToAnalyze[0])==feature]
                df_toCheck_temp=df_toCheck_temp.assign(anomalyScore=np.round(IF.decision_function(df_toCheck_temp), decimals=3))
                df_toCheck_anomalyScore=pd.concat([df_toCheck_anomalyScore, df_toCheck_temp], axis=0)
            i+=1
            if i%5==0:
                print(".")
        if testMonthsSeparatly and selectOption=='Option 1a':
            print(month, ' done ')

    #writeFileAnom = readFile + '_step5a_step6'
    #writeFilePred = readFile + '_step5a_step6_onlyAnomalies'

    df=df_anomalyScore
    df_numerical=df_anomalyScore_numerical
    print('-------------------------------------------------------------------------------')
    print("df after step 5:")
    print(df.dtypes)
    print(df.shape)
    #############################ANALYZE 6####################################
    # Sort values by most anomal
    df.sort_values(by=['anomalyScore'], inplace=True)
    print('-------------------------------------------------------------------------------')
    print("df after step 6:")
    df = AL.addPredictions(df, 'anomalyScore')
    print("Number of predicted anomalies:         ", df.loc[df['predNormal'] == 0].shape[0])
    print("Number of predicted nomalies:          ", df.loc[df['predNormal'] == 1].shape[0])
    print("Percentage of predicted anomalies:     ",
          df.loc[df['predNormal'] == 0].shape[0] / df.shape[0])
    print("Treshold is set to:                    ", GC.TRESHOLD)
    print(df.head())
    print(df.shape)

    if ninaDemo:
        print('-------------------------------------------------------------------------------')
        print("Selected year:")
        print(df_toCheck_anomalyScore.head())
        df_toCheck_anomalyScore=AL.addPredictions(df_toCheck_anomalyScore, 'anomalyScore')
        df_toCheck_anomalyScore.sort_values(by=['anomalyScore'], inplace=True)
        DS.writeToFile_csv(df_toCheck_anomalyScore, F.nameToFileName(readFile+'_2018predicted_basedOn2016_perSourceSystem'), index=index)
    # Save file containing sorted predictions
    DS.writeToFile_csv(df, F.nameToFileName(readFile+'_anomalyScore'), index=index)

    # Save file containing only predicted anomalies
    DS.writeToFile_csv(df.loc[df['predNormal'] == 0], F.nameToFileName(readFile+'_anomalyScoreBelowTreshold'), index=index)


    #############################ANALYZE 6 NUMERICAL PART###########################################################
    if not df_numerical.empty:
        # Sort values by most anomal
        df_numerical.sort_values(by=['anomalyScore'], inplace=True)
        print("-------------------------------------------------------------------------------")
        print("Numerical part:")
        df_numerical = AL.addPredictions(df_numerical, 'anomalyScore')
        print("Number of predicted anomalies:         ",
              df_numerical[df_numerical['predNormal'] == 0].shape[0])
        print("Number of predicted nomalies:          ",
              df_numerical[df_numerical['predNormal'] == 1].shape[0])
        print("Percentage of predicted anomalies:     ",
              df_numerical[df_numerical['predNormal'] == 0].shape[0] /
              df_numerical.shape[0])
        print("Treshold is set to:                    ", GC.TRESHOLD)
        print(df_numerical.head())
        print(df_numerical.shape)
        #writeFileAnom = readFile + '_step5b_step6b'
        # Save file containing sorted predictions for only numerical entries
        DS.writeToFile_csv(df_numerical, F.nameToFileName(readFile+'_anomalyScore_numerical'), index=index)
        #writeFilePred = readFile + '_step5b_step6b_onlyAnomalies'
        # Save file containing only predicted anomalies for only numerical entries
        DS.writeToFile_csv(df_numerical.loc[df_numerical['predNormal'] == 0], F.nameToFileName(readFile+'_anomalyScoreBelowTreshold_numerical'), index=index)

    """
    ******** - 'Option 2': RUNNING CHECK TO SEE IF COLUMNS IN TWO DATASETS (OR THE TOTAL DATASETS)
    ********               HAVE ENTRIES THAT DOES NOT MATCH
    """
elif selectOption == 'Option 2':
   
    ######### Get columns that are in both datasets
    hasCommoncolumns, commonColumns = F.nonEmptyIntersection(df.columns.tolist(), df_old.columns.tolist())
    # Ensure that both dataframes have the same columns
    if hasCommoncolumns:
        df = df[commonColumns]
        df_old = df_old[commonColumns]
        print("-------------------------------------------------------------------------------")
        print("Columns that will be kept in dataset (common for both datasets): ")
        print(df.dtypes)
    else:
        print("-------------------------------------------------------------------------------")
        print("No columns are common for these two files")

    shapeOfDf_old=df_old.shape
    print("-------------------------------------------------------------------------------")
    print("First 5 rows in " + compareFile + " are:")
    print(df_old.head())
    print("This file now has", shapeOfDf_old[0], "rows and", shapeOfDf_old[1], "columns")

    ########Editing indexes (rows) so all id's are in both files
    # Get df and df_old with common id, rows only in df, rows only in df_old
    df, df_old, dfRowsOnly, df_oldRowsOnly=F.getIntersectingAndUniqueRows(df, df_old)
    
    
    if not df_oldRowsOnly.empty:
        print("-------------------------------------------------------------------------------")
        print("There are ", df_oldRowsOnly.shape[0], " rows in compareFile that are not found in readFile:")
        print("these will be saved as a file:")
        # Save dataframe with entries that does not match
        DS.writeToFile_csv(df_oldRowsOnly, F.nameToFileName('rowsIn' + compareFile + '_butNotIn' + readFile), index)
        del df_oldRowsOnly
    else:
        print("-------------------------------------------------------------------------------")
        print("All rows in compareFile are found in readFile")
        del df_oldRowsOnly

    if not dfRowsOnly.empty:
        print("-------------------------------------------------------------------------------")
        print("There are ", dfRowsOnly.shape[0], " rows in readFile that are not found in compareFile,")
        print("these will be saved as a file:")
        # Save dataframe with entries that does not match
        DS.writeToFile_csv(dfRowsOnly, F.nameToFileName('rowsIn' + readFile + '_butNotIn' + compareFile), index)
        del dfRowsOnly
    else:
        print("-------------------------------------------------------------------------------")
        print("All rows in readFile are found in compareFile")
        del dfRowsOnly
    
    #########Ensure that floats have the same precision
    # Numerical remaining columns
    list_numericalColumns = df.select_dtypes(exclude=['bool', 'object']).columns.tolist()
    if len(list_numericalColumns)!=0:
        print("-------------------------------------------------------------------------------")
        print('Values in ',list_numericalColumns, 'will be rounded to 5 decimals.')

        df_old[list_numericalColumns] = AN.deleteSameEntriesByPrecision(df_old, list_numericalColumns)
        df[list_numericalColumns] = AN.deleteSameEntriesByPrecision(df, list_numericalColumns)


    #Make dataframe with dtypes of df and df_old
    df_dtypes=pd.DataFrame({'readFile': df.dtypes, 'compareFile': df_old.dtypes}, index=df_old.dtypes.index)
    #Columns that needs to be made into objects before comparison
    columnsToChange=df_dtypes[df_dtypes['readFile']!=df_dtypes['compareFile']].index.values #indexes to change
    df[columnsToChange]=df[columnsToChange].astype(str)
    df_old[columnsToChange] = df_old[columnsToChange].astype(str)
    if len(columnsToChange!=0):
        print("-------------------------------------------------------------------------------")
        print("There are column(s) that does not have the same datatype in them:")
        print(columnsToChange)
        print("These will be converted to string before comparison.")

    # Get dataframe with entries that are not equal
    df = AN.compareEntriesInDataFrame(df_old, df, 'compareFileEntry', 'readFileEntry')

    if not df.empty:
        print("-------------------------------------------------------------------------------")
        print("There are ", df.shape[0], "entries that should be equal but are not,")
        print("these will be saved as a file:")
        # Save dataframe with entries that does not match
        DS.writeToFile_csv(df, F.nameToFileName(readFile + '_' + compareFile + '_notMatchingEntries'))
    else:
        print("-------------------------------------------------------------------------------")
        print("All entries with the same ID matches")

    """
    ******** - 'Option 3': RUNNING CHECK TO SEE IF ALL ENTRIES IN A COLUMN ARE NOT THE SAME     
    """
elif selectOption == 'Option 3':
    # Find entries that does not match first entry, for selected columns
    df = AN.findEntriesNotTheSame(df)

    if not df.empty:
        # Save dataframe containing which rows does not match, for each column. Includes current and correct values
        print("-------------------------------------------------------------------------------")
        print("Entries that does not match the most occuring entry in the selected column(s):")
        print(df)
        print("-------------------------------------------------------------------------------")
        writeFile = readFile + '_entriesThatDoesNotMatchFirstEntrySelectedColumns'
        DS.writeToFile_csv(df, F.nameToFileName(writeFile))
    else:
        print("-------------------------------------------------------------------------------")
        print("No rows in " + readFile + " for the selected column(s) does not match")
        print("the wanted value")
        print("(wanted value is taken to be the value that occurs most in each column)")