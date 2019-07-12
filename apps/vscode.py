import time
from talon.voice import Context, Key, press, Str
from ..utils import parse_words_as_integer, repeat_function, optional_numerals, text

context = Context("VSCode", bundle="com.microsoft.VSCode")


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


def jump_tabs(m):
    line_number = parse_words_as_integer(m._words[1:])

    if line_number is None:
        return

    for i in range(0, line_number):
        press("cmd-alt-right")


def jump_to_next_word_instance(m):
    press("escape")
    press("cmd-f")
    Str(" ".join([str(s) for s in m.dgndictation[0]._words]))(None)
    press("return")


def select_lines_function(m):
    divider = 0
    for word in m._words:
        if str(word) == "until":
            break
        divider += 1
    line_number_from = int(str(parse_words_as_integer(m._words[2:divider])))
    line_number_until = int(str(parse_words_as_integer(m._words[divider + 1 :])))
    number_of_lines = line_number_until - line_number_from

    press("cmd-g")
    Str(str(line_number_from))(None)
    press("enter")
    for i in range(0, number_of_lines + 1):
        press("shift-down")


context.keymap(
    {
        # Selecting text
        "select line"
        + optional_numerals
        + "until"
        + optional_numerals: select_lines_function,
        # Finding text
        "find": Key("cmd-f"),
        "find next <dgndictation>": jump_to_next_word_instance,
        # Clipboard
        "clone": Key("alt-shift-down"),
        # Navigation
        "liner" + optional_numerals: jump_to_line,
        "Go to line": Key("cmd-g"),
        
        # Navigating Interface
        "explore tab": Key("shift-cmd-e"),
        "search tab": Key("shift-cmd-f"),
        "debug tab": Key("shift-cmd-d"),
        "source control tab": Key("shift-ctrl-g"),
        "extensions tab": Key("shift-cmd-x"),
        "go to file <dgndictation>": [Key("cmd-p"), text],
        "master": Key("cmd-p"),
        # tabbing
        "stiffy": Key("cmd-alt-left"),
        "(next tab | nexta)": Key("cmd-alt-right"),
        "stippy": Key("cmd-alt-right"),
        "(prexta | prior tab | untab)": Key("cmd-alt-left"),
        "new tab": Key("cmd-n"),
        "jump" + optional_numerals: jump_tabs,
        # Menu
        "save": Key("cmd+s"),
        "open": Key("cmd+o"),
        # editing
        "bracken": [Key("cmd-shift-ctrl-right")],
        # various
        "green it": Key("cmd-/"),
        "search all": Key("cmd-shift-f"),
        "(drop-down)": Key("ctrl-space"),
        "command pallet":Key('cmd-shift-p'),
        "settings": Key('cmd-,'),

        # basic editing
        "[switch] line up" + optional_numerals: repeat_function(2, "alt-up"),
        "[switch] line down" + optional_numerals: repeat_function(2, "alt-down"),
        "copy [line] down": Key('shift-alt-down'),
        "copy [line] up": Key('shift-alt-up'),
        "delete line": Key('ctrl-shift-k'),
        "line below": Key('cmd-enter'),
        "line above": Key('cmd-shift-enter'),  
        "indent": [Key('cmd-left'), Key('tab')],
        "outdent": [Key('cmd-left'), Key('shift-tab')],
        "match (bracket | pair)": Key('cmd-shift-\\'),
        # "scroller page down": Key-('cmd-pagedown'),
        # "scroller down": Key('ctrl-pageup'),
        # "scroller up": Key('ctrl-pagedown'),
        # "scroller page up": Key-('cmd-pageup'),
        "fold region": Key('cmd-alt-['),
        "unfold region": Key('cmd-alt-]'),
        "fold all subregions": Key('cmd-k cmd-['),
        "unfold all subregions": Key('cmd-k cmd-]'),
        "fold all regions": Key('cmd-k cmd-0'),
        "unfold all regions": Key('cmd-k cmd-j'), 
        "toggle block comment": Key('shift-alt-a'),
        "toggle word wrap": Key('alt-z'), 

        # Multi cursor and selection
        # "insert cursor": Key('alt-click'), don't know how to make this
        "cursor above": Key('cmd-alt-up'),
        "cursor below": Key('cmd-alt-down'),
        "cursor up": Key('cmd-shift-alt-up'), # other multi cursor commands
        "cursor down": Key('cmd-shift-alt-down'), 
        "cursor left": Key('cmd-shift-alt-left'), 
        "cursor right": Key('cmd-shift-alt-left'), 
        "cursor far up": Key('cmd-shift-alt-pageup'),
        "cursor far down": Key('cmd-shift-alt-pageup'),
        "[undo] last cursor [operation]": Key('cmd-u'),
        "(cursor selected | insert cursor at end of each line selected)":Key('shift-alt-i'),
        "(current selection | select all occurrences of current selection)": Key('shift-cmd-l'),
        "(current word | select all occurrences of current word)": Key('cmd-f2'),
        "expand": Key('cmd-ctrl-shift-right'),
        "shrink": Key('cmd-ctrl-shift-left'),

        # Search and replace
        "replace": Key('alt-cmd-f'),
        "next match": Key('cmd-g'),
        "previous match": Key('cmd-shift-g'),
        "select all matches": Key('alt-enter'),
        "add selection to next [find] match": Key('cmd-d'),
        "move last selection to next [find] match": Key('cmd-k cmd-d'),

        # Rich languages editing
        "[trigger] suggestion": Key('ctrl-space'),
        "[trigger] parameter [hints]": Key('cmd-shift-space'),
        "format document": Key('shift-alt-f'),
        "format selection": Key('cmd-k cmd-f'),
        "(definition | deffy)": Key('f12'),
        "peak (def | definition)": Key('alt-f12'),
        "definition [to the] side": Key('cmd-k f12'),
        "quick fix": Key('cmd-.'),
        "show references": Key('shift-f12'),
        "rename symbol": Key('f2'),
        "trim [trailing] white": Key('cmd-k cmd-x'),
        "change file language": Key('cmd-k cmd-m'),


        # Navigation
        "show all symbols": Key('cmd-t'),
        "go to symbol": Key('cmd-shift-o'),
        "[show] problems [panel]": Key('cmd-shift-m'),
        "next error": Key('f8'),
        "(prior | previous) error": Key('shift-f8'),
        "[navigate] [editor] group history": Key('ctrl-shift-tab'),
        "go back": Key('ctrl--'),
        "[go] forward": Key('ctrl-shift--'),
        "toggle tab moves focus": Key('ctrl-shift-m'),

        # Editor management
        "close editor": Key('cmd-w'),
        "close folder": Key('cmd-k f'),
        "split (editor | screen)": Key('cmd-/'),
        "first (pane | group)": Key('cmd-1'),
        "second (pane | group)": Key('cmd-2'),
        "third (pane | group)": Key('cmd-3'),
        "next pane": Key('cmd-k cmd-shift-right'),
        "(prior | previous | un) pane": Key('cmd-k cmd-shift-left'),
        "push pane left": Key('ctrl-cmd-left'),
        "push pane right": Key('ctrl-cmd-right'),

        # File management
        "new file": Key('cmd-n'),
        "open [file]": Key('cmd-o'),
        "save as": Key('cmd-shift-s'),
        "save all": Key('ctrl-cmd-s'),
        "close": Key('cmd-w'),
        "close all": Key('cmd-k cmd-w'),
        "reopen [tab | editor]": Key('cmd-shift-t'),
        "keep preview mode editor": Key('cmd-k enter'),
        "copy path": Key('cmd-k p'),
        "open in finder": Key('cmd-k r'),
        "new instance [of active file]": Key('cmd-k o'),

        

        # Display
        "explorer": Key('cmd-shift-e'),
        "full screen": Key('ctrl-cmd-f'),
        "toggle (vertical | horizontal)": Key('alt-cmd-0'),
        "zoom in": Key('cmd-='),
        "zoom out": Key('shift-cmd--'),
        "sidebar": Key('cmd-b'),
        "find in files": Key('cmd-shift-f'),
        "[show] source control": Key('ctrl-shift-g'),
        "[show] debug": Key('cmd-shift-d'),
        "extensions": Key('cmd-shift-x'),
        "replace in files": Key('cmd-shift-h'),
        "search details": Key('cmd-shift-j'),
        "[show] output panel": Key('cmd-shift-u'),
        "[open] markdown preview": Key('cmd-shift-v'),
        "markdown preview [to the] side": Key('cmd-k v'),
        "zen mode": Key('cmd-k z'), # esc esc to exit

        "terminal": Key('ctrl-`'),









    }
)
