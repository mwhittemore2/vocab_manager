import { difference, union } from '../lib/setProcessing'
import C from '../constants'

export const documents = (state=[], action) => {
    switch (action.type){
        case C.LIST_DOCUMENTS:
            return action.documents

        default:
            return state
    }
}

export const interaction = (state="", action) => {
    switch (action.type){
        case C.SET_INTERACTION:
            return action.interaction_type
        
        default:
            return state

    }
}

export const lines = (state={}, action) => {
    switch (action.type){
        case C.HIGHLIGHT:
            let prevSelected = state.selected
            return {
                ...state,
                selected: union(prevSelected, action.selected) 
            }

        case C.SET_CURRENT_PAGE:
            return {
                ...state,
                ...action.newPage,
                currPage: action.pageNumber
            }
        
        case C.UNHIGHLIGHT:
            return {
                ...state,
                selected: difference(state.selected, action.selected)
            }

        default:
            return state
    }
}

export const loaded = (state={}, action) => {
    switch (action.type){
        case C.FINISHED_LOADING:
            let newState = {
                ...state,
            }
            newState[action.component] = true
            return newState
        
        default:
            return state
    }
}

export const option = (state="", action) => {
    switch (action.type){
        case C.SET_OPTION:
            return action.option
        
        default:
            return state
    }
}

export const pages = (state={}, action) => {
    switch (action.type){
        case C.SELECT_DOCUMENT:
            return {
                ...state,
                currDoc: action.document
            }

        case C.SET_PAGE_RANGE:
            return {
                ...state,
                content: action.content,
                startPage: action.start,
                endPage: action.end
            }
        
        default:
            return state
    }
}

export const translations = (state={}, action) => {
    switch (action.type){
        case C.APPEND_TRANSLATION_BUFFER:
            let bufferedBoundary = {
                ...state.boundary,
                buffer: action.buffer,
                start: action.start
            }
            return {
                ...state,
                boundary: bufferedBoundary
            }
        
        case C.APPEND_TRANSLATION_QUEUE:
            return {
                ...state,
                searchPhrase: state.searchPhrase.concat(action.words)
            }
        
        case C.DISPLAY_TRANSLATION:
            return {
                ...state,
                currPage: action.currPage,
                matches: action.matches
            }
        
        case C.FILTER_TRANSLATION_QUEUE:
            return {
                ...state,
                searchPhrase: action.searchPhrase
            }
        
        case C.SET_TEXT_BOUNDARY:
            let textBoundary = {
                ...state.boundary,
                currState: action.currState
            }
            return {
                ...state,
                boundary: textBoundary
            }
        
        case C.RESET_TRANSLATIONS:
            return {
                boundary: {
                    buffer: [],
                    currState: "",
                    start: {}
                },
                currPage: 1,
                matches: [],
                searchPhrase: []
            }

        default:
            return state
    }
}