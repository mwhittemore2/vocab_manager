import React from "react"
import { shallow } from "enzyme"
import toJSON from 'enzyme-to-json'
import { Text, Word } from "../../components/ui/Word"

describe("Text component", () =>{
    let word
    let selector
    beforeEach(() => {
        word = {
            text: "Welt"
        }
        selector = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("check raw text", () => {
        let txt = toJSON(
                      shallow(<Text selectWord={selector}
                                    word={word} />
                      )
                      .find('span')
                  )
        expect(txt).toMatchSnapshot()
    })

    it("select word", () => {
        shallow(<Text selectWord={selector}
                      word={word}/>
        )
        .find('span')
        .simulate('click')
        expect(selector).toBeCalled()
    })
})

describe("Word component", () => {
    let word
    let selector
    beforeEach(() => {
        word = {
            text: "Welt"
        }
        selector = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("Selected word", () => {
        let txt = toJSON(
                      shallow(<Word canColor={true}
                                    selectWord={selector}
                                    word={word}/>
                      )
                      .find('b')
                      .html()
                  )
        expect(txt).toMatchSnapshot()
    })

    it("Unselected word", () => {
        let txt = toJSON(
                      shallow(<Word canColor={false}
                                    selectWord={selector}
                                    word={word}/>)
                      .html()
                  )
        expect(txt).toMatchSnapshot()
    })
})