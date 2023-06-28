from matplotlib import  dates, pyplot as plt
import pandas as pd
from api_reader import getYearData
from datetime import datetime
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine


class Connector:
        
    def db_connector(self):
        """generic SQL connector that queries a db and saves result to a dataframe
        This function populates the Connector class database dataframe with whatever parameters are passed to the engine function
        and also whatever the query provided is. Please note that you need to use a .env file and assign the correct values in 
        the file to match the following sqlalchemy engine syntax:
        
        {dialect}+{driver}://{username}:{password}@{host_name}:{port_number}/{database_name}

        Returns:
            db_df: the database transleted into a pandas dataframe
        """
        
        #gets .env variables to access your database
        load_dotenv()
        host = os.getenv('host_name')
        dbname = os.getenv('db_name')
        user = os.getenv('user_name')
        password = os.getenv('user_password')
        port = os.getenv('port_number')
        dialect = os.getenv('dialect')
        driver = os.getenv('driver')
        
        #populates engine to access Postgres database 
        engine = create_engine(f'{dialect}+{driver}://{user}:{password}@{host}:{port}/{dbname}', pool_recycle=3600)
        db_conn = engine.connect()
        
        #if needed to change query, do so here
        db_df = pd.read_sql_query('SELECT * FROM desks_90', con=db_conn)
        
        return db_df
    
    def __init__(self):
        self.db_df = self.db_connector()
        

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

    def plotLast30Days(self): 
        # Check if the dataframe is empty
        
        if self.data_frame.empty: 
            print("There is no data available to display")
            return
        
        # Check for enough data in dataframe to actually plot the last 30 days
        
        if self.data_frame.shape[0] < 30: 
            print("There is not enough data to display the last 30 days")
            return
        
        """ After all checks have been passed, select the last 30 days
        of data and store it in variable
        last_30_days_df
        """
        last_30_days_df = self.data_frame.tail(30)

        """ After storage, convert the 'date' column from string format to datetime format
        for plotting on x-axis
        """
        last_30_days_df['date'] = pd.to_datetime(last_30_days_df['date'])

        # Sort the dataframe by 'date' so the plot displays data in chronological order
        last_30_days_df = last_30_days_df.sort_values(by='date')

        # Create a figure 
        plt.figure(figsize=(10, 5)) 
        # Plot the data
        plt.plot(last_30_days_df['date'], last_30_days_df['avgtemp_f'], marker='o')
        # Label for x-axis 
        plt.xlabel('Date')
        # Label for y-axis
        plt.ylabel('Average Temperature (°F)')
        # Give the plot a title
        plt.title('Average Daily Temperature in Downtown Houston Over the Last 30 Days')
        # Enable the grid
        plt.grid(True)
        plt.gcf().autofmt_xdate()
        # Finally, display the grid
        plt.show()

    def calculateMonthlyAverages(self, df: pd.DataFrame):
        """
        Calculates monthly average weather given datafram of last 365 days
        
        Args: pandas DataFrame containg daily temp data
        
        Returns:
     New pandas DataFrame called mnonthly_df with colums month and avgtemp_f which has the mnonthly
     average temps"""
        parameters = ['date', 'month', 'avgtemp_f']
        monthly_df = pd.DataFrame(columns=parameters)
        monthly_df['date'],monthly_df['avgtemp_f'] = df['date'],df['avgtemp_f']
        
        # convert 'date'column to datetime format
        monthly_df['date'] = pd.to_datetime(monthly_df['date'], format='%Y-%m-%d')
        # Extract month and avg temp data
        monthly_df['month'] = monthly_df['date'].dt.month
        monthly_df = monthly_df.groupby(['month'])['avgtemp_f'].mean().reset_index()
        #rename columns
        monthly_df.rename(columns={'avgtemp_f': 'avg_temp'}, inplace=True)

        return monthly_df
        
    def yearVizData(self, yearData: pd.DataFrame):

        #Sets up and autoscales the window to a larger size for readbabilit
        fig = plt.figure(figsize=(20, 7), dpi=100)
        ax = fig.subplots()
    
        ax.plot(yearData['date'], yearData['avgtemp_f'])
    
        #Sets X-axis increments
        ax.xaxis.set_major_locator(dates.DayLocator(interval=14)) #Sets major tick marks on x-axis to once every month
        ax.xaxis.set_minor_locator(dates.DayLocator()) #Sets minor tick marks on x-axis to once every week
        
        ax.set(xlabel = 'Date', ylabel = 'Avg Temp (°F)', title = 'Historical Data Showing Downtown Houston\'s Average Temperature (°F) for Past 365 Days')

        #Displays grid and formats x-axis test
        plt.grid(which = 'both', axis='x')
        plt.grid(which = 'both', axis='y')
        plt.gcf().autofmt_xdate()
        
        return plt
        
        
    #plots average monthly temp
    def plotAverageMonthlyTemperature(self, monthly_df: pd.DataFrame):
        """
        Plots the average monthly temperature for the last year using a line chart.

        Args:
            monthly_df: A pandas DataFrame containing the average monthly temperatures.

        Returns:
            None (displays the line chart using matplotlib).
        """
        # Extract month and average temperature data
        months = monthly_df['month']
        avg_temp = monthly_df['avg_temp']
    
        # Set up the figure and axes
        fig, ax = plt.subplots()
    
        # Plot the line chart
        ax.plot(months, avg_temp, marker='o', linestyle='-', color='blue')
    
        # Set labels and title
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Temperature °F')
        ax.set_title('Downtown Houston\'s Average Monthly Temperature for 2023')
    
        # Set x-axis ticks and labels
        ax.set_xticks(months)
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
        # Display the chart
        plt.grid()
        plt.show()
        
if __name__== "__main__":
    connector_df = Connector()
    
    weather_viz = WeatherViz('http://api.weatherapi.com/v1/history.json')
    weather_viz.yearData('http://api.weatherapi.com/v1/history.json')
    weather_viz.monthly_df = weather_viz.calculateMonthlyAverages(weather_viz.data_frame)
    weather_viz.yearVizData(weather_viz.data_frame)
    weather_viz.plotLast30Days()
    weather_viz.plotAverageMonthlyTemperature(weather_viz.monthly_df)