import argparse

from datetime import datetime

from data_writer import DataWriter
from languages.german.german_data_connection import GermanDataConnection
from languages.german.german_data_processor import GermanDataProcessor

if __name__ == "__main__":
    #Parse arguments to script
    parser = argparse.ArgumentParser()
    help_string = "German dictionary source data to be transformed"
    parser.add_argument("data_source", help=help_string)
    help_string = "Configurations for the database connection"
    parser.add_argument("conn_config", help=help_string)
    help_string = "Configurations for the etl process"
    parser.add_argument("data_config", help=help_string)
    args = parser.parse_args()

    #Set up ETL components
    data_source = args.data_source
    conn_config = args.conn_config
    data_config = args.data_config
    connection = GermanDataConnection(conn_config)
    processor = (lambda data: GermanDataProcessor(data, data_config))
    data_writer = DataWriter(connection, processor, data_config)
    
    #Run ETL pipeline
    print("Beginning ETL process")
    t1 = datetime.now()
    data_writer.write([data_source])
    t2 = datetime.now()
    time_elapsed = str(t2 - t1)
    print("ETL process finished")
    print("Time elapsed: " + time_elapsed)