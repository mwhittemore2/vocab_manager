import React from "react"

/**
 * Renders a loading message for any component that
 * is experiencing high network latency.
 */
export class Loading extends React.Component {
    render(){
        return (
            <b>Loading...</b>
        )
    }
}