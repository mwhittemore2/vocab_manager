import React from "react"
import { shallow } from "enzyme"
import toJSON from 'enzyme-to-json'
import { EndpointManager, Punctuation, QueueManager,
         Spacing, TextManager, TranslationCoordinator } from '../../components/ui/TranslationCoordinator'
import C from '../../constants'

describe("EndpointManager", () => {
    let setEndpoint
    beforeEach(() => {
        setEndpoint = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })
    
    it("check tags", () => {
        let txt = toJSON(
                      shallow(<EndpointManager setEndpoint={setEndpoint}/>)
                      .find('div')
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("QueueManager", () => {
    let clearQueue
    beforeEach(() => {
        clearQueue = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("check tags", () => {
        let txt = toJSON(
                      shallow(<QueueManager clearQueue={clearQueue}/>)
                      .find('div')
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("Punctuation", () => {
    let addText
    beforeEach(() => {
        addText = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("add comma button", () => {
        let punctuation = ","
        let txt = toJSON(
                      shallow(<Punctuation addText={addText} 
                                           punct={punctuation}/>
                      )
                      .find('button')
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("Spacing", () => {
    let addText
    beforeEach(() => {
        addText = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("add whitespace button", () => {
        let description = "whitespace"
        let spacing = ' '
        let txt = toJSON(
                      shallow(<Spacing addText={addText}
                                       description={description}
                                       spacing={spacing}/>
                      )
                      .find('button')
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("TextManager", () => {
    let addText
    beforeEach(() => {
        addText = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("check tags", () => {
        let txt = toJSON(
                      shallow(<TextManager addText={addText}/>)
                      .find('div')
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("TranslationCoordinator", () => {
    let addText
    let clearQueue
    let interaction
    let option
    let setEndpoint
    let translate
    beforeEach(() => {
        addText = jest.fn()
        clearQueue = jest.fn()
        interaction = C.DOCUMENT_VIEWER
        option = C.DOC_VIEWER_OPTIONS.TRANSLATION_COORDINATOR
        setEndpoint = jest.fn()
        translate = jest.fn()
    })
    it("check tags", () => {
        let txt = toJSON(
                      shallow(<TranslationCoordinator addText={addText}
                                                      clearQueue={clearQueue}
                                                      interaction={interaction}
                                                      option={option}
                                                      setEndpoint={setEndpoint}
                                                      translate={translate}/>
                      )
                      .find('div')
                  )
        expect(txt).toMatchSnapshot()
    })
})