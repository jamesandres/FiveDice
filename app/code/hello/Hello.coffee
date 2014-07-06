React = require 'react'
template = require './hello.jsx'


# HelloWidget renders a simple rotating greeting into a DOM element.
class HelloWidget
    MESSAGES: [
        {"msg": "Hello!"},
        {"msg": "Bonjour!"},
        {"msg": "¡Hola!"},
        {"msg": "مرحبا!", "direction": "rtl"},
        {"msg": "Добры дзень!"},
        {"msg": "হ্যালো!"},
        {"msg": "Здравейте!"},
        {"msg": "您好！"},
        {"msg": "Pozdrav!"},
        {"msg": "Dobrý den!"},
        {"msg": "Hej!"},
        {"msg": "Hujambo!"},
        {"msg": "Здравствуйте!"},
        {"msg": "こんにちは！"},
        {"msg": "안녕하세요!"},
        {"msg": "Olá!"},
    ]

    constructor: (options) ->
        @el = options.el
        @speed = options.speed or 2000

    # Render, render, render
    render: ->
        component = template.render(@state)
        React.renderComponent(component, @el)

    run: =>
        @_updateState()
        @render()
        @timer = setTimeout(@run, @speed)

    stop: ->
        clearTimeout(@timer)
        @timer = null

    _updateState: ->
        @state = @MESSAGES[Math.floor(Math.random() * @MESSAGES.length)]


module.exports =
    create: (options) -> new HelloWidget(options)
