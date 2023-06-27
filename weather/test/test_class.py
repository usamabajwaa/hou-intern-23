from weather_visualization import WeatherViz
import pandas as pd
import matplotlib.pyplot as plt
################################
# Saving these for later for mock testing
# import pytest
# import unittest.mock as mock
# import unittest
################################


def test_yearVizData():
       #Populates a dictionary with 365 instances of a date and temp (temp is constant)
       sample_data = {
              'date': pd.date_range(start='2022-01-01', periods=365),
              'avgtemp_f': [10] * 365  
       }
       year_data = pd.DataFrame(sample_data)

       #inits test obj
       test_obj = WeatherViz('http://api.weatherapi.com/v1/history.json')
       test_plt = test_obj.yearVizData(year_data)
       # test_plt.show()
       #Asserts the plt is not empty after being passed to yearVizData func
       assert test_plt != None
       

