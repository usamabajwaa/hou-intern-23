import pandas as pd
from api_reader import getYearData

# Create and define the class
class WeatherViz:

    #Initialize class with method to define instance variables
    def __init__(self, API_url):

        # Assign API_url to instance variable 
        self.API_url = API_url

        # Create empty dataframe as instance variable 
        self.data_frame = pd.DataFrame()
        
        #Create empty month data frame as instance variable 
        self.monthly_df = pd.DataFrame()
        
    def yearData(self, API_url):
        self.data_frame = getYearData(API_url)
