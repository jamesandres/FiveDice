React = require('react');

var render = function(state) {
    if (!state) {
        return <h1>:-(</h1>
    }

    if (!state.direction) {
        return <h1>{state.msg}</h1>
    } else {
        var style = {"direction": state.direction};
        return <h1 style={style}>{state.msg}</h1>
    }
};

module.exports = {
  render: render
};