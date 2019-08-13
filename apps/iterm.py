from talon.voice import Key, Context
import json
ctx = Context("iterm", bundle="com.googlecode.iterm2")

# goto/save implementation
try:
    goto = json.loads(resource.read('goto.json'))
except FileNotFoundError:
    goto = {}

keymap = {
    "broadcaster": Key("cmd-alt-i"),
    "password": Key("cmd-alt-f"),

    # Pane creation and navigation
    "split horizontal": Key("cmd-shift-d"),
    "split vertical": Key("cmd-d"),
    "pane next": Key("cmd-]"),
    "pane last": Key("cmd-["),
}

ctx.keymap(keymap)
