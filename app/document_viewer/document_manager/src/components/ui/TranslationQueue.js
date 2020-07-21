import PropTypes from "prop-types"
import React from "react"
import C from '../../constants'

const queueID = "translation-queue"

const buildKey = (index, word) => {
    let domain = "tq"
    let separator = "-"
    let key = domain + separator + index.toString() + separator + word
    return key
}

export const QueueElement = ({position, remove, text}) =>
    <span onClick={() => remove(position)}>{text}</span>

export class TranslationQueue extends React.Component{
    render(){
        let interaction = this.props.interaction
        if(interaction === C.DOCUMENT_VIEWER){
            let remove = this.props.remove
            let translations = this.props.translations
            return(
                <div id={queueID}>
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

export default TranslationQueue