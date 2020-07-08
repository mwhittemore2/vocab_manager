import React from "react"
import PropTypes from 'prop-types'
import { Word } from './Word'

const buildLineKey = (index, page) => {
    let domain = "line"
    let separator = "-"
    let key = domain + separator + page.currPage.toString() + separator + index.toString()
    return key
}

const buildWordKey = (index, word) => {
    let domain = "word"
    let separator = "-"
    let key = domain + separator + index.toString() + separator + word
    return key
}

const buildWord = (index, line, page, word) => {
    return {line: line, page: page.currPage, pos: index, text: word}
}

const canColor = (line, pos, page) => {
    let separator = ":"
    let word = page.currPage.toString() + separator + line.toString() + separator + pos.toString()
    let decision = page.selected.has(word)
    return decision
}

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