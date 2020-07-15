import axios from 'axios'
import C from '../constants'
import { difference, equals, union } from '../lib/setProcessing'
import { storeFactory } from '../store'
import * as actions from '../actions'

jest.mock('axios')

describe("Append translation queue", () => {
    let initState
    let store
    beforeEach(() => {
        localStorage.removeItem('redux-store')
        initState = {
            translations: {
                searchPhrase: ["das ", "Buch "]
            }
        }
        store = storeFactory(initState)
    })

    it("Add multiple words", () => {
        let toAppend = ["ist ", "interessant."]
        let expectedState = {
            translations: {
                searchPhrase: ["das ", "Buch ", "ist ", "interessant."]
            }
        }
        let msg = {
            type: C.APPEND_TRANSLATION_QUEUE,
            words: toAppend
        }
        store.dispatch(msg)
        expect(store.getState().translations).toStrictEqual(expectedState.translations)
    })
})

describe("Choose document", () => {
    let testData
    let initState
    let store
    beforeEach(() => {
        localStorage.removeItem('redux-store')
        testData = [
            {"title": "Die Welt", "author": "Schopenhauer"},
            {"title": "Kritik", "author": "Kant"}
        ]
        initState = {
            documents: testData, 
            interaction: C.DOCUMENT_SELECTOR
        }
        store = storeFactory(initState)
    })

    it("Document processed", () => {
        store.dispatch(actions.setCurrentDocument(testData[0]))
        let pages = store.getState().pages
        expect(pages.currDoc).toEqual(testData[0])
    })

    it("Switch to viewer", () => {
        store.dispatch(actions.setCurrentDocument(testData[1]))
        let viewer = C.DOCUMENT_VIEWER
        let interaction = store.getState().interaction
        expect(interaction).toEqual(viewer)
    })
})

describe("Display translations", () => {
    beforeEach(() => {
        localStorage.removeItem('redux-store')
    })

    it("First page", () => {
        let initState = {
                translations:{
                    currPage: 1,
                    matches: [],
                    searchPhrase: ["das ", "Buch"]
                }
            }
        let data = {
                translations: [
                   {
                       text: "das Buch",
                       pos: "Noun",
                       definitions: ["the book"]
                   }
            ]}
        let store = storeFactory(initState)
        axios.mockResolvedValue(JSON.stringify(data))
        let testDispatch = (msg) => {
            store.dispatch(msg)
            expect(store.getState().translations.matches).toStrictEqual(data.translations)
        }
        actions.getTranslations(testDispatch, store.getState, 1)
    })
})

describe("Filter translation queue", () => {
    let initState
    let store
    beforeEach(() => {
        initState = {
            translations: {
                currPage: 1,
                searchPhrase: ["das ", "interessante ", "Buch"]
            }
        } 
        localStorage.removeItem('redux-store')
        store = storeFactory(initState)
    })

    it("clear queue", () => {
        actions.clearTranslationQueue()(store.dispatch, store.getState)
        let result = {
            currPage: 1,
            searchPhrase: []
        }
        expect(store.getState().translations).toStrictEqual(result)
    })

    it("remove last element", () => {
        let lastPos = store.getState().translations.searchPhrase.length - 1
        actions.deleteFromTranslationQueue(lastPos)(store.dispatch, store.getState)
        let result = {
            currPage: 1,
            searchPhrase: ["das ", "interessante "]
        }
        expect(store.getState().translations).toStrictEqual(result)
    })

    it("remove middle element", () => {
        actions.deleteFromTranslationQueue(1)(store.dispatch, store.getState)
        let result = {
            currPage: 1,
            searchPhrase: ["das ", "Buch"]
        }
        expect(store.getState().translations).toStrictEqual(result)
    })
})


describe("Highlight", () => {
    beforeEach(() => {
        localStorage.removeItem('redux-store')
    })

    it("multiple elements", () => {
        let oldWords = new Set(["1::1::1"])
        let initState = {
            lines: {
                selected: oldWords
            }
        }
        let store = storeFactory(initState)
        let newWords = new Set(["2::3::1", "1::2::1"])
        actions.highlight(store.dispatch, newWords)
        let expected = union(oldWords, newWords)
        let areEqual = equals(expected, store.getState().lines.selected)
        expect(areEqual).toBe(true)
    })

    it("single element", () => {
        let word = "1::1::1"
        let initState = {
            lines: {
                selected: new Set([word])
            }
        }
        let store = storeFactory(initState)
        let newWord = "2::3::1"
        let words = new Set([newWord])
        actions.highlight(store.dispatch, words)
        let result = new Set([word, newWord])
        let areEqual = equals(result, store.getState().lines.selected)
        expect(areEqual).toBe(true)
    })
})

