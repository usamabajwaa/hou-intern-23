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


