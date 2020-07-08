import PropTypes from "prop-types"
import React from "react"
import C from '../../constants'

export const Navigator = ({cursor, jumpToPage, results, viewer}) =>
    <div id={viewer.concat("-navigator")}>
        <button id={viewer.concat("-previous")} onClick={cursor(C.PREVIOUS_PAGE, results.currPage)}>
            Previous
        </button>
        <div id={viewer.concat("-current")}>
           <input onKeyDown={(e) => jumpToPage(e)}
                  type="text"
                  placeholder={results.currPage}/>
        </div>
        <button id={viewer.concat("-next")} onClick={cursor(C.NEXT_PAGE, results.currPage)}>
            Next
        </button>
    </div>

Navigator.propTypes = {
    cursor: PropTypes.func,
    jumpToPage: PropTypes.func,
    results: PropTypes.object,
    viewer: PropTypes.string
}