import pytest
import pandas as pd
from weather_visualization import WeatherViz
import matplotlib.pyplot as plt

#def test_disable_matplotlib_show():
    #plt.ioff()
    #yield
    #plt.ion()

def test_plot_average_monthly_temeprature():
    monthly_df = pd.DataFrame({
        'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'avg_temp': [20, 25, 30, 44, 22, 19, 75, 80, 90, 67, 54, 65]
    })
    # create instance of WeatherViz
    weather_visualization= WeatherViz('http://api.weatherapi.com/v1/history.json')
    weather_visualization.plotAverageMonthlyTemperature(monthly_df)
    
    # check title of plot is right
   # assert WeatherViz.ax.get_title() == "Downtown Houston\'s Average Monthly Temperature for 2023"
    plt.close()