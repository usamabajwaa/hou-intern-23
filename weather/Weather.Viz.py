# Import necessary libraries 
import pandas as pd 
import requests 

# Create and define the class
class Weather_Viz: 
    def __init__(self, API_url, API_token):
        # Initiate the API_url and API_token
        self.API_url = API_url
        self.API_token = API_token
        # Fetch the data and store it in the DF propetry
        self.data_frame = self.get_data()