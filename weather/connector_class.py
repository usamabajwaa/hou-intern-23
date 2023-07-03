import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

class Connector:
        
    def db_connector(self) -> pd.DataFrame():
        """generic SQL connector that queries a db and saves result to a dataframe
        This function populates the Connector class database dataframe with whatever parameters are passed to the engine function
        and also whatever the query provided is. Please note that you need to use a .env file and assign the correct values in 
        the file to match the following sqlalchemy engine syntax:
        
        {dialect}+{driver}://{username}:{password}@{host_name}:{port_number}/{database_name}

        Returns:
            db_df: the database translated into a pandas dataframe
        """
        
        #gets .env variables to access your database
        load_dotenv()
        host = os.getenv('host_name')
        dbname = os.getenv('db_name')
        user = os.getenv('user_name')
        password = os.getenv('user_password')
        port = os.getenv('port_number')
        dialect = os.getenv('dialect')
        driver = os.getenv('driver')
        
        #populates engine to access Postgres database 
        engine = create_engine(f'{dialect}+{driver}://{user}:{password}@{host}:{port}/{dbname}', pool_recycle=3600)
        db_conn = engine.connect()
        
        #if needed to change query, do so here
        db_df = pd.read_sql_query('SELECT * FROM desks_90', con=db_conn)
        return db_df
    
    def __init__(self):
        self.db_df = self.db_connector()

test_df = Connector()

class Transformers: 
    def __init__(self): 
        self.data = pd.DataFrame

    def drop_unused_columns(self, df: pd.DataFrame ) -> pd.DataFrame:

        df = df[['Creator Name', 'Desk Name', 'Start (UTC)', 'Canceled At (UTC)']]

        return df
    
    def group_data(self, df: pd.DataFrame) -> pd.DataFrame:
        
        df  = df.groupby(['Start (UTC)', 'Creator Name'])
        
        return df

        