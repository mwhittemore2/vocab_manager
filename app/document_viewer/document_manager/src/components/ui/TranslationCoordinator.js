import PropTypes from "prop-types"
import React from "react"
import C from "../../constants"
import grammar from "../../data/grammar"

const coordinatorID = "translation-coordinator"

const endpointManagerID = "translation-coordinator-endpoint-manager"

const textManagerID = "translation-coordinator-text-manager"

export const EndpointManager = ({setEndpoint, translations}) => {

}

export const QueueManager = ({clearQueue}) => {

}

export const TextManager = ({addText, translations}) => {

}

export class TranslationCoordinator extends React.Component{
    render(){
        let interaction = this.props.interaction
        if(interaction === C.DOCUMENT_VIEWER){
            let option = this.props.option
            if(option === C.DOC_VIEWER_OPTIONS.TRANSLATION_COORDINATOR){
                let addText = this.props.addText
                let clearQueue = this.props.clearQueue
                let setEndpoint = this.props.setEndpoint
                let translate = this.props.translate
                let translations = this.props.translations
                return(
                    <div id={coordinatorID}>
                        <TextManager addText={addText}
                                     translations={translations}/>
                        <EndpointManager setEndpoint={setEndpoint}
                                         translations={translations}/>
                        <QueueManager clearQueue={clearQueue}/>
                        <button onClick={translate()}>Get Translations</button>
                    </div>
                )
            }
        }
        return(
            <div id={coordinatorID}></div>
        )
    }
}