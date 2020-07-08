import React from "react"
import { shallow } from "enzyme"
import toJSON from 'enzyme-to-json'
import { BaseFormMatch, Definitions, DerivedFormMatch,
         TranslationViewer, ViewMatches } from '../../components/ui/TranslationViewer'
import C from '../../constants'

describe("Definitions", () => {
    it("single definition", () => {
        let match = {
                definitions: ["book"]
            }
        let page = 1
        let txt = toJSON(
                      shallow(<Definitions match={match}
                                           page={page}/>)
                  )
        expect(txt).toMatchSnapshot()
    })

    it("multiple definitions", () => {
        let match = {
                definitions: ["book", "novel", "writing"]
            }
        let page = 1
        let txt = toJSON(
                      shallow(<Definitions match={match}
                                           page={page}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("next page", () => {
        let match = {
                definitions: ["lamp", "light"]
            }
        let page = 2
        let txt = toJSON(
                      shallow(<Definitions match={match}
                                           page={page}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("BaseFormMatch", () => {
    it("single definition", () => {
        let match = {
                text: "Welt",
                pos: "Noun",
                definitions: ["world"]
            }
        let page = 1
        let txt = toJSON(
                      shallow(<BaseFormMatch match={match}
                                             page={page}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("multiple definitions", () => {
        let match = {
                text: "Welt",
                pos: "Noun",
                definitions: ["world", "earth"]
            }
        let page = 1
        let txt = toJSON(
                      shallow(<BaseFormMatch match={match}
                                             page={page}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("DerivedFormMatch", () => {
    it("single definition", () => {
        let match = {
                text: "Welten",
                definitions: ["worlds"],
                see_also:{
                    text: "Welt",
                    pos: "Noun"
                }
            }
        let page = 1
        let txt = toJSON(
                      shallow(<DerivedFormMatch match={match}
                                                page={page}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("multiple definitions", () => {
        let match = {
                text: "Welten",
                definitions: ["worlds", "earths"],
                see_also: {
                    text: "Welt",
                    pos: "Noun"
                }
            }
        let page = 1
        let txt = toJSON(
                      shallow(<DerivedFormMatch match={match}
                                                page={page}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("ViewMatches", () => {
    it("single match", () => {
        let translations = {
                currPage: 1,
                matches: [
                    {
                        text: "Welt",
                        pos: "Noun",
                        definitions: ["world", "earth"]
                    }
                ]
            }
        let txt = toJSON(
                      shallow(<ViewMatches translations={translations}/>)
                  )
        expect(txt).toMatchSnapshot()
    })

    it("multiple matches", () => {
        let translations = {
            currPage: 1,
            matches: [
                {
                    text: "Welt",
                    pos: "Noun",
                    definitions: ["world", "earth"]
                },
                {
                    text: "Welten",
                    definitions: ["worlds", "earths"],
                    see_also: {
                        text: "Welt",
                        pos: "Noun"
                    }
                }
            ]
        }
        let txt = toJSON(
                      shallow(<ViewMatches translations={translations}/>)
                  )
        expect(txt).toMatchSnapshot()
    })
})

describe("TranslationViewer" , () => {
    let closeViewer
    let cursor
    let translations
    beforeEach(() => {
        closeViewer = jest.fn()
        cursor = jest.fn()
        translations = {
            currPage: 1,
            matches: [
                {
                    text: "Welt",
                    pos: "Noun",
                    definitions: ["world", "earth"]
                }
            ]
        }
    })

    afterAll(() => {
        jest.resetAllMocks()
    })

    it("view translations", () => {
        let interaction = C.DOCUMENT_VIEWER
        let option = C.TRANSLATION_VIEWER
        let loaded = {}
        loaded[C.TRANSLATION_VIEWER] = true
        let txt = toJSON(
                      shallow(<TranslationViewer closeViewer={closeViewer}
                                                 cursor={cursor}
                                                 interaction={interaction}
                                                 loaded={loaded}
                                                 option={option}
                                                 translations={translations}/>
                      )
                  )
        expect(txt).toMatchSnapshot()
    })

    it("loading", () => {
        let interaction = C.DOCUMENT_VIEWER
        let option = C.TRANSLATION_VIEWER
        let loaded = {}
        loaded[C.TRANSLATION_VIEWER] = false
        let txt = toJSON(
                      shallow(<TranslationViewer closeViewer={closeViewer}
                                                 cursor={cursor}
                                                 interaction={interaction}
                                                 loaded={loaded}
                                                 option={option}
                                                 translations={translations}/>
                      )  
                  )
        expect(txt).toMatchSnapshot()
    })

    it("not in document viewer", () =>{
        let interaction = C.DOCUMENT_SELECTOR
        let option = C.TRANSLATION_VIEWER
        let loaded = {}
        loaded[C.TRANSLATION_VIEWER] = true
        let txt = toJSON(
                      shallow(<TranslationViewer closeViewer={closeViewer}
                                                 cursor={cursor}
                                                 interaction={interaction}
                                                 loaded={loaded}
                                                 option={option}
                                                 translations={translations}/>
                      ).html()    
                  )
        expect(txt).toMatchSnapshot()
    })
})

