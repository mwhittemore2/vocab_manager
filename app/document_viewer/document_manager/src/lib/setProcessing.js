export const difference = (a,b) => {
    let d = new Set([...a].filter(x => !b.has(x)))
    return d
}

//Use axiom of extensionality to test for equality
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

export const union = (a,b) => {
    let uList = [...a].concat([...b])
    let u = new Set(uList)
    return u
}