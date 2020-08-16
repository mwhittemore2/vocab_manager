import React from "react"
import PropTypes from 'prop-types'

/**
 * Displays the raw text comprising a word.
 * 
 * @param {func} selectWord Adds the current word to the translation queue.
 * @param {object} word A detailed JS object representing the current word.
 * @return {html} The HTML representation of the the text of the current word. 
 */
export const Text = ({selectWord=f=>f, word={}}) => 
    <span onClick={() => selectWord(word)}>{word.text}</span>

/**
 * 
 * @param {bool} canColor True if the word should be highlighted, False otherwise.
 * @param {func} selectWord Adds the current word to the translation queue. 
 */
export const Word = ({canColor=false, selectWord=f=>f, word={}}) =>
   canColor ? <b><Text selectWord={selectWord} word={word}/></b> : 
    <Text selectWord={selectWord} word={word}/>

Text.propTypes = {
    selectWord: PropTypes.func,
    word: PropTypes.object
}

Word.propTypes = {
    canColor: PropTypes.bool,
    selectWord: PropTypes.func,
    word: PropTypes.object
}