//Load test data
const documentList = require('./data/documentList').documentList
const translationData = require('./data/translations').translationData
const pageRangeData = require('./data/pageRange').pageRangeData

//Set up client configurations
const mockServerClient = require('mockserver-client').mockServerClient
const port = 1080

//Initialize document data
mockServerClient("localhost", port)
.mockAnyResponse(documentList)
.then(
    () => {
        console.log("Set up document list expectation")
    },
    (error) => {
        console.error(error)
    }
)

//Initialize translation data
mockServerClient("localhost", port)
.mockAnyResponse(translationData)
.then(
    () => {
        console.log("Set up translation expectation")
    },
    (error) => {
        console.error(error)
    }
)

//Initialize page range data
mockServerClient("localhost", port)
.mockAnyResponse(pageRangeData)
.then(
    () => {
        console.log("Set up page range expectation")
    },
    (error) => {
        console.error(error)
    }
)