import PropTypes from "prop-types"
import React from "react"
import C from "../../constants"
import stylesheet from './stylesheets/common'
import { grammar } from "../../data/grammar"

const coordinatorID = "translation-coordinator"

const customTextID = "translation-coordinator-custom-text-manager"

const customTextSubmit = "translation-coordinator-custom-text-submit"

const endpointManagerID = "translation-coordinator-endpoint-manager"

const queueManagerID = "translation-coordinator-queue-manager"

const textManagerID = "translation-coordinator-text-manager"

/**
 * Assigns a unique key to a button in a submenu which can manage 
 * the content appearing in the translation queue.
 * 
 * @param {number} index The position of the button in the submenu.
 * @param {string} text The text of the button.
 * @return {string} The button identifier.
 */
const buildTextManagerKey = (index, text) => {
    let domain = "text-manager"
    let separator = "-"
    let key = domain + separator + index.toString() + separator + text
    return key
}

/**
 * Sends along the text in the translation queue to be translated,
 * if it's possible to do so.
 * 
 * @param {object} currState The current state of the translation queue.
 * @param {func} translate Triggers a translation request on the server.
 */
const processTranslationRequest = (currState, translate) => {
    if(currState.searchPhrase.length > 0){
        translate()
    }
    else{
        let errorMessage = "Translation Queue must have content to be translated."
        window.alert(errorMessage)
    }
}

/**
 * Adds user-supplied raw text to the translation queue,
 * if user pressed the enter key.
 * 
 * @param {object} e A key press event.
 * @param {func} addText Adds raw text to the translation queue.
 */
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

/**
 * A menu for preparing raw text supplied by the user for
 * eventual translation.
 * 
 * @param {func} addText Adds raw text to the translation queue.
 * @return {html} The HTML representation of the custom text menu 
 */
export const CustomText = ({addText}) =>
    <div id={customTextID}>
        <input id={customTextSubmit}
               onKeyDown={(e) => submitCustomText(e, addText)}
               type="text"
               placeholder="Enter text here"/>
    </div>

/**
 * A menu for selecting a continuous span of text to be
 * translated.
 * 
 * @param {func} setEndpoint Determines the boundaries of the text span.
 * @return {html} The HTML representation of the menu. 
 */
export const EndpointManager = ({setEndpoint}) => 
    <div id={endpointManagerID}>
        Set text boundaries
        <br></br>
        <button className={stylesheet.primaryButton}
                onClick={() => setEndpoint(C.TEXT_START)}>Start</button>
        <button className={stylesheet.primaryButton}
                onClick={() => setEndpoint(C.TEXT_FINISH)}>End</button>
        <br></br>
        <br></br>
    </div>

/**
 * A menu for providing more granular control over the contents
 * of the translation queue.
 * 
 * @param {func} clearQueue Deletes all content in the translation queue.
 * @return {html} The HTML representation of the menu. 
 */
export const QueueManager = ({clearQueue}) => 
    <div id={queueManagerID}>
        Manage the translation queue
        <br></br>
        <button className={stylesheet.primaryButton}
                onClick={() => clearQueue()}>Clear Queue</button>
        <br></br>
        <br></br>
    </div>

/**
 * A button that adds specific punctuation to the
 * translation queue.
 * 
 * @param {func} addText Adds the specified punctuation to the
 *                       translation queue.
 * @param {string} punct The specific punctuation to add to the
 *                       translation queue.
 * @return {html} The HTML representation of the button.
 */
export const Punctuation = ({addText, punct}) => 
    <button className={stylesheet.primaryButton}
            onClick={() => addText(punct)}>{punct}</button>

/**
 * A button that adds a specific type of spacing to the
 * translation queue.
 * 
 * @param {func} addText Adds the specified spacing to the
 *                       translation queue.
 * @param {string} description A natural language description
 *                             of the type of spacing to be added.
 * @param {string} spacing The spacing to be added.
 * @return {html} The HTML representation of the menu. 
 */
export const Spacing = ({addText, description, spacing}) =>
    <button className={stylesheet.primaryButton}
            onClick={() => addText(spacing)}>{description}</button>

/**
 * Top-level menu for adding text to the translation queue.
 * 
 * @param {func} addText Adds the specified text to the translation
 *                       queue.
 * @return {html} The HTML representation of the the menu.
 */
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

/**
 * Renders the menus used to build up a candidate phrase
 * to be translated.
 */
export class TranslationCoordinator extends React.Component{
    render(){
        let interaction = this.props.interaction
        if(interaction === C.DOCUMENT_VIEWER){
            let option = this.props.option
            if(option === C.DOC_VIEWER_OPTIONS.TRANSLATION_COORDINATOR){
                let addText = this.props.addText
                let clearQueue = this.props.clearQueue
                let closeViewer = this.props.closeViewer
                let setEndpoint = this.props.setEndpoint
                let translate = this.props.translate
                let translations = this.props.translations
                return(
                    <div id={coordinatorID} className={stylesheet.option}>
                        <button onClick={() => closeViewer()}>Close</button>
                        <br></br>
                        <b className={stylesheet.optionHeader}>Translation Coordinator</b>
                        <br></br>
                        <br></br>
                        <EndpointManager setEndpoint={setEndpoint}/>
                        <QueueManager clearQueue={clearQueue}/>
                        <TextManager addText={addText}/>
                        <br></br>
                        <br></br>
                        <button className={stylesheet.primaryButton}
                                onClick={() => {
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
    closeViewer: PropTypes.func,
    interaction: PropTypes.string,
    option: PropTypes.string,
    setEndpoint: PropTypes.func,
    translate: PropTypes.func,
    translations: PropTypes.object
}

TranslationCoordinator.defaultProps = {
    addText: f=>f,
    clearQueue: f=>f,
    closeViewer: f=>f,
    interaction: C.DOCUMENT_SELECTOR,
    option: C.DOC_VIEWER_OPTIONS.DEFAULT,
    setEndpoint: f=>f,
    translate: f=>f,
    translations: {}
}

export default TranslationCoordinator