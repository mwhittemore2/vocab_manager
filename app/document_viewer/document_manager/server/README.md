This folder contains the infrastructure for mocking data from the server, 
which can be used to test API calls that originate from the front-end code 
without also requiring the corresponding back-end code to be fully implemented.

To run the infrastructure, you'll need node.js. Assuming you have this, you'll 
then need to install some MockServer libraries for node which can be installed 
with npm as follows:

npm install mockserver-node
npm install mockserver-client

Once these are installed, you need to start the server. This can be done by
running the following command from within this directory:

node runMockServer.js

After the server is up and running, you'll then need to upload the mock API data.
To do this, start a separate terminal/process and navigate to this directory.
Next, run the following command:

node initializeResponses.js

Once the api data is uploaded, you can confirm that it works correctly by running
the following curl command:

curl "http://localhost:1080/translations"

You should see the following output:

{
  "text" : "Welt",
  "definitions" : [ "world", "earth" ]
}

If you see this output, you can then leave the server running and it will send mock API
data for testing your front-end API calls.

