React = require('react');

module.exports = {
    // See: http://facebook.github.io/react/docs/tutorial.html
    render: function(state) {
        if (!state) {
            return <h1 className="hello">:-(</h1>
        }

        if (!state.direction) {
            return <h1 className="hello">{state.msg}</h1>
        } else {
            var style = {"direction": state.direction};
            return <h1 className="hello" style={style}>{state.msg}</h1>
        }
    }
};