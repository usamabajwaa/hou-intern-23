import requests
import pandas as pd
from datetime import datetime, timedelta

def getYearData(API_url):
    
    """Fetches 365 days worth of historical data (date and temperature in Fahrenheit) from API provided.

    API url is polled in 30 day increments and the necessary data is extracted and appended to a pandas
    dataframe. The API paremeters are then updated and this process repeats until 365 days of historical
    data has been extracted.
    
    Args:
        API_url: provides an API url and key thast is then f-stringed into the url request.
        
    Returns:
        a pandas dataframe containing 365 days and their corresponding temperature is returned to the Weather.Viz.py file
    """
    
    #Populates the current day and sets a datestart 365 days in the past and sets an end date 30 days after due to api 
    #restrictions set to gathering only ~30 days of data at a time 
    currDate = datetime.date(datetime.now())
    dateStart = currDate - timedelta(days=365)
    dateEnd = dateStart + timedelta(days=30)
    
    #init pandas dataframe
    parameters = ['date', 'avgtemp_f']
    df = pd.DataFrame(columns=parameters)

    for i in range(0, 13):
        result = requests.get(f'{API_url}?key=b5d1d68681064ffcb53173100230706&q=Houston&dt={dateStart}&end_dt={dateEnd}')
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
