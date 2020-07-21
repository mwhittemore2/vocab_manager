const mockServer =  require('mockserver-node')
const port = 1080

//Start mock server
mockServer.start_mockserver({
    serverPort: port,
    //systemProperties: "-Dmockserver.enableCORSForAllResponses=true",
    trace: true,
    verbose: true
})