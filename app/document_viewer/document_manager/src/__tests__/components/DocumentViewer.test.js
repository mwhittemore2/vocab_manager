import React from "react"
import { shallow } from "enzyme"
import toJSON from 'enzyme-to-json'
import { Display, DocumentViewer } from '../../components/ui/DocumentViewer'
import C from '../../constants'

let cursor = jest.fn()
let lines = {
        currPage: 1,
        words: [],
        selected: new Set([])
    }
lines.words.push(["Die ", "Welt "])
lines.words.push(["ist ", "meine ", "Vorstellung"])
let selector = jest.fn()

describe("Display", () =>{
    it("show page", () =>{
        let txt = toJSON(
                      shallow(<Display cursor={cursor}
                                       lines={lines}
                                       selector={selector}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("DocumentViewer", () => {
    it("use viewer", () => {
        let interaction = C.DOCUMENT_VIEWER
        let txt = toJSON(
                      shallow(<DocumentViewer cursor={cursor}
                                              interaction={interaction}
                                              lines={lines}
                                              selectWord={selector}/>
                     )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("viewer inactive", () => {
        let interaction = C.DOCUMENT_SELECTOR
        let txt = toJSON(
                      shallow(<DocumentViewer cursor={cursor}
                                              interaction={interaction}
                                              lines={lines}
                                              selectWord={selector}/>
                      )  
                  )
        expect(txt).toMatchSnapshot()
    })
})

