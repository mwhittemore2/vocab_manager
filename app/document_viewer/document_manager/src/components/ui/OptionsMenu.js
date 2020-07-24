import PropTypes from "prop-types"
import React from "react"
import stylesheet from './stylesheets/common'
import C from "../../constants"

const optionsMenuID = "document-viewer-options-menu"

export const DisplayOptions = ({selectOption}) =>
    <div id={optionsMenuID} className={stylesheet.option}>
        <b className={stylesheet.optionHeader}>Document Viewer Options</b>
        <br></br>
        <br></br>
        <ul className={stylesheet.chooseOption}>
            <div onClick={() => selectOption(C.DOC_VIEWER_OPTIONS.TRANSLATION_COORDINATOR)}>
                <li>Select words to translate</li>
            </div>
            <br></br>
            <div onClick={() => window.alert("This feature isn't implemented yet")}>
                <li>Manage bookmarks</li>
            </div>
        </ul>
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

/*
OptionsMenu.defaultProps = {
    interaction: C.DOCUMENT_VIEWER,
    option: C.DOC_VIEWER_OPTIONS.DEFAULT,
    selectOption: f=>f
}*/

export default OptionsMenu