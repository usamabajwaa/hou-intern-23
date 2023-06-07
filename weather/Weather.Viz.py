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

    def get_data(self): 
        # Define the headers for API request
        headers = {
            'Authorization' : f'Bearer {self.API_token}',
        }

        # Send GET request to the API_url with the headers
        response = requests.get(self.API_url, headers=headers)

        # Check that the GET request was successful. If not, raise an error. 
        if response.status_code != 200: 
            raise Exception(f"GET request to {self.API_URL} failed with status code {response.status_code}")
        
        # Convert the JSON response to a dictionary
        data = response.json()

        # Convert the data dictionary to a DF and return it 
        data_frame = pd.DataFrame(data)

        return data_frame