HelloWidget = require './hello/Hello'

document.addEventListener('DOMContentLoaded', ->
    hello = HelloWidget.create({"el": document.getElementById("hello")})
    hello.run()

    # Debugging and tinkering interface
    window.hello = hello
)