describe("List documents", () => {
    beforeEach(() => {
        localStorage.removeItem('redux-store')
    })

    it("multiple docs", () => {
        let initState = {
                documents: []
            }
        let data = {
                docs: [
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
        let store = storeFactory(initState)
        axios.mockResolvedValue(JSON.stringify(data))
        let testDispatch = (msg) => {
            store.dispatch(msg)
            expect(store.getState().documents).toStrictEqual(data.docs)
        }
        actions.listDocuments()(testDispatch, store.getState)  
    })
})

describe("Reset translations", () => {
    let initState
    let store
    beforeEach(() => {
        localStorage.removeItem('redux-store')
        initState = {
            translations: {
                boundary: {
                    buffer: [],
                    currState: C.TEXT_START,
                    start: {}
                },
                currPage: 1,
                matches: [],
                searchPhrase: ["das ", "Buch"]
            }
        }
        store = storeFactory(initState)
    })

    it("go to default state", () => {
        let defaultState = {
            translations: {
                boundary: {
                    buffer: [],
                    currState: "",
                    start: {}
                },
                currPage: 1,
                matches: [],
                searchPhrase: []
            }
        }
        actions.resetTranslations()(store.dispatch, store.getState)
        expect(store.getState().translations).toStrictEqual(defaultState.translations)
    })
})

describe("Set current page", () => {
    let initState
    let store
    beforeEach(() => {
        localStorage.removeItem('redux-store')
        initState = {
            lines:{
                currPage: 3,
                words:[
                    ["das ", "Buch "],
                    ["ist ", "interessant."]
                ]
            },
            pages:{
                content: [{
                    words: [
                        ["das ", "Buch "],
                        ["ist ", "interessant."]
                    ]
                },
                {
                    words: [
                        ["Die ", "Welt "],
                        ["ist ", "meine ", "Vorstellung"]
                    ]
                }],
                endPage: 5,
                startPage: 3
            }
        }
        store = storeFactory(initState)
    })

    it("Go to next page", () => {
        actions.getPages(store.dispatch, store.getState, 4)
        let newLines = {
            currPage: 4,
            words: [
                ["Die ", "Welt "],
                ["ist ", "meine ", "Vorstellung"]
            ]   
        }
        expect(store.getState().lines).toStrictEqual(newLines)
    })
})

describe("Set option", () => {
    it("Switch to default option", () => {
        let initState = {
                option: C.DOC_VIEWER_OPTIONS.ADD_VOCAB
            }
        let store = storeFactory(initState)
        let newOption = C.DOC_VIEWER_OPTIONS.DEFAULT
        actions.setOption(newOption)(store.dispatch, store.getState)
        expect(store.getState().option).toBe(newOption)
    })

    it("Switch to vocabulary viewer", () => {
        let initState = {
                option: C.DOC_VIEWER_OPTIONS.DEFAULT
            }
        let store = storeFactory(initState)
        let newOption = C.DOC_VIEWER_OPTIONS.ADD_VOCAB
        actions.setOption(newOption)(store.dispatch, store.getState)
        expect(store.getState().option).toBe(newOption)
    })
})

describe("Set page range", () => {
    let data
    let initState
    let store
    beforeEach(() => {
        localStorage.removeItem('redux-store')
        data = {
            content: [{
                words: [
                    ["das ", "Buch "],
                    ["ist ", "interessant."]
                ]
            },
            {
                words: [
                    ["Die ", "Welt "],
                    ["ist ", "meine ", "Vorstellung"]
                ]
            }],
            startPage: 6
        }
        initState = {
            lines: {},
            pages: {
                currDoc: {
                    author: "Schopenhauer",
                    title: "Die Welt"
                },
                endPage: 5,
                startPage: 3
            }
        }
        store = storeFactory(initState)
    })

    it("check lines", () => {
        let newLines = {
            ...data.content[0],
            currPage: 6,
        }
        let testDispatch = (msg) => {
            store.dispatch(msg)
            if(msg.type === C.SET_CURRENT_PAGE){
                expect(store.getState().lines).toStrictEqual(newLines)
            }
        }
        axios.mockResolvedValue(JSON.stringify(data))
        actions.getPages(testDispatch, store.getState, 6)
    })

    it("check pages", () => {
        let newPages = {
            currDoc: initState.pages.currDoc,
            content: data.content,
            endPage: 7,
            startPage: 6
        }
        let testDispatch = (msg) => {
            store.dispatch(msg)
            if(msg.type === C.SET_PAGE_RANGE){
                expect(store.getState().pages).toStrictEqual(newPages)
            }
        }
        axios.mockResolvedValue(JSON.stringify(data))
        actions.getPages(testDispatch, store.getState, 6)
    })
})

describe("Set text boundary", () => {
    let initState
    let store
    beforeEach(() => {
        localStorage.removeItem('redux-store')
        initState = {
            translations: {
                boundary:{
                    currState: C.TEXT_START
                },
                searchPhrase: []
            }
        }
        store = storeFactory(initState)
    })

    it("Text end", () => {
        let boundary = C.TEXT_FINISH
        actions.setTextBoundary(boundary)(store.dispatch, store.getState)
        let result = {
            translations: {
                boundary: {
                    currState: C.TEXT_FINISH
                },
                searchPhrase: []
            }
        }
        expect(store.getState().translations).toStrictEqual(result.translations)
    })
})

describe("Unhighlight", () => {
    let initState
    let store
    let words
    beforeEach(() => {
        localStorage.removeItem('redux-store')
        words = new Set(["1::1::1", "1::1::2"])
        initState = {
            lines: {
                selected: words
            }
        }
        store = storeFactory(initState)
    })

    it("Unhiglight all", () => {
        actions.unhighlight(store.dispatch, words)
        let emptySet = new Set([])
        let areEqual = equals(emptySet, store.getState().lines.selected)
        expect(areEqual).toBe(true)
    })

    it("Unhighlight single word", () => {
        let singleWord = new Set(["1::1::2"])
        actions.unhighlight(store.dispatch, singleWord)
        let expected = difference(words, singleWord)
        let areEqual = equals(expected, store.getState().lines.selected)
        expect(areEqual).toBe(true)
    })
})