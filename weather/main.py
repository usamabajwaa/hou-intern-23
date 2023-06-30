from weather_visualization import WeatherViz
# from connector_class import Connector

if __name__== "__main__":
    # connector_df = Connector()
    # print(connector_df.db_df)
    
    weather_viz = WeatherViz('http://api.weatherapi.com/v1/history.json')
    weather_viz.yearData('http://api.weatherapi.com/v1/history.json')
    # weather_viz.monthly_df = weather_viz.calculateMonthlyAverages(weather_viz.data_frame)
    # weather_viz.yearVizData(weather_viz.data_frame)
    # weather_viz.plotLast30Days()
    # weather_viz.plotAverageMonthlyTemperature(weather_viz.monthly_df)

    weather_viz.weekly_df = weather_viz.calculateWeeklyAverages(weather_viz.data_frame)
    weather_viz.plotAverageWeeklyTemperature(weather_viz.weekly_df) 