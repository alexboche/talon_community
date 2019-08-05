from urllib.request import pathname2url
import json
import webbrowser

from talon.voice import Context, Key, Str
from talon import ctrl, clip, resource, ui
from talon.app import notify


numbers = {str(i): i for i in range(1, 101)}
# helper functions that will go away with newapi
def insert(s):
    Str(s)(None)

def key(key):
    Key(key)(None)

# copy mouse command implementation
def copy_mouse_command(m):
    x, y = map(int, ctrl.mouse_pos())
    clip.set(f'ctrl.mouse_move({x}, {y})')

# tell_key implementation
punctuation = {
    'period': '.',
    'comma': ',',
}
def tell_key(m):
    p = punctuation[m['geodude.map'][0]]
    ctrl.key_press(p)

# goto/save implementation
try:
    goto = json.loads(resource.read('goto.json'))
except FileNotFoundError:
    goto = {}

def run_goto(m):
    name = m['geodude.goto'][0]
    path = goto.get(name)
    if not path:
        app.notify(f'Goto "{name}" failed', body='No path associated')
        return
    webbrowser.open(path)

def get_location_url():
    app = ui.active_app()
    win = ui.active_window()
    if app.name in ('Safari', 'Google Chrome', 'Firefox'):
        with clip.capture() as s:
            key('cmd-l cmd-a cmd-c')
        path = s.get()
        ctrl.key_press('esc')
    elif app.name == "Finder":
        with clip.capture() as s:
            key('cmd-alt-c')
        # path = s.get()
        path = 'file://' + pathname2url(s.get())
    else:
        path = 'file://' + pathname2url(win.doc)
        print(path)
    if not path:
        notify('No location found.')
        raise ValueError('No location found.')
    return path

def save_goto(m):
    print(m)
    name = ' '.join(m.dgndictation[0])
    try:
        location = get_location_url()
    except Exception as e:
        notify('Save failed', body=str(e))
        return

    goto[name] = location
    resource.write('goto.json', json.dumps(goto))
    notify(f'Saved "{name}"', body=location)
# end save/goto
def insert(s):
    return Str(str(s))(None)
    
def add(a, b, c, d):
    insert(a + b + c + d)

ctx = Context('geodude')
ctx.keymap({
    'addition {geodude.a} {geodude.b}': lambda m: add(numbers[m.a[0]], numbers[m.b[0]], 5, 6),
      
    'copy mouse command': copy_mouse_command,
    'tell {geodude.map}': [Key('cmd-right'), tell_key, Key('enter')],
    'go to [bookmark] {geodude.goto}': run_goto,
    'bookmark [as] <dgndictation>': save_goto,
    "test out this command": lambda m: ctrl.mouse_move(1257, 269),
    "center kick": lambda m: ctrl.mouse_move(720, 393),
    'copy app bundle': lambda m: clip.set(ui.active_app().bundle),
    
})
ctx.set_list('map', punctuation)
ctx.set_list('goto', goto)
ctx.set_list('a', numbers)
ctx.set_list('b', numbers)
