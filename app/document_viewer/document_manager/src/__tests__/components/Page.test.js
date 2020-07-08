import React from "react"
import { shallow } from "enzyme"
import toJSON from 'enzyme-to-json'
import { Line, Page } from '../../components/ui/Page'

describe("Line component", () => {
    let index
    let line
    let page
    let selector
    let separator
    beforeEach(() => {
        index = 5
        line = ["Die ", "Welt ", "ist ", "meine ", "Vorstellung"]
        page = {
            currPage: 10,
            selected: new Set([])
        }
        selector = jest.fn()
        separator = ":"
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("raw line", () => {
        let txt = toJSON(
                      shallow(<Line line={line}
                                    num={index}
                                    page={page}
                                    selectWord={selector}/>
                        
                    )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("select first word", () => {
        let firstWordPos = "0"
        let wordKey = page.currPage.toString() + separator
        wordKey = wordKey + index.toString() + separator
        wordKey = wordKey + firstWordPos
        page.selected = new Set([wordKey])
        let txt = toJSON(
                      shallow(<Line line={line}
                                    num={index}
                                    page={page}
                                    selectWord={selector}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("select middle word", () => {
        let middleWordPos = "2"
        let wordKey = page.currPage.toString() + separator
        wordKey = wordKey + index.toString() + separator 
        wordKey = wordKey + middleWordPos
        page.selected = new Set([wordKey])
        let txt = toJSON(
                      shallow(<Line line={line}
                                    num={index}
                                    page={page}
                                    selectWord={selector}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("select final word", () => {
        let lastWordPos = "4"
        let wordKey = page.currPage.toString() + separator
        wordKey = wordKey + index.toString() + separator
        wordKey = wordKey + lastWordPos
        page.selected = new Set([wordKey])
        let txt = toJSON(
                      shallow(<Line line={line}
                                    num={index}
                                    page={page}
                                    selectWord={selector}/>
                      )  
                  )
        expect(txt).toMatchSnapshot()
    })

    it("select multiple words", () => {
        let keyTemplate = page.currPage.toString() + separator
        keyTemplate = keyTemplate + index.toString() + separator
        let wordPos = "3"
        let w1 = keyTemplate + wordPos
        wordPos = "4"
        let w2 = keyTemplate + wordPos
        page.selected = new Set([w1, w2])
        let txt = toJSON(
                      shallow(<Line line={line}
                                    num={index}
                                    page={page}
                                    selectWord={selector}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

})

describe("Page component", () => {
    let lines
    let selector
    beforeEach(() => {
        lines = {
            currPage: 10,
            selected: new Set([]),
            words: []
        }
        selector = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("no lines", () => {
        let txt = toJSON(
                      shallow(<Page lines={lines} 
                                    selectWord={selector}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("single line", () => {
        lines.words.push(["Die ", "Welt"])
        let txt = toJSON(
                      shallow(<Page lines={lines}
                                    selectWord={selector}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("multiple lines", () => {
        lines.words.push(["Die ", "Welt "])
        lines.words.push(["ist ", "meine ", "Vorstellung"])
        let txt = toJSON(
                      shallow(<Page lines={lines}
                                    selectWord={selector}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })
})