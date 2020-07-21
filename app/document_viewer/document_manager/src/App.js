import React from "react"
import { 
    DocumentDisplay, DocumentSelection, Options, 
    TranslationCandidate, TranslationCoordination,
    TranslationDisplay
} from './components/containers'

/*
const App = () =>
    <div className="app">
        <DocumentSelection />
        <TranslationCandidate />
        <DocumentDisplay />
        <Options />
        <TranslationCoordination />
        <TranslationDisplay />
    </div>*/

const App = () =>
    <div className="app">
        <DocumentSelection />
        <DocumentDisplay />
        <Options />
        <TranslationCoordination />
        <TranslationDisplay />
    </div>

export default App