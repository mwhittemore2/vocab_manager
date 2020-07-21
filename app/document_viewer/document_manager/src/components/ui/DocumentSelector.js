import PropTypes from 'prop-types'
import React from "react"
import C from '../../constants'
import { Loading } from './Loading'

const buildKey = (doc, index) => {
    let domain = "docChoice"
    let separator = "-"
    let key = domain + separator + index.toString() + separator + doc
    return key
}

export const DocumentChoice = ({doc, selector}) =>
    <div onClick={() => selector(doc)}>
        {doc.title}
    </div>

export const DocumentIterator = ({documents, selectDocument}) =>
    <div id="document-selector">
        {documents.sort((a, b) => (a.title > b.title) ? 1 : -1).map((doc, index) =>
            <DocumentChoice key={buildKey(doc.title, index)}
                            doc={doc}
                            selector={selectDocument}/>
        )}
    </div>

 export class DocumentSelector extends React.Component {
    render(){
        let documents = this.props.documents
        let getDocuments = this.props.getDocuments
        let interaction = this.props.interaction
        let loaded = this.props.loaded[C.DOCUMENT_SELECTOR]
        let selectDocument = this.props.selectDocument
        if (interaction === C.DOCUMENT_SELECTOR){
            if (loaded){
                return (
                    <DocumentIterator documents={documents}
                                      selectDocument={selectDocument}/>
                )
            }
            else{
                if (documents.length <= 0){
                    getDocuments()
                }
                return (
                    <Loading />
                )
            }
        }
        return (
            <div id={"document-selector"}/>
        )
    }
}

DocumentChoice.propTypes = {
    doc: PropTypes.object,
    selector: PropTypes.func
}

DocumentIterator.propTypes = {
    documents: PropTypes.array,
    selectDocument: PropTypes.func
}

DocumentSelector.propTypes = {
    documents: PropTypes.array,
    getDocuments: PropTypes.func,
    interaction: PropTypes.string,
    loaded: PropTypes.object,
    selectDocument: PropTypes.func
}

DocumentSelector.defaultProps = {
    documents: [],
    getDocuments: f=>f,
    interaction: C.DOCUMENT_SELECTOR,
    loaded: {},
    selectDocument: f=>f
}

export default DocumentSelector