import React from "react"
import { Provider } from "react-redux"
import { TranslationCandidate } from '../../../components/containers'
import { mount } from "enzyme"
import C from '../../../constants'

jest.mock('../../../components/ui/TranslationQueue')

describe("TranslationCandidate container", () => {
    let wrapper
    let searchPhraseData = ["das ", "Buch"]
    const store = {
        dispatch: jest.fn(),
        subscribe: jest.fn(),
        getState: jest.fn(() => 
            ({
                interaction: C.DOCUMENT_VIEWER,
                translations: {
                    searchPhrase: searchPhraseData
                }
            })
        )
    }

    beforeAll(() => wrapper = mount (
        <Provider store={store}>
            <TranslationCandidate/>
        </Provider>        
    ))

    afterEach(() => jest.resetAllMocks())

    it("check queue", () => {
        expect(wrapper
               .find('TranslationQueueMock')
               .props()
               .translations
               .searchPhrase
        ).toStrictEqual(searchPhraseData)
    })

    it("correct interaction", () => {
        expect(wrapper
               .find('TranslationQueueMock')
               .props()
               .interaction
        ).toBe(C.DOCUMENT_VIEWER)
    })

    it("remove element from queue", () => {
        wrapper
        .find('TranslationQueueMock')
        .props()
        .remove(0)

        expect(store.dispatch).toBeCalled()
    })
})