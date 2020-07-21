import axios from "axios"
import { collectTextRange, getNextWord } from './lib/textProcessing'
import C from './constants'

const buildPhrase = words => {
    if(words.length > 0){
        let phrase = words.reduce((acc, currVal) => acc + currVal)
        return phrase
    }
    else{
        //TODO: Change this to a warning that the translation queue is empty
        let emptyPhrase = ""
        return emptyPhrase
    }
}

const convertDocuments = response => {
    let messages = []
    let msg = {
        type: C.LIST_DOCUMENTS,
        documents: response.works
    }
    messages.push(msg)
    
    msg = {
        type: C.FINISHED_LOADING,
        component: C.DOCUMENT_SELECTOR
    }
    messages.push(msg)
    
    return messages
}

const convertPages = response => {
    let messages = []
    
    if(!("content" in response)){
        msg = {
            type: NO_ACTION
        }
        return msg
    }

    let content = response.content
    let start = response.startPage
    let end = start + content.length - 1
    let msg = {
            type: C.SET_PAGE_RANGE,
            content: content,
            start: start,
            end: end
        }
    messages.push(msg)
    
    let lines = content[0]
    msg = {
        type: C.SET_CURRENT_PAGE,
        newPage: lines,
        pageNumber: start
    }
    messages.push(msg)

    return messages
}

const convertTranslations = (page, response) => {
    let messages = []
    let msg = {}
    if ("translations" in response){
        msg = {
            type: C.DISPLAY_TRANSLATION,
            matches: response.translations,
            currPage: page
        }
    }
    else {
        msg = {
            type: C.DISPLAY_TRANSLATION,
            matches: [],
            currPage: 1
        }
    }
    messages.push(msg)

    msg = {
        type: C.FINISHED_LOADING,
        component: C.TRANSLATION_VIEWER
    }
    messages.push(msg)

    return messages
}

const logError = error => console.error(error)

const makeServiceCall = (convert, dispatch, url, method, body={}) => {
    axios({
      url: url,
      method: method,
      headers: {}, //TODO: Implement getHeaders()
      data: body,
      timeout: 20000  
    })
    .then(parseResponse)
    .then(convert)
    .then(dispatch)
    .catch(logError)
}

const multiDispatch = (dispatch, messages) => {
    messages.forEach(msg => dispatch(msg)) 
}

const parseResponse = response => {
    if(typeof response === "string"){
        return JSON.parse(response)
    }

    return response.data
}

export const addToTranslationQueue = (dispatch, getState, word) => {
    let direction = C.DIRECTION.RIGHT
    let lines = getState().lines
    let newWord = getNextWord(direction, lines, word)
    let msg = {
        type: C.ADD_WORD,
        word: newWord.fulltext
    }
    dispatch(msg)
    highlight(dispatch, newWord.selected)
}

export const clearTranslationQueue = () =>
    (dispatch, getState) => {
        let emptyQueue = []
        let msg = {
            type: C.FILTER_TRANSLATION_QUEUE,
            searchPhrase: emptyQueue
        }
        dispatch(msg)
    }

export const deleteFromTranslationQueue = (position) =>
    (dispatch, getState) => {
        let searchPhrase = getState().translations.searchPhrase
        let filteredPhrase = searchPhrase.filter((val, index) => index != position)
        let msg = {
            type: C.FILTER_TRANSLATION_QUEUE,
            searchPhrase: filteredPhrase
        }
        dispatch(msg)
    }

export const getPages = (dispatch, getState, pageNumber) => {
    let pages = getState().pages
    if (pageNumber >= pages.startPage & pageNumber <= pages.endPage){
        let offset = pageNumber - pages.startPage
        let msg = {
                type: C.SET_CURRENT_PAGE,
                newPage: pages.content[offset],
                pageNumber: pageNumber
            }
        dispatch(msg)
    }
    else {
        let body = {
                title: pages.currDoc.title,
                author: pages.currDoc.author,
                page: pageNumber
            }
        makeServiceCall(
            convertPages,
            (messages) => multiDispatch(dispatch, messages),
            localStorage["login::services::getPages"],
            'GET',
            body 
        )
    }
}

export const getTranslations = (dispatch, getState, pageNumber) => {
    let translations = getState().translations
    let phrase = buildPhrase(translations.searchPhrase)
    let body = {
        page: pageNumber,
        query: phrase
    }
    //TODO: Insert loading message here
    makeServiceCall(
        (response) => convertTranslations(pageNumber, response),
        (messages) => multiDispatch(dispatch, messages),
        localStorage["login::services::getTranslations"],
        'GET',
        body
    )
}

export const highlight = (dispatch, words) => {
    let msg = {
        type: C.HIGHLIGHT,
        selected: words
    }
    dispatch(msg)
}

export const listDocuments = () =>
    (dispatch, getState) => {
        makeServiceCall(
            convertDocuments,
            (messages) => multiDispatch(dispatch, messages),
            localStorage["login::services::listDocuments"],
            'GET'
        )            
    }

export const navigate = (direction, pageNumber, navigator) => 
    (dispatch, getState) => {
        if (direction === C.PREVIOUS_PAGE){
            navigator(dispatch, getState, pageNumber - 1)
        }
        if (direction === C.NEXT_PAGE){
            navigator(dispatch, getState, pageNumber + 1)
        }
    }

export const registerSelectedWord = (word) =>
    (dispatch, getState) => {
        let boundary = getState().translations.boundary.currState
        if (boundary === C.TEXT_START){
            setTextStart(dispatch, getState, word)
        }
        else if (boundary === C.TEXT_FINISH){
            setTextEnd(dispatch, getState, word)
        }
        else {
            addToTranslationQueue(dispatch, getState, word)
        }
    }

export const resetTranslations = () =>
    (dispatch, getState) => {
        let msg = {
            type: C.RESET_TRANSLATIONS
        }
        dispatch(msg)
    }

export const setCurrentDocument = doc =>
    (dispatch, getState) => {
        let msg = {
            type: C.SELECT_DOCUMENT,
            document: doc
        }
        dispatch(msg)

        msg = {
            type: C.SET_INTERACTION,
            interaction_type: C.DOCUMENT_VIEWER
        }
        dispatch(msg)

        let firstPage = 1
        getPages(dispatch, getState, firstPage)
        //TODO: Set loaded to false again and clear document list
    }

export const setOption = option => 
    (dispatch, getState) => {
        let msg = {
            type: C.SET_OPTION,
            option: option
        }
        dispatch(msg)
    }

export const setTextBoundary = (boundary) =>
    (dispatch, getState) => {
        let msg = {
            type: C.SET_TEXT_BOUNDARY,
            currState: boundary
        }
        dispatch(msg)
    }

//Add full phrase to translation queue
export const setTextEnd = (dispatch, getState, word) => {
        let selected = collectTextRange(dispatch, getState, word)
        highlight(dispatch, selected)
}

export const setTextStart = (dispatch, getState, word) => {
    let lines = getState().lines
    let msg = {
        type: C.APPEND_TRANSLATION_BUFFER,
        buffer: lines.words,
        start: word
    }
    dispatch(msg)
}

export const unhighlight = (dispatch, words) => {
    let msg = {
        type: C.UNHIGHLIGHT,
        selected: words
    }
    dispatch(msg)
}