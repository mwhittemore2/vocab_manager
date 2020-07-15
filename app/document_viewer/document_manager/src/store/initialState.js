import C from '../constants'

export const initStateData = {
    documents: [],
    interaction: "selector",
    lines: {
        currPage: 1,
        selected: new Set([]),
        words: []
    },
    loaded: {},
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