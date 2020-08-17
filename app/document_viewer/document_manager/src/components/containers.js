import { connect } from 'react-redux'
import DocumentViewer from './ui/DocumentViewer'
import DocumentSelector from './ui/DocumentSelector'
import OptionsMenu from './ui/OptionsMenu'
import TranslationCoordinator from './ui/TranslationCoordinator'
import TranslationQueue from './ui/TranslationQueue'
import TranslationViewer from './ui/TranslationViewer'
import * as actions from '../actions'
import C from '../constants'

/**
 * Display's a user's document in the browser.
 */
export const DocumentDisplay = connect(
    state => 
        ({
            interaction: state.interaction,
            lines: state.lines
        }),
    dispatch =>
        ({
            cursor: (direction, pageNumber) => {
                dispatch(actions.navigate(direction, pageNumber, actions.getPages))
            },
            jumpToPage: (e) => {
                dispatch(actions.jumpToPage(e, actions.getPages))
            },
            selectWord: (word) => {
                dispatch(actions.registerSelectedWord(word))
            }
        })
)(DocumentViewer);

/**
 * Presents the user with documents to read.
 */
export const DocumentSelection = connect(
    state =>
        ({
            documents: state.documents,
            interaction: state.interaction,
            loaded: state.loaded
        }),
    dispatch =>
        ({
            getDocuments: () => {
                dispatch(actions.listDocuments());
            },
            selectDocument: (doc) => {
                dispatch(actions.setCurrentDocument(doc));
            }
        })
)(DocumentSelector);

/**
 * Presents the user with options for interacting with
 * the current document.
 */
export const Options = connect(
    state =>
        ({
            interaction: state.interaction,
            option: state.option
        }),
    dispatch => 
        ({
             selectOption: (option) => {
                 dispatch(actions.setOption(option))
             }
        })
)(OptionsMenu);

/**
 * Displays the text of the user's query to be translated.
 */
export const TranslationCandidate = connect(
    state => 
        ({
            interaction: state.interaction,
            translations: state.translations
        }),
    dispatch => 
        ({
            remove: (position) => {
                dispatch(actions.deleteFromTranslationQueue(position))
            }
        })
)(TranslationQueue);

/**
 * Provides tools for building a phrase to be translated.
 */
export const TranslationCoordination = connect(
    state =>
        ({
            interaction: state.interaction,
            option: state.option,
            translations: state.translations
        }),
    dispatch =>
        ({
            addText: (txt) => {
                let textToAdd = {
                    text: txt
                }
                dispatch(actions.registerSelectedWord(textToAdd))
            },
            clearQueue: () => {
                dispatch(actions.clearTranslationQueue())
            },
            
            closeViewer: () => {
                dispatch(actions.setOption(C.DOC_VIEWER_OPTIONS.DEFAULT))
                dispatch(actions.resetTranslations())
            },
            setEndpoint: (endpoint) => {
                dispatch(actions.setTextBoundary(endpoint))
            },
            translate: () => {
                dispatch(actions.navigate(C.NEXT_PAGE, 0, actions.getTranslations))
                dispatch(actions.setOption(C.TRANSLATION_VIEWER))
            }
        })
)(TranslationCoordinator);

/**
 * Displays the translations of the user's query.
 */
export const TranslationDisplay = connect(
    state => 
        ({
            interaction: state.interaction,
            loaded: state.loaded,
            option: state.option,
            translations: state.translations
        }),
    dispatch =>
        ({
            closeViewer: () => {
                dispatch(actions.setOption(C.DOC_VIEWER_OPTIONS.DEFAULT))
                dispatch(actions.resetTranslations())
            },
            cursor: (direction, pageNumber) => {
                dispatch(actions.navigate(direction, pageNumber, actions.getTranslations))
            },
            jumpToPage: (e) => {
                dispatch(actions.jumpToPage(e, actions.getTranslations))
            }
        })
)(TranslationViewer);