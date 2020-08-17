import axios from "axios"
import { getHeaders, setLanguage } from './lib/apiTools'
import { collectTextRange, getNextWord, isAlreadySelected } from './lib/textProcessing'
import C from './constants'

/**
 * Constructs a phrase from an array of words which will
 * then be used as the user's translation query.
 * 
 * @param {array} words The words comprising the phrase.
 * @return {string} The user's translation query.
 */
const buildPhrase = words => {
    if(words.length > 0){
        let phrase = ""
        words.forEach(word => {
            phrase = phrase + word.fulltext
        })
        return phrase
    }
    else{
        let emptyPhrase = ""
        return emptyPhrase
    }
}

/**
 * Loads documents for the user to choose from after
 * they've been received from the corresponding service
 * call.
 * 
 * @param {object} response The document choices.
 * @return {array} The messages to be dispatched.
 */
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

/**
 * Loads pages for the user to read in the document
 * viewer after receiving them from the corresponding
 * service call.
 * 
 * @param {object} response The pages to be dispalyed.
 * @return {array} The messages to be dispatched.
 */
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

/**
 * Loads translations of a the user's query after receiving
 * them from the corresponding service.
 * 
 * @param {number} page The current page of translation results
 * @param {object} response The translation results from the server.
 * @return {array} The messages to be dispatched.
 */
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

/**
 * Logs an error message to the console.
 * 
 * @param {string} error The error message to be logged.
 */
const logError = error => console.error(error)

/**
 * Makes an API call to a microservice.
 * 
 * @param {func} convert Transforms the microservice response into messages
 *                       to be dispatched to the state store.
 * @param {func} dispatch Sends a message to the state store.
 * @param {string} url The endpoint for accessing the microservice.
 * @param {string} method The type of HTTP request to make.
 * @param {object} body The body of the JSON request.
 */
const makeServiceCall = (convert, dispatch, url, method, body={}) => {
    axios({
      url: url,
      method: method,
      headers: getHeaders(), 
      data: body,
      timeout: 20000  
    })
    .then(parseResponse)
    .then(convert)
    .then(dispatch)
    .catch(logError)
}

/**
 * Dispatches a series of messages to the state store to the 
 * synchronous manner.
 * 
 * @param {func} dispatch Sends an individial message to the
 *                        state store.
 * @param {array} messages The messages to be sent.
 */
const multiDispatch = (dispatch, messages) => {
    messages.forEach(msg => dispatch(msg)) 
}

/**
 * Converts the JSON response of a microservice call to a form that
 * can be processed more easily by downstream components.
 * 
 * @param {object} response The JSON response from a microservice call.
 * @return {object} The converted response.
 */
const parseResponse = response => {
    if(typeof response === "string"){
        return JSON.parse(response)
    }

    return response.data
}

/**
 * Appends a word to the translation queue.
 * 
 * @param {func} dispatch Sends a message to the state store.
 * @param {func} getState Fetches the state store.
 * @param {object} word The word to add to the queue.
 */
export const addToTranslationQueue = (dispatch, getState, word) => {
    let direction = C.DIRECTION.RIGHT
    let lines = getState().lines
    
    if(isAlreadySelected(getState, word)){
        let errorMessage = "Word is already selected"
        window.alert(errorMessage)
        return
    }

    let newWord = getNextWord(direction, lines, word)
    let msg = {
        type: C.APPEND_TRANSLATION_QUEUE,
        words: [newWord]
    }
    dispatch(msg)
    highlight(dispatch, newWord.selected)
}

/**
 * Removes all content in the translation queue.
 */
export const clearTranslationQueue = () =>
    (dispatch, getState) => {
        let toUnighlight = getState().lines.selected
        let emptyQueue = []
        let msg = {
            type: C.FILTER_TRANSLATION_QUEUE,
            searchPhrase: emptyQueue
        }
        dispatch(msg)
        unhighlight(dispatch, toUnighlight)
    }

/**
 * Deletes a particular item from the translation queue based
 * on its position in the queue.
 * 
 * @param {number} position The position of the item to be
 *                          deleted.
 */
export const deleteFromTranslationQueue = (position) =>
    (dispatch, getState) => {
        let searchPhrase = getState().translations.searchPhrase
        let toUnhighlight = searchPhrase[position].selected
        let filteredPhrase = searchPhrase.filter((val, index) => index != position)
        let msg = {
            type: C.FILTER_TRANSLATION_QUEUE,
            searchPhrase: filteredPhrase
        }
        dispatch(msg)
        unhighlight(dispatch, toUnhighlight)
    }

/**
 * Fetches the pages that the user wants to read next.
 * 
 * @param {func} dispatch Sends a message to the state store.
 * @param {func} getState Fetches the state store.
 * @param {number} pageNumber The number of the first page to fetch.
 */
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
                start: pageNumber
            }
        makeServiceCall(
            convertPages,
            (messages) => multiDispatch(dispatch, messages),
            localStorage["login::services::getPages"],
            'POST',
            body 
        )
    }
}

/**
 * Processes the user's translation query.
 * 
 * @param {func} dispatch Sends a message to the state store.
 * @param {func} getState Fetches the state store.
 * @param {number} pageNumber The page of translation results
 *                            to fetch.
 */
