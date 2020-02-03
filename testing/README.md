Before the tests can be run, you must have a MongoDB instance running
with a dedicated database for testing. You must also have an Elasticsearch
instance running with German dictionary data in the appropriate form.

Once this infrastructure is in place, the variables in vocab_manager/config.py
for the configuration TestingConfig must be initialized.

After the prerequisites have been met, to run the tests, go to the top level 
project directory (vocab_manager) and run the following command:

python3 run_tests.py

The test results will be printed to the console.