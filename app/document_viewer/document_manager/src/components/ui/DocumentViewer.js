import PropTypes from "prop-types"
import React from "react"
import { Navigator } from './Navigator'
import { Page } from './Page'
import stylesheet from './stylesheets/common'
import C from '../../constants'

const displayID = "document-viewer"

/**
 * Manages the current page that the user is reading.
 * 
 * @param {func} cursor Function for moving to previous or next page.
 * @param {func} jumpToPage Function for moving to a specified page.
 * @param {object} lines The text of the currently displayed page.
 * @param {func} selectWord Adds the user-selected word to the translation 
 *                          queue.
 * @return {html} The HTML representation of the current page.
 */
export const Display = ({cursor, jumpToPage, lines, selectWord}) =>
    <div id={displayID} className={stylesheet.displayDocumentViewer}>
        <Page lines={lines} selectWord={selectWord} />
        <Navigator cursor={cursor}
                   jumpToPage={jumpToPage}
                   results={lines}
                   viewer={displayID}/>
    </div>

/**
 * Renders the interface for reading and traversing a document.
 */
export class DocumentViewer extends React.Component{
    render(){
        let interaction = this.props.interaction
        if(interaction === C.DOCUMENT_VIEWER){
            let cursor = this.props.cursor
            let jumpToPage = this.props.jumpToPage
            let lines = this.props.lines
            let selectWord = this.props.selectWord
            return(
                <Display cursor={cursor}
                         jumpToPage={jumpToPage}
                         lines={lines}
                         selectWord={selectWord}/>
            )
        }
        return(
            <div id={displayID}></div>
        )
    }
}

Display.propTypes = {
    cursor: PropTypes.func,
    jumpToPage: PropTypes.func,
    lines: PropTypes.object,
    selectWord: PropTypes.func
}

DocumentViewer.propTypes = {
    cursor: PropTypes.func,
    interaction: PropTypes.string,
    jumpToPage: PropTypes.func,
    lines: PropTypes.object,
    selectWord: PropTypes.func
}

DocumentViewer.defaultProps = {
    cursor: f=>f,
    interaction: C.DOCUMENT_SELECTOR,
    jumpToPage: f=>f,
    lines: {},
    selectWord: f=>f
}

export default DocumentViewer