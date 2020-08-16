import PropTypes from "prop-types"
import React from "react"
import stylesheet from './stylesheets/common'
import C from '../../constants'

const queueID = "translation-queue"

/**
 * Assigns a unique identifier to an element of the
 * translation queue.
 * 
 * @param {number} index The position of the element in the queue.
 * @param {string} word The text of the element in the queue.
 * @return {string} The queue element identifier.
 */
const buildKey = (index, word) => {
    let domain = "tq"
    let separator = "-"
    let key = domain + separator + index.toString() + separator + word
    return key
}

/**
 * A higher-level abstraction of a word in the translation queue.
 * 
 * @param {number} position The position of the word in the queue.
 * @param {string} remove Deletes the word from the queue.
 * @param {string} text The raw text comprising the word.
 * @return {html} The HTML representation of the word in the queue.
 */
export const QueueElement = ({position, remove, text}) =>
    <span onClick={() => remove(position)}>{text}</span>

/**
 * Renders the translation queue above the current page the user
 * is reading.
 */
export class TranslationQueue extends React.Component{
    render(){
        let interaction = this.props.interaction
        if(interaction === C.DOCUMENT_VIEWER){
            let remove = this.props.remove
            let translations = this.props.translations
            return(
                <div id={queueID} className={stylesheet.displayQueue}>
                    {translations.searchPhrase.map((word, index) =>
                        <QueueElement key={buildKey(index, word.fulltext)}
                                      position={index}
                                      remove={remove}
                                      text={word.fulltext}/>)}
                </div>
            )
        }
        return(
            <div id={queueID}></div>
        )
    }
}

QueueElement.propTypes = {
    position: PropTypes.number,
    remove: PropTypes.func,
    text: PropTypes.string
}

TranslationQueue.propTypes = {
    interaction: PropTypes.string,
    remove: PropTypes.func,
    translations: PropTypes.object
}

TranslationQueue.defaultProps = {
    interaction: C.DOCUMENT_SELECTOR,
    remove: f=>f,
    translations: {}
}

export default TranslationQueue