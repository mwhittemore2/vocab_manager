import React from "react"
import { shallow } from "enzyme"
import toJSON from 'enzyme-to-json'
import { Navigator } from '../../components/ui/Navigator'
import C from '../../constants'

describe("Navigator", () => {
    let cursor
    let jumpToPage
    let results
    let viewer
    beforeEach(() => {
        cursor = jest.fn()
        jumpToPage = jest.fn()
        results = {
            currPage: 1
        }
        viewer = C.DOCUMENT_VIEWER
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("correct display", () => {
        let txt = toJSON(
                      shallow(<Navigator cursor={cursor}
                                         jumpToPage={jumpToPage}
                                         results={results}
                                         viewer={viewer}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("previous page", () => {
        let previous = "#" + C.DOCUMENT_VIEWER + "-previous"
        shallow(<Navigator cursor={cursor}
                           jumpToPage={jumpToPage}
                           results={results}
                           viewer={viewer}/>
        )
        .find(previous)
        .simulate('click')
        expect(cursor).toBeCalled()    
    })

    it("next page", () => {
        let next = "#" + C.DOCUMENT_VIEWER + "-next"
        shallow(<Navigator cursor={cursor}
                           jumpToPage={jumpToPage}
                           results={results}
                           viewer={viewer}/>
        )
        .find(next)
        .simulate('click')
        expect(cursor).toBeCalled()
    })
})