const mockServer =  require('mockserver-node')
const port = 1080

//Start mock server
mockServer.start_mockserver({
    serverPort: port,
    trace: true,
    verbose: true
})