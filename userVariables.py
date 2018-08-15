#########  PLEASE REFER TO THE USER MANUAL WHEN SETTING THESE VARIABLES.
#########  THE COMMENTING IS ONLY TO HELP THOSE THAT ARE FAMILIAR WITH
#########  THE PROGRAM AND SHOULD NOT BE USED INSTEAD OF THE USER MANUAL

"""
**********************************************************************************************
********WRITE NAME OF FILE WITH NAME readFile                     
********MUST BE .csv-FILE SEPARATED BY ,                
********EXAMPLE:                                       
********readFile='myFile'           
"""
readFile=''

"""
**********************************************************************************************
********SELECT BETWEEN
******** - 'Option 1a': RUNNING THE ANOMALY-DETECTION PROGRAM FOR GLOBAL ANOMALIES
******** - 'Option 1b': RUNNING THE ANOMALY-DETECTION PROGRAM FOR LOCAL ANOMALIES                    
******** - 'Option 2': RUNNING CHECK TO SEE IF COLUMNS IN TWO DATASETS (OR THE TOTAL DATASETS)
********               HAVE ENTRIES THAT DOES NOT MATCH
******** - 'Option 3': RUNNING CHECK TO SEE IF ALL ENTRIES IN A COLUMN ARE NOT THE SAME (THE VALUE THAT 
********               OCCURS THE MOST IS TAKEN TO BE CORRECT)    
********EXAMPLE:                                       
********selectOption = 'Option 2'
"""
selectOption = ''

"""
**********************************************************************************************
********IF  YOU CHOSE 'Option 2' IN THE ABOVE SECTION,
********PLEASE WRITE NAME OF FILE WITH NAME compareFile
********MUST BE .csv-FILE SEPARATED BY ,                
********EXAMPLE:                                       
********compareFile='myOldFile' 
"""
compareFile =''

"""
**********************************************************************************************
********DO YOU WANT TO WRITE WHICH COLUMNS TO KEEP                                  
********OR WRITE WHICH COLUMNS TO DELETE? ('keep'/'delete')                         
********IF YOU WANT TO KEEP ALL COLUMNS, WRITE 'all'                                
********EXAMPLE:                                                                    
********keepOrDelete='keep'                                                         
"""
keepOrDelete = 'all'

"""
**********************************************************************************************
********IF YOU DECIDED keepOrDelete='keep', WRITE NAME OF COLUMNS IN DATASET  
********YOU WANT TO KEEP AS A LIST WITH NAME selectedColumns                  
********EXAMPLE:                                                              
********keepColumns=['Column1', 'Column2', 'Column4']                         
********
********IF YOU DECIDED keepOrDelete='delete', WRITE NAME OF COLUMNS IN DATASET  
********YOU WANT TO DELETE AS LIST WITH NAME deleteColumns                      
********EXAMPLE:                                                                
********deleteColumns=['Column1', 'Column3', 'Column4']                         
"""
keepColumns = []
deleteColumns = []

"""
**********************************************************************************************
********IF YOU WANT TO CHANGE NAMES OF COLUMNS, WRITE NEW NAMES             
********IN DICTIONARY renameColumns                                         
********EXAMPLE:                                                            
********renameColumns={'Column1':'NewNameColumn1', 'Column2':'NewNameColumn2'}
"""
renameColumns ={}

"""
**********************************************************************************************
********WRITE NAME OF COLUMN CONTAINING DATE TO USE        
********WHEN LOOKING AT DATASET OVER TIME  
*******AS A LIST WITH NAME dateColumn                    
********EXAMPLE:                                        
********dateColumn=['RecordingDate']                    
"""
dateColumn = []

"""
**********************************************************************************************
********TO DESCRIBE THE DATE THERE WILL BE MADE A COLUMN WITH
********WHICH YEAR THE SAMPLE WERE TAKEN, AND WHICH MONTH THE 
********SAMPLE WERE TAKEN
********WOULD YOU LIKE TO HAVE A COLUMN WITH THE DAY AS WELL?
********IF SO, SET 'includeDays' to 'True'
********EXAMPLE:                                        
********includeDays=True
"""
includeDays = False

"""
**********************************************************************************************
********WRITE DOWN THE FIRST DATE THAT SHOULD BE AN AN ENTRY 
********IN THE DATASET AS startDate, 
********AND THE LAST DATE THAT SHOULD BE AN ENTRY IN THE
********DATASET AS endDate 
********IF NO DATES ARE GIVEN, THE PROGRAM WILL USE THE  
********FIRST AND LAST DATES IT FINDS (this takes longer
********and it is therefore beneficial to enter the dates)
********FORMAT: ['m/d/yyyy']
********EXAMPLE:                                        
********startDate=['12/26/1994']
********endDate=['7/24/2018']
"""
startDate = []
endDate = []

"""
**********************************************************************************************
********WRITE NAME OF COLUMN CONTAINING UNIQUE IDENTIFICATION
********FOR EACH ROW, SO THAT IT'S EASY FOR YOU TO KNOW
********WHICH SAMPLES HAVE BEEN LABELED AS ABNORMAL
********WHEN THE PROGRAM HAS DONE IT'S CALCUlATIONS.
********EXAMPLE:                                        
********identifierColumn=['Row_Id']
"""
identifierColumn = []

"""
**********************************************************************************************
********WRITE DATE YOU WANT TO DO LOCAL CHECK FOR ANOMALIES
********ON FORMAT [yyyy,m,d]
********OR [yyyy,m],
********EXAMPLE FOR WHEN YOU HAVE 'includeDays=True':                                        
********dateInternalCheck=[2018,12,26]
********EXAMPLE FOR WHEN YOU HAVE 'includeDays=False':                                        
********dateInternalCheck=[2018,12]
********UPDATE: Can test a month when includeDays=True
"""
dateInternalCheck = []

"""
**********************************************************************************************
********WRITE NAME OF COLUMNS CONTAINING NUMBERS THAT ARE 
********ACTUALLY NOT NUMBERS (example: In an identification-column
********the value 8 could represent the country Norway, and should
********be treated as if the column contained 'Norway' instead of '8')
********EXAMPLE:                                        
********numberThatIsReallyWordColumns=['buying_Id', 'country_id']
"""
numberThatIsReallyWordColumns = []

"""
**********************************************************************************************
********WRITE NAME OF COLUMN CONTAINING FEATURE TO LOOK AT
********LEAVE IT EMPTY IF YOU DON'T WANT TO LOOK AT ANYTHING
********IN PARTICULAR
********FOR EXTERNAL CHECKS
********EXAMPLE:                                        
********featureToAnalyze=['From_Country']
"""
featureToAnalyze = []

"""
**********************************************************************************************
********DO YOU WANT TO TEST EACH MONTH SEPARATLY?
********IF SO, SET testMonthsSeparatly=True
"""
testMonthsSeparatly = False

"""
**********************************************************************************************
********DO YOU WANT TO ONLY LOOK AT YOUR SELECTED COLUMNS?
********IF SO, SET onlyUserColumns=True
"""
onlyUserColumns = False

"""
**********************************************************************************************
********THE CODE BELOW IS NOT INTENDED TO BE USED, AND IS ONLY INCLUDED FOR DEMONSTRATION
********PURPOSES. IF YOU WISH TO USE FUNCTIONALITY THE VARIABLES BELOW OFFER,
********PLEASE CONTACT SOMEONE WHO IS FAMILIAR WITH THE CODE IN THIS PROGRAM
"""
#fill in if you want to fit algorithm to only one other year
yearToCheck=[2016]
yearToFit=[2018]

ninaDemo=False