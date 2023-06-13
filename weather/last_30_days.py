import matplotlib.pyplot as plt 
import pandas as pd
from api_reader import getYearData

# Create function with 'self' parameter referring to instance of class

def plotData(self): 

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

    





