import PropTypes from 'prop-types'
import React from "react"
import stylesheet from './stylesheets/common'
import C from '../../constants'
import { Loading } from './Loading'

/**
 * Assigns a unique identifier to a document in a list.
 * 
 * @param {object} doc The document that needs a corresponding key.
 * @param {number} index The position of the document in a list.
 * @return {string} The document identifier.
 */
const buildKey = (doc, index) => {
    let domain = "docChoice"
    let separator = "-"
    let key = domain + separator + index.toString() + separator + doc
    return key
}

/**
 * Displays a document that the user can choose to read.
 * 
 * @param {object} doc A document that the user can select.
 * @param {func} selector Function for handling the selected document.
 * @return {html} The HTML representation of the document.
 */
export const DocumentChoice = ({doc, selector}) =>
    <div className={stylesheet.documentChoice}>
         <span onClick={() => selector(doc)}>{doc.title}</span>
    </div>

/**
 * Displays all documents that the user can choose from.
 * 
 * @param {array} documents The documents the user can choose from.
 * @param {func} selectDocument Function for handling the selected document.
 * @return {html} The HTML representation of the documents the user can choose from. 
 */
export const DocumentIterator = ({documents, selectDocument}) =>
    <div id="document-selector" className={stylesheet.displayDocumentSelector}>
        <b>Select a document to read</b>
        <br></br>
        <br></br>
        {documents.sort((a, b) => (a.title > b.title) ? 1 : -1).map((doc, index) =>
            <DocumentChoice key={buildKey(doc.title, index)}
                            doc={doc}
                            selector={selectDocument}/>
        )}
    </div>

/**
 * Renders a list of documents that the user can choose from.
 */
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