export const getTranslations = (dispatch, getState, pageNumber) => {
    let translations = getState().translations
    let phrase = buildPhrase(translations.searchPhrase)
    let body = {
        page: pageNumber,
        query: phrase
    }
    
    let msg = {
        type: C.NOT_LOADED,
        component: C.TRANSLATION_VIEWER
    }
    dispatch(msg)

    let language = getState().pages.currDoc.language
    let template = localStorage["login::services::getTranslations"]
    let route = setLanguage(language, template)
    makeServiceCall(
        (response) => convertTranslations(pageNumber, response),
        (messages) => multiDispatch(dispatch, messages),
        route,
        'POST',
        body
    )
}

/**
 * Colors the specified words in the browser.
 * 
 * @param {func} dispatch Sends a message to the state store.
 * @param {Set} words The words to be colored.
 */
export const highlight = (dispatch, words) => {
    let msg = {
        type: C.HIGHLIGHT,
        selected: words
    }
    dispatch(msg)
}

/**
 * Moves the calling component to the specified page.
 * 
 * @param {event} e A key press.
 * @param {func} navigator Fetches desired page.
 */
export const jumpToPage = (e, navigator) =>
    (dispatch, getState) => {
        let enterKey = C.KEYBOARD_INPUT.ENTER
        if(e.keyCode === enterKey){
            let pageNumber = e.target.value
            let isNumeric = !isNaN(pageNumber)
            if(isNumeric){
                pageNumber = parseInt(pageNumber)
                navigator(dispatch, getState, pageNumber)
            }
            else{
                let errorMessage = "Destination must be a whole number"
                window.alert(errorMessage)
            }
        }
    }

/**
 * Fetches the documents that the user can choose to read.
 */
export const listDocuments = () =>
    (dispatch, getState) => {
        makeServiceCall(
            convertDocuments,
            (messages) => multiDispatch(dispatch, messages),
            localStorage["login::services::listDocuments"],
            'GET'
        )            
    }

/**
 * Fetches the desired page for the calling component.
 * 
 * @param {string} direction The direction in which to move.
 * @param {number} pageNumber The number of the current page
 * @param {func} navigator Sends the calling component its
 *                         desired page.
 */
export const navigate = (direction, pageNumber, navigator) => 
    (dispatch, getState) => {
        if (direction === C.PREVIOUS_PAGE){
            navigator(dispatch, getState, pageNumber - 1)
        }
        if (direction === C.NEXT_PAGE){
            navigator(dispatch, getState, pageNumber + 1)
        }
    }

/**
 * Decides what action to take with the word the user
 * has just clicked on.
 * 
 * @param {object} word The word the user has clicked on.
 */
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

/**
 * Deletes the current translation results.
 */
export const resetTranslations = () =>
    (dispatch, getState) => {
        clearTranslationQueue()(dispatch, getState)
        
        let msg = {
            type: C.RESET_TRANSLATIONS
        }
        dispatch(msg)
    }

/**
 * Specifies the document to display.
 * 
 * @param {object} doc The document to display.
 */
export const setCurrentDocument = doc =>
    (dispatch, getState) => {
        //Start transition to document viewer
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

        //Get first page of selected document
        let firstPage = 1
        getPages(dispatch, getState, firstPage)

        //Cleanup operations
        msg = {
            type: C.NOT_LOADED,
            component: C.DOCUMENT_SELECTOR
        }
        dispatch(msg)
       
        msg = {
            type: C.CLEAR_DOCUMENTS
        }
        dispatch(msg)
    }

/**
 * Specifies the specific tool for working with the
 * document the user is reading.
 * 
 * @param {string} option The name of the tool to use.
 */
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

/**
 * Adds a span of text to the translation queue.
 * 
 * @param {func} dispatch Sends a message to the state store.
 * @param {func} getState Fetches the state store.
 * @param {object} word The end of the span.
 */
export const setTextEnd = (dispatch, getState, word) => {
        let selected = collectTextRange(dispatch, getState, word)
        highlight(dispatch, selected)
        let defaultBoundary = C.TEXT_BOUNDARY_DEFAULT
        setTextBoundary(defaultBoundary)(dispatch, getState)
}

/**
 * Specifies the start of a span of text that will eventually
 * be added to the translation queue.
 * 
 * @param {func} dispatch Sends a message to the state store.
 * @param {func} getState Fetches the state store.
 * @param {object} word The start of the span of text.
 */
export const setTextStart = (dispatch, getState, word) => {
    let lines = getState().lines
    let linesCopy = {
        breaks: lines.breaks,
        words: lines.words
    }
    let msg = {
        type: C.APPEND_TRANSLATION_BUFFER,
        buffer: linesCopy,
        start: word
    }
    dispatch(msg)
}

/**
 * Removes coloring from specified words.
 * 
 * @param {func} dispatch Sends a message to the state store.
 * @param {Set} words The words that will lose their coloring.
 */
export const unhighlight = (dispatch, words) => {
    let msg = {
        type: C.UNHIGHLIGHT,
        selected: words
    }
    dispatch(msg)
}