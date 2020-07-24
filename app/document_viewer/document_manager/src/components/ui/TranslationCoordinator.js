import PropTypes from "prop-types"
import React from "react"
import C from "../../constants"
import stylesheet from './stylesheet'
import { grammar } from "../../data/grammar"

const coordinatorID = "translation-coordinator"

const customTextID = "translation-coordinator-custom-text-manager"

const customTextSubmit = "translation-coordinator-custom-text-submit"

const endpointManagerID = "translation-coordinator-endpoint-manager"

const queueManagerID = "translation-coordinator-queue-manager"

const textManagerID = "translation-coordinator-text-manager"

const buildTextManagerKey = (index, text) => {
    let domain = "text-manager"
    let separator = "-"
    let key = domain + separator + index.toString() + separator + text
    return key
}

const processTranslationRequest = (currState, translate) => {
    if(currState.searchPhrase.length > 0){
        translate()
    }
    else{
        let errorMessage = "Translation Queue must have content to be translated."
        window.alert(errorMessage)
    }
}

const submitCustomText = (e, addText) => {
    let enterKey = C.KEYBOARD_INPUT.ENTER
    if(e.keyCode === enterKey){
        let customText = e.target.value
        if(customText){
            addText(customText)
            document.getElementById(customTextSubmit).value=''
        }
        else{
            let errorMessage = "Enter text to add to the translation queue"
            window.alert(errorMessage)
        }
    }
}

export const CustomText = ({addText}) =>
    <div id={customTextID}>
        <input id={customTextSubmit}
               onKeyDown={(e) => submitCustomText(e, addText)}
               type="text"
               placeholder="Enter text here"/>
    </div>

export const EndpointManager = ({setEndpoint}) => 
    <div id={endpointManagerID}>
        Set text boundaries
        <br></br>
        <button className={stylesheet.buttonDivider}
                onClick={() => setEndpoint(C.TEXT_START)}>Start</button>
        <button onClick={() => setEndpoint(C.TEXT_FINISH)}>End</button>
        <br></br>
        <br></br>
    </div>

export const QueueManager = ({clearQueue}) => 
    <div id={queueManagerID}>
        Manage the translation queue
        <br></br>
        <button onClick={() => clearQueue()}>Clear Queue</button>
        <br></br>
        <br></br>
    </div>

export const Punctuation = ({addText, punct}) => 
    <button className={stylesheet.buttonDivider}
            onClick={() => addText(punct)}>{punct}</button>

export const Spacing = ({addText, description, spacing}) =>
    <button onClick={() => addText(spacing)}>{description}</button>

export const TextManager = ({addText}) => 
    <div id={textManagerID}>
        Punctuation
        <br></br>
        {grammar.default.punctuation.map((punct, index) => 
            <Punctuation addText={addText}
                         key={buildTextManagerKey(index, punct)}
                         punct={punct}/>)}
        <br></br>
        <br></br>
        Spacing
        <br></br>
        {Object.keys(grammar.default.spacing).sort().map((description, index) =>
            <Spacing addText={addText}
                     description={description}
                     key={buildTextManagerKey(index, description)}
                     spacing={grammar.default.spacing[description]}/>)}
        <br></br>
        <br></br>
        Custom Text
        <CustomText addText={addText}/>
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
                    <div id={coordinatorID} className={stylesheet.option}>
                        <b className={stylesheet.optionHeader}>Translation Coordinator</b>
                        <br></br>
                        <br></br>
                        <EndpointManager setEndpoint={setEndpoint}/>
                        <QueueManager clearQueue={clearQueue}/>
                        <TextManager addText={addText}/>
                        <br></br>
                        <br></br>
                        <button onClick={() => {
                            processTranslationRequest(translations, translate)
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

CustomText.propTypes = {
    addText: PropTypes.func
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