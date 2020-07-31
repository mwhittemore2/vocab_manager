import C from '../constants'

export const getHeaders = () => {
    let headerString = localStorage[C.SERVICES.HEADERS]
    let headers = JSON.parse(headerString)
    return headers
}

export const setLanguage = (language, service) => {
    let toReplace = "LANGUAGE"
    let endpoint = service.replace(toReplace, language)
    return endpoint
}