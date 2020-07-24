import PropTypes from "prop-types"
import React from "react"
import stylesheet from './stylesheets/common'
import C from '../../constants'

export const Navigator = ({cursor, jumpToPage, results, viewer}) =>
    <div id={viewer.concat("-navigator")} className={stylesheet.navigator}>
        <button id={viewer.concat("-previous")} onClick={() => cursor(C.PREVIOUS_PAGE, results.currPage)}>
            Previous
        </button>
        <input id={viewer.concat("-current")}
               onKeyDown={(e) => jumpToPage(e)}
               type="text"
               placeholder={results.currPage}/>
        <button id={viewer.concat("-next")} onClick={() => cursor(C.NEXT_PAGE, results.currPage)}>
            Next
        </button>
    </div>

Navigator.propTypes = {
    cursor: PropTypes.func,
    jumpToPage: PropTypes.func,
    results: PropTypes.object,
    viewer: PropTypes.string
}