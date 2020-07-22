import PropTypes from "prop-types"
import React from "react"
import { Navigator } from './Navigator'
import { Page } from './Page'
import C from '../../constants'

const displayID = "document-viewer"

export const Display = ({cursor, jumpToPage, lines, selectWord}) =>
    <div id={displayID}>
        <Page lines={lines} selectWord={selectWord} />
        <Navigator cursor={cursor}
                   jumpToPage={jumpToPage}
                   results={lines}
                   viewer={displayID}/>
    </div>

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