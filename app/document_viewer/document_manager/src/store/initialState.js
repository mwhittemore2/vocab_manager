import C from '../constants'

export const initStateData = {
    documents: [],
    interaction: C.DOCUMENT_SELECTOR,
    lines: {
        currPage: 1,
        selected: new Set([]),
        words: []
    },
    loaded: {"DOCUMENT_SELECTOR": false, "TRANSLATION_VIEWER": false},
    option: C.DOC_VIEWER_OPTIONS.DEFAULT,
    pages: {
        content: [],
        currDoc: {},
        startPage: 0,
        endPage: 0
    },
    translations: {
        boundary: {
            buffer: [],
            currState: "",
            start: {}
        },
        currPage: 1,
        matches: [],
        searchPhrase: []
    }

}