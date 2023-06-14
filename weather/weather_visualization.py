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

    # Create function with 'self' parameter referring to instance of class

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
        plt.ylabel('Average Temperature (F)')
        # Give the plot a title
        plt.title('Average Daily Temperature Over the Last 30 Days')
        # Enable the grid
        plt.grid(True)
        # Finally, display the grid
        plt.show()

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

        #plots average monthly temp

    def plotAverageMonthlyTemperature(monthly_df):
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
        ax.set_ylabel('Average Temperature')
        ax.set_title('Average Monthly Temperature for the Last Year')
    
        # Set x-axis ticks and labels
        ax.set_xticks(months)
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
        # Display the chart
        plt.show()