/**
 * Subtracts the second set from the first.
 * 
 * @param {Set} a First set. 
 * @param {Set} b Second set.
 * @return {Set} The set-theoretic difference.
 */
export const difference = (a,b) => {
    let d = new Set([...a].filter(x => !b.has(x)))
    return d
}

/** 
 * Determines if two sets are equal by using the axiom of 
 * extensionality.
 * 
 * @param {Set} a First set.
 * @param {Set} b Second set.
 * @return {bool} True if the sets are equal, False otherwise.
 */
export const equals = (a,b) => {
    let leftToRight = isSubsetOf(a,b)
    let rightToLeft = isSubsetOf(b,a)
    let decision
    if(leftToRight & rightToLeft){
        decision = true
    }
    else{
        decision = false
    }
    return decision
}

/**
 * Determines if the the first set is a subset of the second 
 * one.
 * 
 * @param {Set} a First set.
 * @param {Set} b Second set.
 * @return {bool} True if the first set is a subset of the second 
 *                one, False otherwise.
 */
export const isSubsetOf = (a,b) => {
    let decision = true
    for (let element of a){
        if(!(b.has(element))){
            decision = false
            return decision
        }
    }
    return decision
}

/**
 * Joins the first set with the second.
 * 
 * @param {Set} a First set.
 * @param {Set} b Second set.
 * @return {Set} The set-theoretic union. 
 */
export const union = (a,b) => {
    let uList = [...a].concat([...b])
    let u = new Set(uList)
    return u
}