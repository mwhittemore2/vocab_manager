import PropTypes from "prop-types"
import React from "react"
import C from '../../constants'
import { Loading } from './Loading'
import { Navigator } from './Navigator'

const matchesID = "translation-matches"

const viewerID = "translation-viewer"

/**
 * Assigns a unique identifier to each definition in a list
 * of definitions.
 * 
 * @param {number} index The position of the definition in the list. 
 * @param {number} page The current page of translation results.
 * @return {string} The definition identifier.
 */
const buildDefinitionKey = (index, page) => {
    let domain = "tr-def"
    let separator = "-"
    let key = domain + separator + page.toString() + separator + index.toString()
    return key
}

/**
 * Assigns a unique identifier to each result of the user's
 * translation query.
 * 
 * @param {number} index The position of the match in the result set.
 * @param {number} page The current page of translation results.
 * @return {string} The match identifier
 */
const buildMatchKey = (index, page) => {
    let domain = "tr-match"
    let separator = "-"
    let key = domain + separator + page.toString() + separator + index.toString()
    return key
}

/**
 * A list of target-language definitions/translations based on the
 * user's query.
 * 
 * @param {object} match A translation of the user's query.
 * @param {number} page The current page of translation results.
 * @return {html} The HTML representation of the definitions.
 */
export const Definitions = ({match, page}) =>
    <ol>
        {match.definitions.map((definition, index) => 
            {
                return(<li key={buildDefinitionKey(index, page)}>{definition}</li>)   
            }
        )}
    </ol>

/**
 * A simple translation of the user's query.
 * 
 * @param {object} match The translation.
 * @param {number} page The current page of translation results.
 * @return {html} The HTML representation of the translation.
 */
export const BaseFormMatch = ({match, page}) =>
    <div>
        Text: {match.text}
        <br></br>
        POS: {match.pos}
        <br></br>
        Definition: {match.definition}
    </div>

/**
 * A translation with suggestions for similar phrases
 * in the base language.
 * 
 * @param {object} match The translation
 * @param {number} page The current page of translation results.
 * @return {html} The HTML representation of the translation. 
 */
export const DerivedFormMatch = ({match, page}) =>
    <div>
        Text: {match.text}
        <br></br>
        Definition: {match.definition}
        <br></br>
        See Also: {match.see_also.text} ({match.see_also.pos})
        <br></br>
    </div>

/**
 * Displays the translations of the user's query.
 * 
 * @param {object} translations The translations to be displayed.
 * @return {html} The HTML representation of the matching translations.
 */
export const ViewMatches = ({translations}) =>
    <div id={matchesID}>
        {translations.matches.map((match, index) =>
            ('see_also' in match) ?
              <DerivedFormMatch key={buildMatchKey(index, translations.currPage)}
                                match={match}
                                page={translations.currPage}/> :
              <BaseFormMatch key={buildMatchKey(index, translations.currPage)}
                             match={match}
                             page={translations.currPage}/>
        )}
    </div>

/**
 * Renders the tool for viewing translations of a user's query.
 */
export class TranslationViewer extends React.Component{
    render(){
        let interaction = this.props.interaction
        if(interaction === C.DOCUMENT_VIEWER){
            let option = this.props.option
            if(option === C.TRANSLATION_VIEWER){
                let loaded = this.props.loaded[C.TRANSLATION_VIEWER]
                if(loaded){
                    let closeViewer = this.props.closeViewer
                    let cursor = this.props.cursor
                    let jumpToPage = this.props.jumpToPage
                    let translations = this.props.translations
                    return(
                        <div id={viewerID} className="option">
                            <button onClick={() => closeViewer()}>Close</button>
                            <ViewMatches translations={translations}/>
                            <Navigator cursor={cursor}
                                       jumpToPage={jumpToPage}
                                       results={translations}
                                       viewer={viewerID}/>
                        </div>
                    )
                }
                else{
                    return(
                        <div id={viewerID} className="option">
                            <Loading/>
                        </div>
                    )
                }
            }
        }
        return( 
            <div id={viewerID}></div>
        )
    }
}

BaseFormMatch.propTypes = {
    match: PropTypes.object,
    page: PropTypes.number
}

Definitions.propTypes = {
    match: PropTypes.object,
    page: PropTypes.number
}

DerivedFormMatch.propTypes = {
    match: PropTypes.object,
    page: PropTypes.number
}

TranslationViewer.propTypes = {
    closeViewer: PropTypes.func,
    cursor: PropTypes.func,
    interaction: PropTypes.string,
    jumpToPage: PropTypes.func,
    loaded: PropTypes.object,
    option: PropTypes.string,
    translations: PropTypes.object
}

TranslationViewer.defaultProps = {
    closeViewer: f=>f,
    cursor: f=>f,
    interaction: C.DOCUMENT_SELECTOR,
    jumpToPage: f=>f,
    loaded: {},
    option: C.DOC_VIEWER_OPTIONS.DEFAULT,
    translations: {}
}

ViewMatches.propTypes = {
    translations: PropTypes.object
}

export default TranslationViewer