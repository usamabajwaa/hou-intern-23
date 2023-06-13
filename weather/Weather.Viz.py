from matplotlib import  dates, pyplot as plt
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
    
def yearVizData(yearData):

    #Sets up and autoscales the window to a larger size for readbabilit
    fig = plt.figure(figsize=(20, 7), dpi=100)
    ax = fig.subplots()
    
    ax.plot(yearData.data_frame['date'], yearData.data_frame['avgtemp_f'])
    
    #Sets X-axis increments
    ax.xaxis.set_major_locator(dates.DayLocator(interval=14)) #Sets major tick marks on x-axis to once every month
    ax.xaxis.set_minor_locator(dates.DayLocator()) #Sets minor tick marks on x-axis to once every week
        
    ax.set(xlabel = 'Date', ylabel = 'Avg Temp (°F)', title = 'Historical Data Showing Avg Temp (°F) for Past 365 Days')

    #Displays grid and formats x-axis test
    plt.grid(which = 'both', axis='x')
    plt.grid(which = 'both', axis='y')
    plt.gcf().autofmt_xdate()
    plt.show()

test = WeatherViz('http://api.weatherapi.com/v1/history.json')
test.yearData(test.API_url)
testGraph = yearVizData(test)
