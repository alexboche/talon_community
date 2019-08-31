import time
from .. import utils
from talon.voice import Context, Key, Str, press
from talon import ctrl, clip, resource, ui
from ..misc.switcher import switch_app

def insert(s):
    return Str(str(s))(None)

def insert_number(m):
    number = utils.parse_words_as_integer(m._words[1:])

    if number is None:
        return
    time.sleep(0.3)
    # press("cmd-g")
    Str(str(number))(None)
    time.sleep(0.1)
    press("enter")

ctx = Context("acrobat", bundle="com.adobe.Reader")
ctx.set_list("n", utils.numeral_list)
# adobe acrobat reader dc
ctx.keymap(
    {
        "hommer": [lambda m: ctrl.mouse_move(25, 57)],
        # "hommer": lambda m: ctrl.mouse_click(25, 57, button=0,  times=1, wait=10000),
        "alex test": Key('a'),
        "new note": [lambda m: ctrl.mouse_click(button=1), Key('down'), Key('enter')],
        "pager" + utils.optional_numerals: [Key('cmd-shift-n'), insert_number, Key('enter')],
        "set zoom" + utils.optional_numerals: [Key('cmd-y'), insert_number, Key('enter')],
# ctrl.mouse_click(x, y, button=button, times=times, wait=16000)
    }
)