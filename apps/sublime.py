import time
from talon.voice import Key, Context, Str, press
from ..utils import parse_words_as_integer, repeat_function, optional_numerals, text

ctx = Context("sublime", bundle="com.sublimetext.3")

def jump_to_line(m):
    line_number = parse_words_as_integer(m._words[1:])

    if line_number is None:
        return

    # Zeroth line should go to first line
    if line_number == 0:
        line_number = 1

    press("ctrl-g")
    time.sleep(0.2)
    Str(str(line_number))(None)
    press("enter")



keymap = {
    
    # Latex
    "color box": ["\\colorbox{gray}{}", Key('left')],

    # Sublime specific
    # general
    "green it": Key('cmd-/'),
    "liner" + optional_numerals: jump_to_line,
    "comment super": Key("cmd-alt-/"),

    "sidebar": [Key("cmd-k"), Key("cmd-b")],
    "(subl | sublime) (focus | folk) sidebar": Key("ctrl-0"),
    "console": Key("ctrl-`"),
    "[command] pallet": Key("cmd-shift-p"),
    "(column | row) one": Key("alt-cmd-1"),
    "column two": Key("alt-cmd-2"),
    "column three": Key("alt-cmd-3"),
    "row two": Key("shift-alt-cmd-2"),
    "row three": Key("shift-alt-cmd-3"),
    "grid": Key("alt-cmd-5"),
    # window
    "(subl | sublime) new window": Key("shift-cmd-n"),
    # close window
    # file
    "(save | safe) all": Key("cmd-alt-s"),
    "revert": Key("ctrl-alt-r"),  # requires adding key binding
    "go file": Key("cmd-t"),
    # selection
    "(select line | shackle)": Key("cmd-l"),
    "(select | cell) word": Key("cmd-d"),
    "all word": Key("cmd-ctrl-g"),  # expand currently selected word to all
    "(select | cell) current": Key(
        "ctrl-cmd-g"
    ),  # select all occurrences of current selection
    "(select | cell) scope": Key("shift-cmd-space"),
    "(select | cell) (bracket | paren)": Key("ctrl-shift-m"),
    "bracken": [Key("ctrl-shift-m")],
    "(select | cell) indent": Key("shift-cmd-j"),
    "cursor up": Key("ctrl-shift-up"),
    "cursor down": Key("ctrl-shift-down"),
    "cursor push": Key("cmd-shift-l"),
    "cursor pop": [Key("cmd-shift-l"), Key("cmd-left")],
    "(cursor | select) undo": Key("cmd-u"),
    "undo (select | cursor)": Key("cmd-u"),
    "(select | cell) sky": Key("ctrl-shift-up"),
    # "bounce [right]": Key("ctrl-alt-shift-right"),
    # "bound": Key("ctrl-alt-shift-left"),
    "bounce (left | back)": Key("ctrl-alt-shift-left"),
    # edit
    "snipline super": Key("ctrl-shift-k"),
    "duple": Key("cmd-shift-d"),
    # "up slap": Key("cmd-shift-enter"),
    # "(scrap | scratch | delete) end": [Key("cmd-k"), Key("cmd-k")],
    # "(uppercase | upcase)": [Key("cmd-k"), Key("cmd-u")],
    # "(lower | lowercase | downcase)": [Key("cmd-k"), Key("cmd-l")],
    # navigation
    "go line": Key("ctrl-g"),
    "tab last": Key("cmd-shift-["),
    "tab next": Key("cmd-shift-]"),
    "match bracket": Key("ctrl-m"),
    "go forward": Key("ctrl-alt-f"),
    "go back": Key("ctrl-alt-b"),
    # "jump (up | start)": Key("cmd-up"),
    # "jump (down | end)": Key("cmd-down"),
    # find & replace
    # "(subl | sublime) find": Key("cmd-f"),
    "expression": Key("alt-cmd-r"),
    "case insensitive": Key("alt-cmd-c"),
    "whole word": Key("alt-cmd-w"),
    
}
ctx.keymap(keymap)