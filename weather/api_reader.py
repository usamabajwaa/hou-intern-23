import requests
import pandas as pd
from datetime import datetime, timedelta

def getYearData():
    
    """
    reads in the API request and uses f-strings to adjust the start date and end date for collecting necessary data.
    the output should be a pandas dataframe containing both the date (format YYYY-MM-DD) and the daily avg temp in Fahrenheit
    dateStart and dateEnd are adjusted after each execution of the for loop due and are re-inserted into the api key parameters
    Might need to update API_url to include API_token depending on how class is being handled
    """
    
    API_url = 'http://api.weatherapi.com/v1/history.json'
    API_token = 'b5d1d68681064ffcb53173100230706'
    
    #Populates the current day and sets a datestart 365 days in the past and sets an end date 30 days after due to api 
    #restrictions set to gathering only ~30 days of data at a time 
    currDate = datetime.date(datetime.now())
    dateStart = currDate - timedelta(days=365)
    dateEnd = dateStart + timedelta(days=30)
    
    #init pandas dataframe
    parameters = ['date', 'avgtemp_f']
    df = pd.DataFrame(columns=parameters)

    for i in range(0, 13):
        result = requests.get(f'{API_url}?key={API_token}&q=Houston&dt={dateStart}&end_dt={dateEnd}')
        result_dict = dict(result.json())
        if result_dict == None: break

        #For loop checks the dictionary for the necessary values and stores them into a new_row dataframe, it is then
        #transposed and concat'd with the pre-existing dataframe
        for i in range(len(result_dict['forecast']['forecastday'])):
            date = result_dict['forecast']['forecastday'][i]['date']
            avgTempF = result_dict['forecast']['forecastday'][i]['day']['avgtemp_f']
            
            new_row = pd.DataFrame([date, avgTempF], index=parameters).T
            df = pd.concat([df,new_row], ignore_index=True)

        dateStart = dateEnd + timedelta(days=1)
        dateEnd = dateStart + timedelta(days=30)

        if dateEnd >= datetime.date(datetime.now()): dateEnd = datetime.date(datetime.now())
        
    return df
