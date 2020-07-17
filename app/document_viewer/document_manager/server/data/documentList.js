const documentList = {
    "httpRequest":{
        "path": "/document_retrieval/doc_list"
    },
    "httpResponse": {
        "body": {
            "works": [
                {
                    title: "Die Welt als Wille und Vorstellung",
                    author: "Arthur Schopenhauer"
                },
                {
                    title: "Kritik der reinen Vernunft",
                    author: "Immanuel Kant"
                }
            ]
       }
    }
}

module.exports = {
    documentList: documentList
}