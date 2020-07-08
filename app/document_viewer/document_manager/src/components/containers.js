import { connect } from 'react-redux'
import DocumentViewer from './ui/DocumentViewer'
import DocumentSelector from './ui/DocumentSelector'
import OptionsMenu from './ui/OptionsMenu'
import TranslationQueue from './ui/TranslationQueue'
import TranslationViewer from './ui/TranslationViewer'
import * as actions from '../actions'
import C from '../constants'

export const DocumentDisplay = connect(
    state => 
        ({
            interaction: state.interaction,
            lines: state.lines
        }),
    dispatch =>
        ({
            cursor(direction, pageNumber){
                dispatch(actions.navigate(direction, pageNumber, getPage))
            },
            selectWord(word){
                dispatch(actions.registerSelectedWord(word))
            }
        })
)(DocumentViewer);

export const DocumentSelection = connect(
    state =>
        ({
            documents: state.documents,
            interaction: state.interaction,
            loaded: state.loaded
        }),
    dispatch =>
        ({
            getDocuments(){
                dispatch(actions.listDocuments());
            },
            selectDocument(doc){
                dispatch(actions.setCurrentDocument(doc));
            }
        })
)(DocumentSelector);


export const Options = connect(
    state =>
        ({
            interaction: state.interaction,
            option: state.option
        }),
    dispatch => 
        ({
             selectOption(option){
                 dispatch(actions.setOption(option))
             }
        })
)(OptionsMenu)


export const TranslationCandidate = connect(
    state => 
        ({
            interaction: state.interaction,
            translations: state.translations
        }),
    dispatch => 
        ({
            remove(position){
                dispatch(actions.deleteFromTranslationQueue(position))
            }
        })
)(TranslationQueue)


export const TranslationDisplay = connect(
    state => 
        ({
            interaction: state.interaction,
            option: state.option,
            translations: state.translations
        }),
    dispatch =>
        ({
            closeViewer(){
                dispatch(actions.setOption(C.DOC_VIEWER_OPTIONS.DEFAULT))
            },
            cursor(direction, pageNumber){
                dispatch(actions.navigate(direction, pageNumber, getTranslation))
            }
        })
)(TranslationViewer)