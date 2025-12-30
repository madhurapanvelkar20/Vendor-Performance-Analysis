import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logger = logging.getLogger(__name__)

def ingest_db(df, table_name, engine):
    logger.info(f"Ingesting data into {table_name}")

engine = create_engine("sqlite:///inventory.db")

def load_raw_data():
    '''this function will load the CSVs as dataframe and ingest into db'''
    start = time.time()
    for file in os.listdir('Vendor Performance'):
        if '.csv' in file:
            df = pd.read_csv('Vendor Performance/'+file)
            logging.info('Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end-start)/60
    logging.info('Ingestion Complete')
    logging.info(f'\nTotal Time Taken: {total_time} minutes')

if __name__ == '__main__':
    load_raw_data()