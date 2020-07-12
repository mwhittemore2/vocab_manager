import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import App from './App'
import { initStateData } from './store/initialState'
import { storeFactory } from './store'

const store = storeFactory(initStateData)

window.React = React
window.store = store

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('document-manager')
)