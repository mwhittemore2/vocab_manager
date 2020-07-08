import React from "react"
import { Provider } from "react-redux"
import { Options } from '../../../components/containers'
import { mount } from "enzyme"
import C from '../../../constants'

jest.mock('../../../components/ui/OptionsMenu')

describe("Options container", () => {
    let wrapper
    const store = {
        dispatch: jest.fn(),
        subscribe: jest.fn(),
        getState: jest.fn(() => 
            ({
                interaction: C.DOCUMENT_VIEWER,
                option: C.DOC_VIEWER_OPTIONS.DEFAULT
            })
        )
    }

    beforeAll(() => wrapper = mount (
        <Provider store={store}>
            <Options/>
        </Provider>        
    ))

    afterEach(() => jest.resetAllMocks())

    it("check current option", () => {
        expect(wrapper
               .find('OptionsMenuMock')
               .props()
               .option
        ).toBe(C.DOC_VIEWER_OPTIONS.DEFAULT)
    })

    it("correct interaction", () => {
        expect(wrapper
               .find('OptionsMenuMock')
               .props()
               .interaction
        ).toBe(C.DOCUMENT_VIEWER)
    })

    it("set option", () => {
        wrapper
        .find('OptionsMenuMock')
        .props()
        .selectOption(C.DOC_VIEWER_OPTIONS.ADD_VOCAB)

        expect(store.dispatch).toBeCalled()
    })
})