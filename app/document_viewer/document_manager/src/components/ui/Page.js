import React from "react"
import PropTypes from 'prop-types'
import { Word } from './Word'

/**
 * Assigns a unique identifier to a line from a given page.
 * 
 * @param {number} index The position of the line in the page.
 * @param {object} page The page in which the line occurs.
 * @return {string} The line identifier.
 */
const buildLineKey = (index, page) => {
    let domain = "line"
    let separator = "-"
    let key = domain + separator + page.currPage.toString() + separator + index.toString()
    return key
}

/**
 * Assigns a unique identifier to a word in a given line.
 * 
 * @param {number} index The position of the word in a line.
 * @param {object} word The word to be assigned an identifier.
 * @return {string} The word identifier.
 */
const buildWordKey = (index, word) => {
    let domain = "word"
    let separator = "-"
    let key = domain + separator + index.toString() + separator + word
    return key
}

/**
 * Creates a more detailed representation of a word occurring
 * in the page in order to facilitate downstream processing.
 * 
 * @param {number} index The position of the word in its corresponding line.
 * @param {number} line The position of the line in its corresponding page.
 * @param {number} page The number of the page in its corresponding document.
 * @param {string} word The actual text of the chosen word.
 * @return {object} The word represented as a more detailed JS object.
 */
const buildWord = (index, line, page, word) => {
    return {line: line, page: page.currPage, pos: index, text: word}
}

/**
 * Determines whether the current word should be highlighted in the browser.
 * 
 * @param {number} line The position of the line in its corresponding page.
 * @param {number} pos The position of the word in its corresponding line. 
 * @param {object} page The page the user is currently reading.
 * @return {bool} True if the word can be highlighted, False otherwise.
 */
const canColor = (line, pos, page) => {
    let separator = ":"
    let word = page.currPage.toString() + separator + line.toString() + separator + pos.toString()
    let decision = page.selected.has(word)
    return decision
}

/**
 * Displays a line of text from the current page the user is reading.
 * 
 * @param {array} line The words to be displayed.
 * @param {number} num The position of the line in its corresponding page.
 * @param {object} page The page the user is currently reading.
 * @param {func} selectWord Adds the selected word to the translation queue.
 * @return {html} The HTML representation of the line.
 */
export const Line = ({line, num, page, selectWord}) => {
    return (
        <div>
            {line.map((word, index) => 
                <Word canColor={canColor(num, index, page)}
                      key={buildWordKey(index, word)}
                      selectWord={selectWord}
                      word={buildWord(index, num, page, word)}/>)}
            <br></br>
        </div>       
    )    
}

/**
 * Displays the current page of the document the user is reading.
 * 
 * @param {object} lines The lines comprising the page.
 * @param {func} selectWord Adds the selected word to the 
 *                          translation queue.
 * @return {html} The HTML representation of the page. 
 */
export const Page = ({lines={}, selectWord=f=>f}) =>
    <div className="page">
        {lines.words.map((line, index) =>
            <Line key ={buildLineKey(index, lines)}
                  line={line}
                  num={index}
                  page={lines}
                  selectWord={selectWord}/>)}
    </div>

Line.propTypes = {
    line: PropTypes.array,
    num: PropTypes.number,
    page: PropTypes.object,
    selectWord: PropTypes.func
}

Page.propTypes = {
    lines: PropTypes.object,
    selectWord: PropTypes.func
}