import matplotlib.pyplot as plt
import pandas as pd

data = {
    'month' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'avg_temp': [45, 48, 52, 58, 65, 66, 67, 68, 75, 23, 44, 35]
}
monthly_df = pd.DataFrame(data)

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


plotAverageMonthlyTemperature(monthly_df)