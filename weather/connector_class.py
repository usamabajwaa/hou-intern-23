import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine


class Connector:
    def db_connector(self, verbose) -> pd.DataFrame():
        """generic SQL connector that queries a db and saves result to a dataframe
        This function populates the Connector class database dataframe with whatever parameters are passed to the engine function
        and also whatever the query provided is. Please note that you need to use a .env file and assign the correct values in
        the file to match the following sqlalchemy engine syntax:

        {dialect}+{driver}://{username}:{password}@{host_name}:{port_number}/{database_name}

        Returns:
            db_df: the database translated into a pandas dataframe
        """

        # gets .env variables to access your database
        load_dotenv()
        host = os.getenv("host_name")
        dbname = os.getenv("db_name")
        user = os.getenv("user_name")
        password = os.getenv("user_password")
        port = os.getenv("port_number")
        dialect = os.getenv("dialect")
        driver = os.getenv("driver")

        if verbose:
            print("host", host)
            print("dbname", dbname)
            print("user", host)
            print("password", password)
            print("port", port)
            print("dialect", dialect)
            print("driver", driver)

        # populates engine to access Postgres database
        engine = create_engine(
            f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{dbname}",
            pool_recycle=3600,
        )
        db_conn = engine.connect()

        # if needed to change query, do so here
        db_df = pd.read_sql_query("SELECT * FROM desks_90", con=db_conn)
        return db_df

    def __init__(self, use_csv=False, verbose=False):
        # load data from DB
        if not use_csv:
            if verbose:
                print("Calling db connector")
            self.db_df = self.db_connector(verbose)
        # load data from CSV file directly
        else:
            if verbose:
                print("reading CSV file")
            self.db_df = pd.read_csv("data/robin.csv")


class Transformers:

    def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:

        df = df[["Creator Name", "Desk Name", "Start (UTC)", "Canceled At (UTC)"]]

        return df

    def group_data(df: pd.DataFrame) -> pd.DataFrame:

        df = df.groupby(["Start (UTC)", "Creator Name"])

        return df
    
    def add_missing_days(self, df: pd.DataFrame) -> pd.DataFrame:

        # Convert 'Start (UTC)' column to datetime format
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
        print (df)
