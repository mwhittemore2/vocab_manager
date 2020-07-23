import PropTypes from "prop-types"
import React from "react"
import C from '../../constants'
import { Loading } from './Loading'
import { Navigator } from './Navigator'

const matchesID = "translation-matches"

const viewerID = "translation-viewer"

const buildDefinitionKey = (index, page) => {
    let domain = "tr-def"
    let separator = "-"
    let key = domain + separator + page.toString() + separator + index.toString()
    return key
}

const buildMatchKey = (index, page) => {
    let domain = "tr-match"
    let separator = "-"
    let key = domain + separator + page.toString() + separator + index.toString()
    return key
}

export const Definitions = ({match, page}) =>
    <ol>
        {match.definitions.map((definition, index) => 
            {
                return(<li key={buildDefinitionKey(index, page)}>{definition}</li>)   
            }
        )}
    </ol>

export const BaseFormMatch = ({match, page}) =>
    <div>
        Text: {match.text}
        <br></br>
        POS: {match.pos}
        <br></br>
        Definitions:
        <Definitions match={match}
                     page={page}/>
    </div>

export const DerivedFormMatch = ({match, page}) =>
    <div>
        Text: {match.text}
        <br></br>
        Definitions:
        <Definitions match={match}
                     page={page}/>
        <br></br>
        See Also: {match.see_also.text} ({match.see_also.pos})
        <br></br>
    </div>

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
                        <div id={viewerID}>
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

/*
TranslationViewer.defaultProps = {
    closeViewer: f=>f,
    cursor: f=>f,
    interaction: C.DOCUMENT_VIEWER,
    jumpToPage: f=>f,
    loaded: {},
    option: C.DOC_VIEWER_OPTIONS.DEFAULT,
    translations: {}
}*/

export default TranslationViewer