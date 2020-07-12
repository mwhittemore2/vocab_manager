import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { documents, interaction, loaded, lines, option,
         pages, translations } from './reducers'
import { initStateData } from './initialState'

let console = window.console

const logger = store => next => action => {
    let result
    console.groupCollapsed("dispatching", action.type)
    console.log('Previous State', store.getState())
    console.log('Action', action)
    result = next(action)
    console.log('Next State', store.getState())
    console.groupEnd()
    return result
}

const saver = store => next => action => {
    let result = next(action)
    localStorage['redux-store'] = JSON.stringify(store.getState())
    return result
}

const middleware = [logger, saver, thunk]

///const reducers = [documents, interaction, lines, options, pages, translations]
const reducers = {documents, interaction, lines, loaded, option, pages, translations}

export const storeFactory = (initialState=initStateData) => 
    applyMiddleware(...middleware)(createStore)(
        combineReducers(reducers),
        (localStorage['redux-store']) ?
            JSON.parse(localStorage['redux-store']) :
            initialState
    )

