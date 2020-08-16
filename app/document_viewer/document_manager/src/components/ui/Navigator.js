import PropTypes from "prop-types"
import React from "react"
import stylesheet from './stylesheets/common'
import C from '../../constants'

/**
 * Enables the user to move to different pages of a collection
 * that are displayed in some higher-level interface.
 * 
 * @param {func} cursor Function for moving to previous or next page.
 * @param {func} jumpToPage Function for moving to a specified page.
 * @param {object} results The collection to be navigated.
 * @param {string} viewer The name of the interface for viewing the collection.
 * @return {html} The HTML representation of the navigator.
 */
export const Navigator = ({cursor, jumpToPage, results, viewer}) =>
    <div id={viewer.concat("-navigator")} className={stylesheet.navigator}>
        <button id={viewer.concat("-previous")}
                className={stylesheet.primaryButton} 
                onClick={() => cursor(C.PREVIOUS_PAGE, results.currPage)}>
            Previous
        </button>
        <input id={viewer.concat("-current")}
               onKeyDown={(e) => jumpToPage(e)}
               type="text"
               placeholder={results.currPage}/>
        <button id={viewer.concat("-next")}
                className={stylesheet.primaryButton} 
                onClick={() => cursor(C.NEXT_PAGE, results.currPage)}>
            Next
        </button>
    </div>

Navigator.propTypes = {
    cursor: PropTypes.func,
    jumpToPage: PropTypes.func,
    results: PropTypes.object,
    viewer: PropTypes.string
}