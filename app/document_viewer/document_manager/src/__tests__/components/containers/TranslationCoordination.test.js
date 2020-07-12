import React from "react"
import { Provider } from "react-redux"
import { TranslationCoordination } from '../../../components/containers'
import { mount } from "enzyme"
import C from '../../../constants'

jest.mock('../../../components/ui/TranslationCoordinator')

describe("TranslationCoordination container", () => {
    let wrapper
    const store = {
        dispatch: jest.fn(),
        subscribe: jest.fn(),
        getState: jest.fn(() => 
            ({
                interaction: C.DOCUMENT_VIEWER,
                option: C.DOC_VIEWER_OPTIONS.TRANSLATION_COORDINATOR
            })
        )
    }

    beforeAll(() => wrapper = mount(
        <Provider store={store}>
            <TranslationCoordination/>
        </Provider>
    ))

    afterEach(() => jest.resetAllMocks())

    it("add text", () => {
        wrapper
        .find("TranslationCoordinatorMock")
        .props()
        .addText({text: "Buch"})

        expect(store.dispatch).toBeCalled()
    })

    it("correct interaction", () => {
        expect(wrapper
               .find('TranslationCoordinatorMock')
               .props()
               .interaction
        ).toBe(C.DOCUMENT_VIEWER)
    })

    it("correct option", () => {
        expect(wrapper
               .find('TranslationCoordinatorMock')
               .props()
               .option
        ).toBe(C.DOC_VIEWER_OPTIONS.TRANSLATION_COORDINATOR)
    })
})