from weather_visualization import WeatherViz
from connector_class import Connector,Transformers
import argparse

if __name__== "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--use_csv', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    use_csv = bool(args.use_csv)
    verbose = bool(args.verbose)

    print("Arguments:")
    print("\tuse_csv:",use_csv)
    print("\tverbose:",verbose)

    if verbose:
        print("Loading data")

    connector_df = Connector(use_csv = use_csv, verbose=verbose)
    if verbose:
        print(connector_df.db_df)

    if verbose:
        print("Transforming data")

    transformer_df = Transformers.drop_unused_columns(connector_df.db_df)
    transformer_df = Transformers.group_data(transformer_df)

    if verbose:
        print("Visualzing weather data")

    weather_viz = WeatherViz('http://api.weatherapi.com/v1/history.json')
    weather_viz.yearData('http://api.weatherapi.com/v1/history.json')
    weather_viz.monthly_df = weather_viz.calculateMonthlyAverages(weather_viz.data_frame)
    weather_viz.yearVizData(weather_viz.data_frame)
    weather_viz.plotLast30Days()
    weather_viz.plotAverageMonthlyTemperature(weather_viz.monthly_df)