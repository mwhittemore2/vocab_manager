import C from '../../../constants'
import { storeFactory } from '../../../store'
import { initStateData } from '../../../store/initialState'


describe("Initialize store", () => {

    it("Store not empty" , () => {
        let store = storeFactory(initStateData)
        let is_empty = true
        if (Object.keys(store).length > 0){
            is_empty = false
        }
        expect(is_empty).toEqual(false)
    })
    
    
    it("Uploads correct state", () => {
        let store = storeFactory(initStateData)
        let currState = store.getState()
        expect(currState).toEqual(initStateData)
    })

})

describe("Update store", () => {

    let store
    let msg
    let viewer
    beforeEach(() => {
        viewer = "viewer"
        msg = {
            type: C.SET_INTERACTION,
            interaction_type: viewer
        }
         store = storeFactory(initStateData)
    })

    it("Updated state", () => {
        store.dispatch(msg)
        let currState = store.getState()
        expect(currState.interaction).toEqual(viewer)

    })

    it("Updated localStorage", () => {
        store.dispatch(msg)
        let currState = store.getState()
        let backup = JSON.parse(localStorage['redux-store'])
        expect(backup).toEqual(currState)
    })
})