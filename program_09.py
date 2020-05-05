#!/bin/env python
"""
2020/05/04
by Charles Huang

Lab9 - Automated Data Quality Checking with Python

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    DataDF.replace(-999,np.nan,inplace = True) # replace -999 to nan
    # record the number of values replaced for each data type in index 1
    ReplacedValuesDF.loc['1. No Data',:] = DataDF.isna().sum()

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # Check for gross errors and apply the following error thresholds
    # 0 <= P <=25
    DataDF['Precip'][(DataDF['Precip'] < 0)|(DataDF['Precip'] >25)]=np.nan
    #-25<=T <=35
    DataDF['Max Temp'][(DataDF['Max Temp'] < -25)|(DataDF['Max Temp'] >35)]=np.nan
    DataDF['Min Temp'][(DataDF['Min Temp'] < -25)|(DataDF['Min Temp'] >35)]=np.nan
    #0 <=WS <= 10
    DataDF['Wind Speed'][(DataDF['Wind Speed'] < 0)|(DataDF['Wind Speed'] >10)]=np.nan
    
     # record the number of values replaced for each data type in index 2
    check01count= ReplacedValuesDF.sum()
    ReplacedValuesDF.loc["2. Gross Error", :] = DataDF.isna().sum() - check01count
    

    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # Swap and count
    count = 0
    sum_T=0
    for i in range (0,(len(DataDF)-1)):
        if DataDF['Max Temp'][i] < DataDF['Min Temp'][i]:
            sum_T = DataDF['Max Temp'][i] + DataDF['Min Temp'][i]
            DataDF['Max Temp'][i] = DataDF['Min Temp'][i]
            DataDF['Min Temp'][i] = sum_T - DataDF['Max Temp'][i]
            count = count + 1
    
    ReplacedValuesDF.loc["3. Swapped", :] = [0,count,count,0]

    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # replace invalid data and count
    count = 0
    for i in range (0,(len(DataDF)-1)):
        if DataDF['Max Temp'][i] - DataDF['Min Temp'][i] >25:
           DataDF['Max Temp'][i] =  np.nan
           DataDF['Min Temp'][i] = np.nan
           count = count + 1

    ReplacedValuesDF.loc["4. Range Fail", :] = [0,count,count,0]
     

    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    
  
    # recall the original data  
    Data, ReplacedValues = ReadData(fileName)

    #Plot of precipitation
    plt.plot(DataDF.index, Data['Precip'], label = "before check") 
    plt.plot(DataDF.index, DataDF['Precip'], label = "after check") 
    plt.xlabel('date')
    plt.ylabel('precipitation (mm)')
    plt.title('Precipitation')
    plt.legend()
    plt.show()
    plt.savefig('precip.jpg')
    plt.close()

    #Plot of max temperature
    plt.plot(DataDF.index, Data['Max Temp'], label = "before check") 
    plt.plot(DataDF.index, DataDF['Max Temp'], label = "after check") 
    plt.xlabel('date')
    plt.ylabel('maximum air temperature (°C)')
    plt.title('Maximum Air Temperature')
    plt.legend()
    plt.show()
    plt.savefig('max_Temp.jpg')
    plt.close()


    #Plot of min temperature
    plt.plot(DataDF.index, Data['Min Temp'], label = "before check") 
    plt.plot(DataDF.index, DataDF['Min Temp'], label = "after check") 
    plt.xlabel('date')
    plt.ylabel('minimum air temperature (°C)')
    plt.title('Minimum Air Temperature')
    plt.legend()
    plt.show()
    plt.savefig('min_temp.jpg')
    plt.close()

    #Plot of wind speed
    plt.plot(DataDF.index, Data['Wind Speed'], label = "before check") 
    plt.plot(DataDF.index, DataDF['Wind Speed'], label = "after check") 
    plt.xlabel('date')
    plt.ylabel('wind speed (m/s)')
    plt.title('Wind Speed')
    plt.legend()
    plt.show()
    plt.savefig('wind_speed.jpg')
    plt.close()

    # output after check files
    DataDF.to_csv("After_check_data.txt", sep = " ")
    ReplacedValuesDF.to_csv("Corrections_made_info.csv", sep = "\t")    
 