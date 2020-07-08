import C from '../../../constants'
import { interaction } from '../../../store/reducers'

describe("interaction Reducer", () => {

    it("use selector", () => {
        const selector = "selector"
        const state = ""
        const action = {
            type: C.SET_INTERACTION,
            interaction_type: selector
        }
        const result = interaction(state, action)
        expect(result).toEqual(selector)
    })

    it("use viewer", () => {
        const viewer = "viewer"
        const state = ""
        const action = {
            type: C.SET_INTERACTION,
            interaction_type: viewer
        }
        const result = interaction(state, action)
        expect(result).toEqual(viewer)
    })
})