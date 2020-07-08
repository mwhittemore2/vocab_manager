import React from "react"
import PropTypes from 'prop-types'

export const Text = ({selectWord=f=>f, word={}}) => 
    <span onClick={selectWord(word)}>{word.text}</span>

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