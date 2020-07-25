const firstPage = {
    words: [
        ["Die ", "Welt ", "ist "],
        ["meine ", "Vorstellung."]
    ],
    breaks: {
        pageBoundaries: {
            next: {},
            previous: {},
        },
        end: [1,3],
        start: [0, 2],
        tokens: [
            {
                fulltext: "Die ", 
                positions: [[1,0,0]]
            },
            {
                fulltext: "ist ",
                positions: [[1,0,2]]
            },
            {
                fulltext: "meine ",
                positions: [[1,1,0]]
            },
            {
                fulltext: "Vorstellung.",
                positions: [[1,1,1]]
            }
        ]
    }
}

const secondPage = {
    words: [
        ["Habe ", "Mu-"],
        ["t ", "zu ", "wissen."]
    ],
    breaks: {
        pageBoundaries: {
            next: {},
            previous: {},
        },
        end: [1,2],
        start: [0, 1],
        tokens: [
            {
                fulltext: "Habe ",
                positions: [[2,0,0]]
            },
            {
                fulltext: "Mut ",
                positions: [[2,0,1], [2,1,0]]
            },
            {
                fulltext: "wissen.",
                positions: [[2,1,2]]
            }
        ]
    }
}

const pages = {
    content: [firstPage, secondPage],
    startPage: 1
}

const pageRangeData = {
    "httpRequest": {
        "path": "/page_range"
    },
    "httpResponse": {
        "body": pages
    }
}

module.exports = {
    pageRangeData: pageRangeData
}