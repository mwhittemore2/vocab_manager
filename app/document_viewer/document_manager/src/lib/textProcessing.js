import { union } from './setProcessing'
import C from '../constants'

/**
 * Constructs a JS object representation of a word in
 * the user's document.
 * 
 * @param {number} index The position of the word in its
 *                       corresponding line.
 * @param {number} line The position of the line in its
 *                      corresponding page.
 * @param {number} page The number of the page in the document.
 * @param {string} text The actual text comprising the word.
 * @return {object} The JS object representation of the word.
 */
export const buildWord = (index, line, page, text) => {
    word = {
        line: line,
        page: page.currPage,
        pos: index,
        text: text
    }
    return word
}

/**
 * Builds a phrase out of all the text between a previously specified
 * start point up to a user-supplied end point.
 * 
 * @param {func} dispatch Sends messages to the state store.
 * @param {func} getState Fetches the current state store.
 * @param {object} word The end point of the phrase to be built.
 * @return {Set} The words in the newly constructed phrase.
 * 
 */
export const collectTextRange = (dispatch, getState, word) => {
    let translations = getState().translations
    let lines = translations.boundary.buffer
    let queueSize = translations.searchPhrase.length
    let selected = new Set([])
    let start = translations.boundary.start
    let toAppend = []
    
    //Check that the page difference is within proper limits
    if((word.page - start.page > 1) | (word.page - start.page < 0)){
        let errorMessage = "Text to be translated spans too many pages."
        window.alert(errorMessage)
        return selected
    }

    //Collect words to translate based on user-specified range
    let canAddWord = true
    let canAppendToQueue = true
    let currWord = start
    let isOutOfBounds = false
    let maxSize = C.TRANSLATION_QUEUE_MAX_SIZE
    while(canAddWord){
        isOutOfBounds = !isPreviousTo(currWord, word)
        if(isOutOfBounds){
            canAddWord = false
            break
        }

        //Make sure translation queue isn't full
        let currSize = queueSize + toAppend.length
        if(currSize > maxSize){
            canAddWord = false
            canAppendToQueue = false
            let errorMessage = "Text to be translated exceeds maximum translation queue size."
            window.alert(errorMessage)
            break
        }
        
        //Add new word to translate
        let direction = C.DIRECTION.RIGHT
        let nextWord = getNextWord(direction, lines, currWord)
        if(word.page - start.page === 1){
            toAppend.push(nextWord)
            selected = union(selected, nextWord.selected)
            lines = getState().lines
            currWord = nextWord.pointer
        }
        else{
            toAppend.push(nextWord)
            selected = union(selected, nextWord.selected)
            currWord = nextWord.pointer
        }
        
        //Check that there's another word to add
        if(Object.keys(currWord).length === 0){
            canAddWord = false
        }
    }

    //Append new words to translation queue
    if(canAppendToQueue){
        let msg = {
            type: C.APPEND_TRANSLATION_QUEUE,
            words: toAppend
        }
        dispatch(msg)
    }
    
    return selected
}

/**
 * Fetches the next word relative to the currently supplied word and 
 * direction. Serves as the foundation for building iterators over 
 * the user's document.
 * 
 * @param {string} direction The direction to move when finding
 *                           the next word.
 * @param {object} lines The words comprising the current page. 
 * @param {object} word The word whose successor is to be found.
 * @return {object} The successor to the currently supplied word.
 */
export const getNextWord = (direction, lines, word) => {
    let nextWord

    //word is custom defined
    let hasPos = word.hasOwnProperty('pos')
    if(!hasPos){
        nextWord = {
            fulltext: word.text,
            pointer: {},
            selected: new Set([])
        }
        return nextWord
    }

    //word is not at boundary
    let line = word.line
    let page = word.page
    let pos = word.pos
    let currTxt = lines.words[line][pos]
    if((pos > 0) & (pos < lines.words[line].length - 1)){
        nextWord = {
            fulltext: currTxt,
            pointer: {
                line: line,
                page: page,
                pos: pos + 1
            },
            selected: new Set([getTokenIdentifier(line, page, pos)])
        }
        return nextWord
    }

    let side
    //word is at beginning of line
    if(pos === 0){
        side = C.LINE_BOUNDARY.START
        nextWord = processLineBreak(direction, lines, side, word)
        return nextWord
    }
    //word is at end of line
    if(pos === lines.words[line].length - 1){
        side = C.LINE_BOUNDARY.END
        nextWord = processLineBreak(direction, lines, side, word)
        return nextWord
    }

    //default option
    nextWord = {
        fulltext: word.text,
        pointer: {
            line: line,
            page: page,
            pos: pos
        },
        selected: new Set([getTokenIdentifier(line, page, pos)]) 
    }
    return nextWord
}

/**
 * A string representation of a word useful for set-theoretic 
 * processing.
 * 
 * @param {number} line The position of the line in which the
 *                      word occurs.
 * @param {number} page The number of the page in which the
 *                      word occurs.
 * @param {number} pos The position of the word in its corresponding
 *                     line.
 * @return {string} The string representation of the the word. 
 */
export const getTokenIdentifier = (line, page, pos) => {
    let separator = ":"
    let tokenID = page.toString() + separator + line.toString()
    tokenID = tokenID + separator + pos.toString()
    return tokenID
}

/**
 * Determines if a word has already been added to the
 * translation queue.
 * 
 * @param {func} getState Fetches the current state store.
 * @param {object} word The word to check.
 * @return {bool} True if the word is already in the 
 *                translation queue, False otherwise.
 */
