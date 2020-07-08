import React from "react"
import { Provider } from "react-redux"
import { TranslationDisplay } from '../../../components/containers'
import { mount } from "enzyme"
import C from '../../../constants'

jest.mock('../../../components/ui/TranslationViewer')

describe("TranslationDisplay container", () => {
    let wrapper
    let matchesData = [{
        text: "Welt",
        definitions: ["World"]
    }]
    const store = {
        dispatch: jest.fn(),
        subscribe: jest.fn(),
        getState: jest.fn(() => 
            ({
                interaction: C.DOCUMENT_VIEWER,
                option: C.TRANSLATION_VIEWER,
                translations: {
                    matches: matchesData
                }
            })
        )
    }

    beforeAll(() => wrapper = mount (
        <Provider store={store}>
            <TranslationDisplay/>
        </Provider>        
    ))

    afterEach(() => jest.resetAllMocks())

    it("close viewer", () => {
        wrapper
        .find('TranslationViewerMock')
        .props()
        .closeViewer()

        expect(store.dispatch).toBeCalled()
    })

    it("correct interaction", () => {
        expect(wrapper
               .find('TranslationViewerMock')
               .props()
               .interaction
        ).toBe(C.DOCUMENT_VIEWER)
    })

    it("correct option", () => {
        expect(wrapper
               .find('TranslationViewerMock')
               .props()
               .option
        ).toBe(C.TRANSLATION_VIEWER)
    })

    it("check matches", () => {
        expect(wrapper
               .find('TranslationViewerMock')
               .props()
               .translations
               .matches
        ).toStrictEqual(matchesData)
    })
})