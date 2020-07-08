import React from "react"
import { shallow } from "enzyme"
import toJSON from 'enzyme-to-json'
import { compose } from 'redux'
import { DocumentChoice, DocumentIterator, DocumentSelector } from '../../components/ui/DocumentSelector'
import C from '../../constants'

describe("Document Choice", () => {
    let doc
    let key
    let selector

    beforeEach(() => {
        doc = {title: "Die Welt", author: "Schopenhauer"}
        key = "testKey"
        selector = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("display document", () => {
        let docText = shallow(<DocumentChoice doc={doc} identifier={key} selector={selector}/>)
                      .find('div')
                      .text()
        expect(docText).toBe(doc.title)
    })

    it("call selector", () => {
        shallow(<DocumentChoice doc={doc} identifier={key} selector={selector}/>)
        .find('div')
        .simulate('click')
        expect(selector).toBeCalled()
    })

    it("check selected document", () => {
        shallow(<DocumentChoice doc={doc} identifier={key} selector={selector}/>)
        .find('div')
        .simulate('click')
        expect(selector).toBeCalledWith(doc)
    })
})

describe("Document Iterator", () => {
    let docs
    let selector

    beforeEach(() => {
        docs = [
            {title: "Die Welt", author: "Schopenhauer"},
            {title: "Kritik", author: "Kant"}
        ]
        selector = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("no docs", () =>{
        let noDocs = []
        let docSet = toJSON(
                         shallow(<DocumentIterator documents={noDocs} selectDocument={selector}/>)
                         .find('div')
                     )
        expect(docSet).toMatchSnapshot()
    })

    it("single doc", () => {
        let singleDoc = [docs[0]]
        let docSet = toJSON(
                         shallow(<DocumentIterator documents={singleDoc} selectDocument={selector}/>)
                         .find('div')
                     )
        expect(docSet).toMatchSnapshot()            
    })

    it("multiple docs", () => {
        let docSet = toJSON(
                         shallow(<DocumentIterator documents={docs} selectDocument={selector}/>)
                         .find('div')
                     )    
        expect(docSet).toMatchSnapshot()
    }) 
})

describe("Document Selector", () => {
    let docs
    let getDocuments
    let interaction
    let selector

    beforeEach(() => {
        docs = [
            {title: "Die Welt", author: "Schopenhauer"},
            {title: "Kritik", author: "Kant"}
        ]
        getDocuments = jest.fn()
        interaction = C.DOCUMENT_SELECTOR
        selector = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("populate selector", () => {
        let loaded = {}
        loaded[C.DOCUMENT_SELECTOR] = true
        let docSet = toJSON(
                         shallow(<DocumentSelector documents={docs} 
                                                   interaction={interaction}
                                                   loaded={loaded}
                                                   selectDocument={selector}/>
                        )
                     )
        expect(docSet).toMatchSnapshot()
    })

    it("dispaly loading message", () => {
        let loaded = {}
        loaded[C.DOCUMENT_SELECTOR] = false
        let noDocs = []
        let docSet = toJSON(
                         shallow(<DocumentSelector documents={noDocs}
                                                   getDocuments={getDocuments}
                                                   interaction={interaction}
                                                   loaded={loaded}/>
                        )
                     )
        expect(docSet).toMatchSnapshot()
    })

    it("download documents", ()=> {
        let loaded = {}
        loaded[C.DOCUMENT_SELECTOR] = false
        let noDocs = []
        shallow(<DocumentSelector documents={noDocs}
                                  getDocuments={getDocuments}
                                  interaction={interaction}
                                  loaded={loaded}/>
        )
        expect(getDocuments).toBeCalled()
    })


})