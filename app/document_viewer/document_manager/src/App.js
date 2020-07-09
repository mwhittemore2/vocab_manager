import { 
    DocumentDisplay, DocumentSelection, Options, 
    TranslationCandidate, TranslationDisplay
} from './components/containers'

const App = () =>
    <div className="app">
        <DocumentSelection />
        <TranslationCandidate />
        <DocumentDisplay />
        <Options />
        <TranslationDisplay />
    </div>

export default App