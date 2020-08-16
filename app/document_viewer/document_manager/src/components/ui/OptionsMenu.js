import PropTypes from "prop-types"
import React from "react"
import stylesheet from './stylesheets/common'
import C from "../../constants"

const optionsMenuID = "document-viewer-options-menu"

/**
 * Lists the various tools available for working with the current
 * document the user is reading.
 * 
 * @param {func} selectOption Selects a tool for working with the current document. 
 * @return {html} The HTML representation of the available tools.
 */
export const DisplayOptions = ({selectOption}) =>
    <div id={optionsMenuID} className={stylesheet.option}>
        <b className={stylesheet.optionHeader}>Document Viewer Options</b>
        <br></br>
        <br></br>
        <ul className={stylesheet.chooseOption}>
            <div onClick={() => selectOption(C.DOC_VIEWER_OPTIONS.TRANSLATION_COORDINATOR)}>
                <li>Open Translation Coordinator</li>
            </div>
            <br></br>
            <div onClick={() => window.alert("This feature isn't implemented yet")}>
                <li>Manage bookmarks</li>
            </div>
        </ul>
    </div>

/**
 * Renders the list of available tools for working with the
 * current document that the user is reading.
 */
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

OptionsMenu.defaultProps = {
    interaction: C.DOCUMENT_SELECTOR,
    option: C.DOC_VIEWER_OPTIONS.DEFAULT,
    selectOption: f=>f
}

export default OptionsMenu