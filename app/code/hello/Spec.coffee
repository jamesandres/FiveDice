HelloWidget = require './Hello'
React = require('react/addons')
ReactTestUtils = React.addons.TestUtils

describe 'Hello', ->
    it 'Should have expected API', ->
        hello = HelloWidget.create({"el": null})

        expect(hello.run).toBeDefined();
        expect(hello.stop).toBeDefined();
        expect(hello.render).toBeDefined();


    it 'Should change message at intervals', ->
        node = document.createElement('DIV')
        hello = HelloWidget.create({"el": node})

        # This should all happen very fast ensuring that run is not called
        # again before stopped. But just to be extra sure we start/stop it
        # fast then do the test checking after.
        hello.run()
        hello.stop()

        expect(node.firstChild.tagName).toBe("H1")
        expect(node.children.length).toBe(1)

        # Remove this message from possible greetings. This ensures that we will
        # definitely get a different message next iteration.
        firstMsg = node.firstChild.innerText
        for greeting, i in hello.MESSAGES
            if greeting.msg == firstMsg
                # See: http://stackoverflow.com/a/5767357
                hello.MESSAGES.splice(i, 1)
                break

        hello.run()
        hello.stop()

        expect(node.firstChild.tagName).toBe("H1")
        expect(node.children.length).toBe(1)

        secondMsg = node.firstChild.innerText

        expect(secondMsg).not.toBe(firstMsg)
