import C from '../constants'

/**
 * Fetches the headers to be used in an API request.
 * 
 * @return {object} The request headers.
 */
export const getHeaders = () => {
    let headerString = localStorage[C.SERVICES.HEADERS]
    if(! headerString){
        let emptyHeaders = {}
        return emptyHeaders
    }
    let headers = JSON.parse(headerString)
    return headers
}

/**
 * Builds the final url for services which are language-dependent.
 * 
 * @param {string} language The language for the service to process. 
 * @param {string} service A template of the service to be called.
 * @return {string} The final url of the service to be called.
 */
export const setLanguage = (language, service) => {
    let toReplace = "LANGUAGE"
    let endpoint = service.replace(toReplace, language)
    return endpoint
}