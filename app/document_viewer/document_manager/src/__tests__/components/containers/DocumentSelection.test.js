import React from "react"
import { Provider } from "react-redux"
import { DocumentSelection } from '../../../components/containers'
import { mount } from "enzyme"
import C from '../../../constants'

jest.mock('../../../components/ui/DocumentSelector')

describe("DocumentSelection container", () => {
    let wrapper
    let loadStatus = {}
    loadStatus[C.DOCUMENT_SELECTOR] = true
    const store = {
        dispatch: jest.fn(),
        subscribe: jest.fn(),
        getState: jest.fn(() => 
            ({
                documents: [],
                interaction: C.DOCUMENT_SELECTOR,
                loaded: loadStatus
            })
        )
    }

    beforeAll(() => wrapper = mount (
        <Provider store={store}>
            <DocumentSelection/>
        </Provider>        
    ))

    afterEach(() => jest.resetAllMocks())

    it("correct interaction", () => {
        expect(wrapper
               .find('DocumentSelectorMock')
               .props()
               .interaction
        ).toBe(C.DOCUMENT_SELECTOR)
    })

    it("documents loaded", () => {
        expect(wrapper
               .find('DocumentSelectorMock')
               .props()
               .loaded[C.DOCUMENT_SELECTOR]
        ).toBe(true)
    })

    it("download new documents", () =>{
        wrapper
        .find('DocumentSelectorMock')
        .props()
        .getDocuments()

        expect(store.dispatch).toBeCalled()
    })
})