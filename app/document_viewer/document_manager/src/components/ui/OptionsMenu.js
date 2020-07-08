import PropTypes from "prop-types"
import React from "react"
import C from "../../constants"

const optionsMenuID = "document-viewer-options-menu"

export const DisplayOptions = ({selectOption}) =>
    <div id={optionsMenuID}>
        <div onClick={selectOption(C.DOC_VIEWER_OPTIONS.ADD_VOCAB)}>
            Select words to translate
        </div>
        <div onClick={selectOption(C.DOC_VIEWER_OPTIONS.BOOKMARKS)}>
            Manage bookmarks
        </div>
    </div>

export class OptionsMenu extends React.Component{
    render(){
        let interaction = this.props.interaction
        if(interaction === C.DOCUMENT_VIEWER){
            let option = this.props.option
            if(option === C.DOC_VIEWER_OPTIONS.DEFAULT){
                let selectOption = this.props.selectOption
                return(
                    <DisplayOptions selectOption={selectOption}/>
                )
            }
        }
        ///Default to empty tag
        return(
            <div id={optionsMenuID}></div>
        )
    }
}

DisplayOptions.propTypes = {
    selectOption: PropTypes.func
}

OptionsMenu.propTypes = {
    interaction: PropTypes.string,
    option: PropTypes.string,
    selectOption: PropTypes.func
}

OptionsMenu.defaultProps = {
    interaction: C.DOCUMENT_VIEWER,
    option: C.DOC_VIEWER_OPTIONS.DEFAULT,
    selectOption: f=>f
}

export default OptionsMenu