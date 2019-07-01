
from talon.voice import Context, Key, Str
from talon import ctrl, clip, resource, ui
from ..misc.switcher import switch_app


ctx = Context("acrobat", bundle="com.adobe.Reader")
# adobe acrobat reader dc
ctx.keymap(
    {
        "hommer": [lambda m: ctrl.mouse_move(25, 57)],
        # "hommer": lambda m: ctrl.mouse_click(25, 57, button=0,  times=1, wait=10000),
        "alex test": Key('a'),
        "new note": [lambda m: ctrl.mouse_click(button=1), Key('down'), Key('enter')],
# ctrl.mouse_click(x, y, button=button, times=times, wait=16000)
    }
)