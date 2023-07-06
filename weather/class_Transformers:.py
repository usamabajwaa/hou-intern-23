import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

class Transformers:

    def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:

        df = df[["Creator Name", "Desk Name", "Start (UTC)", "Canceled At (UTC)"]]

        return df

    def group_data(df: pd.DataFrame) -> pd.DataFrame:

        df = df.groupby(["Start (UTC)", "Creator Name"])

        return df
    
    def add_missing_days(self, df: pd.DataFrame) -> pd.DataFrame:

        ## Convert 'Start (UTC)' column to datetime format
        df['Start (UTC)'] = pd.to_datetime(df['Start (UTC)'])

        # Find the minimum and maximum dates in the dataframe
        min_date = df['Start (UTC)'].min()
        max_date = df['Start (UTC)'].max()

        # Generate a list of all weekdays between the minimum and maximum dates
        all_days = pd.date_range(start=min_date, end=max_date, freq='B').date

        # Add missing days to the dataframe where there were no desks booked
        missing_days = np.setdiff1d(all_days, df['Start (UTC)'].dt.date)
        missing_data = pd.DataFrame({'Start (UTC)': missing_days, 'Creator Name': 'No Booking', 'Desk Name': 'No Booking', 'Canceled At (UTC)': np.nan})
        df = pd.concat([df, missing_data], ignore_index=True)
        # Sort the dataframe by 'Start (UTC)' column
        df = df.sort_values(by='Start (UTC)')
        
        return df
        