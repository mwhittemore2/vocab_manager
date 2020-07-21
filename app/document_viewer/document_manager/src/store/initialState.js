import C from '../constants'

const getDefaultLoadStatus = () => {
    let loadStatus = {}
    loadStatus[C.DOCUMENT_SELECTOR] = false
    loadStatus[C.TRANSLATION_VIEWER] = false
    return loadStatus
}

export const initStateData = {
    documents: [],
    interaction: C.DOCUMENT_SELECTOR,
    lines: {
        currPage: 1,
        selected: new Set([]),
        words: []
    },
    loaded: getDefaultLoadStatus(),
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