export const isAlreadySelected = (getState, word) => {
    let selected = getState().lines.selected
    let hasPos = word.hasOwnProperty('pos')
    if(!hasPos){
        return false
    }
    let line = word.line
    let page = word.page
    let pos = word.pos
    let tokenID = getTokenIdentifier(line, page, pos)
    let decision = selected.has(tokenID)
    return decision
}

/**
 * Determines if the first word occurs before the second
 * in the user's document.
 * 
 * @param {object} w1 The first word.
 * @param {object} w2 The second word.
 * @return {bool} True if the first word occurs before the
 *                second, False otherwise.
 */
export const isPreviousTo = (w1, w2) => {
    let pageInBounds = (w1.page <= w2.page)
    if(!pageInBounds){
        return false
    }
    let lineInBounds = (w1.line <= w2.line)
    if(w1.page === w2.page){
        if(!lineInBounds){
            return false
        }
    }
    let posInBounds = (w1.pos <= w2.pos)
    if((w1.page === w2.page) & (w1.line === w2.line)){
        if(!posInBounds){
            return false
        }
    }
    return true
}

/**
 * Fetches the first word to the left of the currently
 * supplied word.
 * 
 * @param {object} breaks The line breaks in the page.
 * @param {object} currWord The word to move left from.
 * @param {object} lines The words making up the page.
 * @param {array} tokenData The boundaries of the word.
 * @return {object} The first word to the left of the
 *                  current one.
 */
export const moveLeft = (breaks, currWord, lines, tokenData) => {
    let nextWord = {}
    let leftToken = tokenData.positions[0]
    let page = leftToken[0]
    let line = leftToken[1]
    let pos = leftToken[2]
    if(!(currWord.page === page)){
        nextWord.pointer = breaks.pageBoundaries.previous
    }
    else if((line === 0) & (pos === 0)){
        nextWord.pointer = breaks.pageBoundaries.previous
    }
    else{
        if(pos === 0){
            let prevLine = line - 1
            let prevPos = lines.words[prevLine].length - 1
            nextWord.pointer = {
                line: prevLine,
                page: page,
                pos: prevPos
            }
        }
        else{
            let prevPos = currWord.pos - 1
            nextWord.pointer = {
                line: line,
                page: page,
                pos: prevPos
            }
        }
    }

    return nextWord
}

/**
 * Fetches the first word to the right of the currently
 * supplied word.
 * 
 * @param {object} breaks The line breaks in the page.
 * @param {object} currWord The word to move right from.
 * @param {object} lines The words making up the page.
 * @param {array} tokenData The boundaries of the word.
 * @return {object} The first word to the right of the
 *                  current one.
 */
export const moveRight = (breaks, currWord, lines, tokenData) => {
    let nextWord = {}
    let lastTokenPos = tokenData.positions.length - 1
    let rightToken = tokenData.positions[lastTokenPos]
    let page = rightToken[0]
    let line = rightToken[1]
    let pos = rightToken[2]
    let lastLine = lines.words.length - 1
    let lastLinePos = lines.words[lastLine].length - 1
    if(!(currWord.page === page)){
        nextWord.pointer = breaks.pageBoundaries.next
    }
    else if((line === lastLine) & (pos === lastLinePos)){
        nextWord.pointer = breaks.pageBoundaries.next
    }
    else{
        if(pos === lines.words[line].length - 1){
            let nextLine = line + 1
            let nextPos = 0
            nextWord.pointer = {
                line: nextLine,
                page: page,
                pos: nextPos
            }
        }
        else{
            let nextPos = pos + 1
            nextWord.pointer = {
                line: line,
                page: page,
                pos: nextPos
            }
        }
    }

    return nextWord
}

/**
 * Finds the next word when the word is split across multiple lines.
 * 
 * @param {string} direction The direction to move when searching for
 *                           the next word.
 * @param {object} lines The words comprising the current page.
 * @param {string} side The line boundary, if any, where the word is 
 *                      located
 * @param {object} word The word whose successor is to be found.
 * @return {object} The successor of the current word.
 */
export const processLineBreak = (direction, lines, side, word) => {
    let breaks = lines.breaks
    let line = word.line
    let nextWord = {}
    let tokenData = {}
    let tokenPointer = {}
   
    //Initialize default pointer
    nextWord.pointer = {}

    //Process start of line
    if(side === C.LINE_BOUNDARY.START){
        tokenPointer = breaks.start[line]
        tokenData = breaks.tokens[tokenPointer]
        if(direction === C.DIRECTION.LEFT){
            nextWord = moveLeft(breaks, word, lines, tokenData)
        }
        else{
            nextWord = moveRight(breaks, word, lines, tokenData)
        }
    }
    //Process end of line
    else{
        tokenPointer = breaks.end[line]
        tokenData = breaks.tokens[tokenPointer]
        if(direction === C.DIRECTION.LEFT){
            nextWord = moveLeft(breaks, word, lines, tokenData)
        }
        else{
            nextWord = moveRight(breaks, word, lines, tokenData)
        }
    }

    //Get selected tokens
    let tokenIDs = tokenData.positions.map((token) => {
        let page = token[0] 
        let lineNum = token[1]
        let position = token[2]
        let tokenID = getTokenIdentifier(lineNum, page, position)
        return tokenID
    })
    nextWord.selected = new Set(tokenIDs)

    //Get definition
    nextWord.fulltext = tokenData.fulltext
    
    return nextWord
}