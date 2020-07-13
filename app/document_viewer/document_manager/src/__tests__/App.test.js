import App from '../App'

jest.mock('../components/containers')

describe("App", () => {
    it("correct rendering", () => {
        let numChildren = App().props.children.length
        expect(numChildren).toBe(6)
    })
})