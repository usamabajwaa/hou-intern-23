import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import config


class Transformers:

    def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:

        df = df[["Creator Name", "Desk Name", "Start (UTC)", "Canceled At (UTC)"]]

        return df

    def group_data(df: pd.DataFrame) -> pd.DataFrame:
        #renaming the columns 
        df = df.rename(columns={'Start (UTC)': 'date', 'Creator Name': 'creator'})
        
        #groupby works by exact matching, so we need to strip the timestamp
        # df['date'] = df['date'].dt.date
        
        #groupby 'date' and organize 'creator' column into date subgroups
        df = df.groupby('date')['creator']
        

        df = df.sort_values(["Start (UTC)", "Creator Name"])

        return df
    
    def add_missing_days(df: pd.DataFrame) -> pd.DataFrame:

        ## Convert 'Start (UTC)' column to datetime format
        df['Start (UTC)'] = df['Start (UTC)'].dt.date

        # Find the minimum and maximum dates in the dataframe
        min_date = df['Start (UTC)'].min()
        max_date = df['Start (UTC)'].max()

        # Generate a list of all weekdays between the minimum and maximum dates
        all_days = pd.date_range(start=min_date, end=max_date, freq='B').date

        # Add missing days to the dataframe where there were no desks booked
        missing_days = np.setdiff1d(all_days, df['Start (UTC)'])
        missing_data = pd.DataFrame({'Start (UTC)': missing_days, 'Creator Name': 'No Booking', 'Desk Name': 'No Booking', 'Canceled At (UTC)': np.nan})
        df = pd.concat([df, missing_data], ignore_index=True)
        # Sort the dataframe by 'Start (UTC)' column
        df = df.sort_values(by='Start (UTC)')
        
        return df

    def group_bookings_data(df: pd.DataFrame) -> pd.DataFrame:
        
        #perform a summing operation on the groupby object by counting unique elements (assuming you cant book the same day more than once)
        df = df.nunique().reset_index(name='bookings_count')
            
        return df
    
    def add_water_column(df: pd.DataFrame) -> pd.DataFrame:
        
        df['water_usage'] = df.bookings_count * config.avg_water_consumption
        
        return df
    
    def add_commute_emissions(df: pd.DataFrame) -> pd.DataFrame:

        # Copy df to avoid SettingWithCopyWarning
        df = df.copy()

        # Count 'Creator Name' entries to get a number of employees 
        num_employees = df.groupby(df['Start (UTC)'].dt.date)['Creator Name'].nunique()

        # Calculate total commute emissions emissions for each day
        commute_emissions = num_employees * config.avg_commute_score

        # Add new column to df
        df['commute_emissions'] = df['Start (UTC)'].dt.date.map(commute_emissions)
        
        return df
    

        
    

    
    

    
        