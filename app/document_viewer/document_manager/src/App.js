import React from "react"
import { 
    DocumentDisplay, DocumentSelection, Options, 
    TranslationCandidate, TranslationCoordination,
    TranslationDisplay
} from './components/containers'

/**
 * Organizes the components of the application under
 * a single div.
 */
const App = () =>
    <div className="app">
        <DocumentSelection />
        <TranslationCandidate />
        <DocumentDisplay />
        <Options />
        <TranslationCoordination />
        <TranslationDisplay />
    </div>

export default App