import pandas as pd
from api_reader import getYearData

# Create and define the class
class Weather_Viz:

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

    def calculateMonthlyAverages(self, df):
        """
        Calculates monthly average weather given datafram of last 365 days
        
        Args: pandas DataFrame containg daily temp data
        
        Returns:
     New pandas DataFrame called mnonthly_df with colums month and avgtemp_f which has the mnonthly
     average temps"""
        
        # convert 'date'column to datetime format
        df['date'] = pd.to_datetime(df['date'])

        # Extract month and avg temp data
        df['month'] = df['date'].dt.month
        monthly_df = df.groupby(['month'])['avgtemp_f'].mean().reset_index()

        #rename columns
        monthly_df.rename(columns={'avgtemp_f': 'avg_temp'}, inplace=True)

        return monthly_df