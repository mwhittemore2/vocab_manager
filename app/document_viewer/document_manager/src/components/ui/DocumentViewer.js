import PropTypes from "prop-types"
import React from "react"
import { Navigator } from './Navigator'
import { Page } from './Page'
import C from '../../constants'

const displayID = "document-viewer"

export const Display = ({cursor=f=>f, lines={}, selectWord=f=>f}) =>
    <div id={displayID}>
        <Page lines={lines} selectWord={selectWord} />
        <Navigator cursor={cursor}
                   results={lines}
                   viewer={displayID}/>
    </div>

export class DocumentViewer extends React.Component{
    render(){
        let interaction = this.props.interaction
        if(interaction === C.DOCUMENT_VIEWER){
            let cursor = this.props.cursor
            let lines = this.props.lines
            let selectWord = this.props.selectWord
            return(
                <Display cursor={cursor}
                         lines={lines}
                         selectWord={selectWord}/>
            )
        }
        ///Default to empty tag
        return(
            <div id={displayID}></div>
        )
    }
}

Display.propTypes = {
    cursor: PropTypes.func,
    lines: PropTypes.object,
    selectWord: PropTypes.func
}

DocumentViewer.propTypes = {
    cursor: PropTypes.func,
    interaction: PropTypes.string,
    lines: PropTypes.object,
    selectWord: PropTypes.func
}

DocumentViewer.defaultProps = {
    cursor: f=>f,
    interaction: C.DOCUMENT_VIEWER,
    lines: {},
    selectWord: f=>f
}

export default DocumentViewer