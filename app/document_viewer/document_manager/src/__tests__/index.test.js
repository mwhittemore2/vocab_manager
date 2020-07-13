import { render } from 'react-dom'

jest.mock('react-dom')
jest.mock('../store/index', () => () => ({
    subscribe: jest.fn(),
    dispatch: jest.fn(),
    getState: jest.fn()
}))

describe("go to app home page", () => {
    it("render app", () => {
        require("../index.js")
    })
})