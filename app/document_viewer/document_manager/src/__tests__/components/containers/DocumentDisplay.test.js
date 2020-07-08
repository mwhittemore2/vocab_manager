import React from "react"
import { Provider } from "react-redux"
import { DocumentDisplay } from '../../../components/containers'
import { mount } from "enzyme"
import C from '../../../constants'

jest.mock('../../../components/ui/DocumentViewer')

describe("DocumentDisplay container", () => {
    let wrapper
    let linesData = {
        words: [
            ["das ", "Buch"]
        ]
    }
    const store = {
        dispatch: jest.fn(),
        subscribe: jest.fn(),
        getState: jest.fn(() => 
            ({
                interaction: C.DOCUMENT_VIEWER,
                lines: linesData
            })
        )
    }

    beforeAll(() => wrapper = mount (
        <Provider store={store}>
            <DocumentDisplay/>
        </Provider>        
    ))

    afterEach(() => jest.resetAllMocks())

    it("check lines", () => {
        expect(wrapper
               .find('DocumentViewerMock')
               .props()
               .lines
        ).toStrictEqual(linesData)
    })

    it("correct interaction", () => {
        expect(wrapper
               .find('DocumentViewerMock')
               .props()
               .interaction
        ).toBe(C.DOCUMENT_VIEWER)
    })

    it("select word", () => {
        wrapper
        .find('DocumentViewerMock')
        .props()
        .selectWord()
        expect(store.dispatch).toBeCalled()
    })
})