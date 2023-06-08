import requests
from datetime import datetime, timedelta

def getYearData():
    
    """
    reads in the API request and uses f-strings to adjust the start date and end date for collecting necessary data.

    the output should be both a date (format YYYY-MM-DD) and the daily avg temp in Fahrenheit

    dateStart and dateEnd are adjusted after each execution of the for loop due and are re-inserted into the api key parameters
    """
    
    #Populates the current day and sets a datestart 365 days in the past and sets an end date 30 days after due to api 
    #restrictions set to gathering only ~30 days of data at a time 
    currDate = datetime.date(datetime.now())
    dateStart = currDate - timedelta(days=365)
    dateEnd = dateStart + timedelta(days=30)
    
    for i in range(0, 13):
        result = requests.get(f'http://api.weatherapi.com/v1/history.json?key=b5d1d68681064ffcb53173100230706&q=Houston&dt={dateStart}&end_dt={dateEnd}')
        result_dict = dict(result.json())
        if result_dict == None: break

        for i in range(len(result_dict['forecast']['forecastday'])):
            print(f"Date: {result_dict['forecast']['forecastday'][i]['date']}")
            print(f"Temp: {result_dict['forecast']['forecastday'][i]['day']['avgtemp_f']}°F\n")
            
        dateStart = dateEnd + timedelta(days=1)
        dateEnd = dateStart + timedelta(days=30)

        if dateEnd >= datetime.date(datetime.now()): dateEnd = datetime.date(datetime.now())
        
getYearData()