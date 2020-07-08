import React from "react"
import { shallow } from "enzyme"
import toJSON from 'enzyme-to-json'
import { DisplayOptions, OptionsMenu } from '../../components/ui/OptionsMenu'
import C from '../../constants'

describe("DisplayOptions", () => {
    it("check options", () => {
        let selectOption = jest.fn()
        let txt = toJSON(
                      shallow(<DisplayOptions selectOption={selectOption}/>)
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("OptionsMenu", () => {
    it("show menu", () => {
        let interaction = C.DOCUMENT_VIEWER
        let option = C.DOC_VIEWER_OPTIONS.DEFAULT
        let selectOption = jest.fn()
        let txt = toJSON(
                      shallow(<OptionsMenu interaction={interaction}
                                           option={option}
                                           selectOption={selectOption}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("hide menu", () => {
        let interaction = C.DOCUMENT_SELECTOR
        let option = C.DOC_VIEWER_OPTIONS.DEFAULT
        let selectOption = jest.fn()
        let txt = toJSON(
                      shallow(<OptionsMenu interaction={interaction}
                                           option={option}
                                           selectOption={selectOption}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })
})