from weather_visualization import WeatherViz
from connector_class import *

if __name__== "__main__":
    connector_df = Connector()
    transformer_df = Transformers()
    
    transformer_df.data = transformer_df.drop_unused_columns(connector_df.db_df)
    transformer_df.data = transformer_df.group_data(transformer_df.data)
    
    weather_viz = WeatherViz('http://api.weatherapi.com/v1/history.json')
    weather_viz.yearData('http://api.weatherapi.com/v1/history.json')
    weather_viz.monthly_df = weather_viz.calculateMonthlyAverages(weather_viz.data_frame)
    weather_viz.yearVizData(weather_viz.data_frame)
    weather_viz.plotLast30Days()
    weather_viz.plotAverageMonthlyTemperature(weather_viz.monthly_df)