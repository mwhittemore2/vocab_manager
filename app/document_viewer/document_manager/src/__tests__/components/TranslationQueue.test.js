import React from "react"
import { shallow } from "enzyme"
import toJSON from 'enzyme-to-json'
import { QueueElement, TranslationQueue } from '../../components/ui/TranslationQueue'
import C from '../../constants'

describe("QueueElement", ()=>{
    let position
    let remove
    beforeEach(()=> {
        position = 3
        remove = jest.fn()
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("single word", () => {
        let word = "Buch"
        let txt = toJSON(
                      shallow(<QueueElement position={position}
                                            remove={remove}
                                            text={word}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("multiple words", () => {
        let words = "das Buch"
        let txt = toJSON(
                      shallow(<QueueElement position={position}
                                            remove={remove}
                                            text={words}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("remove word", () =>{
        let word = "Buch"
        shallow(<QueueElement position={position}
                              remove={remove}
                              text={word}/>
        )
        .find('span')
        .simulate('click')
        expect(remove).toBeCalled()
    })
})

describe("TranslationQueue", () => {

    it("populated queue", () => {
        let interaction = C.DOCUMENT_VIEWER
        let translations = {
                searchPhrase: [
                    {fulltext: "Die "}, 
                    {fulltext: "Welt "}, 
                    {fulltext: "ist "}, 
                    {fulltext: "meine "}, 
                    {fulltext: "Vorstellung"}
                ]
            }
        let remove = jest.fn()
        let txt = toJSON(
                      shallow(<TranslationQueue interaction={interaction}
                                                remove={remove}
                                                translations={translations}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("empty queue", () => {
        let interaction = C.DOCUMENT_VIEWER
        let translations = {
            searchPhrase: []
        }
        let remove = jest.fn()
        let txt = toJSON(
                      shallow(<TranslationQueue interaction={interaction}
                                                remove={remove}
                                                translations={translations}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("not in document viewer", () => {
        let interaction = C.DOCUMENT_SELECTOR
        let translations = {
            searchPhrase: []
        }
        let remove = jest.fn()
        let txt = toJSON(
                      shallow(<TranslationQueue interaction={interaction}
                                                remove={remove}
                                                translations={translations}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })
})