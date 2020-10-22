import React from 'react';
import ReactMarkdown from 'react-markdown';

export default class ManualPageContent extends React.Component {
    constructor(props) {
        super(props)
        this.state = { source: null }
    }

    componentWillMount() {
        fetch(this.props.path).then(res => res.text()).then(src => {
            this.setState({ source: src})
        });
    }

    render() {
        return (
            <ReactMarkdown source={this.state.source}></ReactMarkdown>
        )
    }
}