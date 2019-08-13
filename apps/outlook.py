from talon.voice import Context, Key
from ..misc.switcher import switch_app

ctx = Context("outlook", bundle="com.microsoft.Outlook")

ctx.keymap(
    {
        "reply": Key("cmd-r"),
        "reply all": Key('cmd-shift-r'),
        "forward [message]": Key('cmd-j'),
        "click send mail": Key("cmd-enter"),
        "clear flag": None,
        "next pain": Key("shift-ctrl-["),
        "(preev | previous | prior) pain": Key("shift-ctrl-]"),
        "dismiss outlook": [lambda m: switch_app(name="outlook"), Key("cmd-w")],
        "search": Key('cmd-shift-f'),
        "(empty) search": Key('cmd-a backspace escape'),
          # To got to the messages from the search bar it's two tabs
        "attach file": Key('cmd-e'),
        "insert emoji": Key('cmd-ctrl-space'),
        "toggle reading pain": Key('cmd-backslash'), # cmd-buckslash does work, but the key action seems to have trouble
        "[go to] mail view": Key('cmd-1'),
        "[go to] calendar view": Key('cmd-2'),
        "[go to] contacts view": Key('cmd-3'),
        "[go to] tasks view": Key('cmd-4'),
        "[go to] notes view": Key('cmd-5'),
        "close window": Key('cmd-w'),
        # "next [outlook] window": Key('cmd-tilde'),
        # "next [outlook] window": Key('cmd-backtick'),
        # "(preev | previous | prior) window": Key('cmd-shift-tilde'),
        # "(preev | previous | prior) window": Key('cmd-shift-backtick'),


    }
)


"""
pack = Packages.register
  name: "custom outlook"
  applications: ["com.microsoft.Outlook"]
  description: "custom commands for outlook"

pack.commands
  "reply-to-email":
    spoken: "reply to e-mail"
    misspoken: 'reply email'
    description: "reply to email"
    enabled: true
    action: (input) ->
      @key 'r', 'command'
  "send-email":
    spoken: "send e-mail"
    description: "send email"
    enabled: true
    action: (input) ->
      @key 'enter', 'command'
  "clear-flag":
    spoken: "clear flag"
    description: "clear flag"
    enabled: true
    action: (input) ->
      @do 'os:openMenuBarPath', ['Message', 'Follow Up', 'Clear Flag']

pack.implement
  'object:previous': -> @key '[', 'control'
  'object:next': -> @key ']', 'control'
  'object:backward': -> @key '[', 'shift control'
  'object:forward': -> @key ']', 'shift control'
"""
