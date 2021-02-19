import argparse
import os
import subprocess

import boto3
import yaml

def load_dictionaries(config):
    """
    Transfers dictionary data from an S3 bucket
    to an EC2 instance and then triggers a
    language-specific ETL job.

    Parameters
    ----------
    config : str
        The path to the configuration file for the
        dictionary download process.
    """
    data = yaml.safe_load(config)
    s3 = boto3.resource('s3')

    tmp = data["tmp"]
    languages = data["languages"]
    for language in languages:
        tasks = data["tasks"][language]

        #Build a dictionary
        for task in tasks:
            params = tasks[task]
            etl_pipeline = params["etl_pipeline"]
            bucket = params["bucket"]
            sources = params["sources"]

            #Download data sources
            os.mkdir(tmp)
            bucket = s3.Bucket(bucket)
            for source in sources:
                to_download = sources[source]["input"]
                destination = os.path.join(tmp, sources[source]["output"])
                try:
                    bucket.download_file(to_download, destination)
                except:
                    error_msg = "Couldn't transfer " + to_download
                    error_msg += " from bucket to " + destination
                    print(error_msg)
            
            #Run ETL pipeline
            subprocess.run(['sh', etl_pipeline])

            #Cleanup
            os.rmdir(tmp)

if __name__ == "__main__":
    #Parse arguments to the script
    parser = argparse.ArgumentParser()
    parser.add_argument("config",
                        help="The configuration file for the dictionary download process",
                        type="string")
    args = parser.parse_args()

    #Download the dictionaries
    config = args.config
    load_dictionaries(config)