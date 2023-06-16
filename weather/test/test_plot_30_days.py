import pandas as pd
import pytest
from weather_visualization import WeatherViz

# Test 'plotLast30Days' with no data
def test_plot_last_30_days_no_data():
    weather_viz = WeatherViz('http://api.weatherapi.com/v1/history.json')
    # Check if RuntimeError is raised
    with pytest.raises(RuntimeError) as excinfo:  
        weather_viz.plotLast30Days()
    # Assert the error message
    assert str(excinfo.value) == 'There is no data available to display'

# Test 'plotLast30Days' with insufficient data
def test_plot_last_30_days_insufficient_data():
    weather_viz = WeatherViz('http://api.weatherapi.com/v1/history.json')
    # Create a DataFrame with less than 30 days of data
    weather_viz.data_frame = pd.DataFrame({'date': pd.date_range(start='1/1/2020', end='1/15/2020'), 'avgtemp_f': range(15)})
    # Check if RuntimeError is raised
    with pytest.raises(RuntimeError) as excinfo:  
        weather_viz.plotLast30Days()
    # Assert the error message
    assert str(excinfo.value) == 'There is not enough data to display the last 30 days'