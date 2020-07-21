import PropTypes from "prop-types"
import React from "react"
import C from "../../constants"
import { grammar } from "../../data/grammar"

const coordinatorID = "translation-coordinator"

const endpointManagerID = "translation-coordinator-endpoint-manager"

const queueManagerID = "translation-coordinator-queue-manager"

const textManagerID = "translation-coordinator-text-manager"

const buildTextManagerKey = (index, text) => {
    let domain = "text-manager"
    let separator = "-"
    let key = domain + separator + index.toString() + separator + text
    return key
}

export const EndpointManager = ({setEndpoint}) => 
    <div id={endpointManagerID}>
        Set the boundaries of the text to be translated
        <br></br>
        <button onClick={() => setEndpoint(C.TEXT_START)}>Start</button>
        <button onClick={() => setEndpoint(C.TEXT_FINISH)}>Finish</button>
    </div>

export const QueueManager = ({clearQueue}) => 
    <div id={queueManagerID}>
        Control the content of the translation queue
        <br></br>
        <button onClick={() => clearQueue()}>Clear Queue</button>
    </div>

export const Punctuation = ({addText, punct}) => 
    <button onClick={() => addText(punct)}>{punct}</button>

export const Spacing = ({addText, description, spacing}) =>
    <button onClick={() => addText(spacing)}>{description}</button>

export const TextManager = ({addText}) => 
    <div id={textManagerID}>
        Select the text to be added to the translation queue.
        <br></br>
        Punctuation
        <br></br>
        {grammar.default.punctuation.map((punct, index) => 
            <Punctuation addText={addText}
                         key={buildTextManagerKey(index, punct)}
                         punct={punct}/>)}
        <br></br>
        Spacing
        <br></br>
        {Object.keys(grammar.default.spacing).sort().map((description, index) =>
            <Spacing addText={addText}
                     description={description}
                     key={buildTextManagerKey(index, description)}
                     spacing={grammar.default.spacing[description]}/>)}
        <br></br>
        Custom Text
    </div>

export class TranslationCoordinator extends React.Component{
    render(){
        let interaction = this.props.interaction
        if(interaction === C.DOCUMENT_VIEWER){
            let option = this.props.option
            if(option === C.DOC_VIEWER_OPTIONS.TRANSLATION_COORDINATOR){
                let addText = this.props.addText
                let clearQueue = this.props.clearQueue
                let setEndpoint = this.props.setEndpoint
                let translate = this.props.translate
                let translations = this.props.translations
                return(
                    <div id={coordinatorID}>
                        <TextManager addText={addText}/>
                        <EndpointManager setEndpoint={setEndpoint}/>
                        <QueueManager clearQueue={clearQueue}/>
                        <button onClick={() => {
                            if(translations.searchPhrase.length > 0){
                                translate()
                            }
                            else{
                                let errorMessage = "Translation Queue must have content to be translated."
                                window.alert(errorMessage)
                            }
                        }}>Get Translations</button>
                    </div>
                )
            }
        }
        return(
            <div id={coordinatorID}></div>
        )
    }
}

EndpointManager.propTypes = {
    setEndpoint: PropTypes.func
}

QueueManager.propTypes = {
    clearQueue: PropTypes.func
}

Punctuation.propTypes = {
    addText: PropTypes.func,
    punct: PropTypes.string
}

Spacing.propTypes = {
    addText: PropTypes.func,
    description: PropTypes.string,
    spacing: PropTypes.string
}

TextManager.propTypes = {
    addText: PropTypes.func
}

TranslationCoordinator.propTypes = {
    addText: PropTypes.func,
    clearQueue: PropTypes.func,
    interaction: PropTypes.string,
    option: PropTypes.string,
    setEndpoint: PropTypes.func,
    translate: PropTypes.func,
    translations: PropTypes.object
}

export default TranslationCoordinator