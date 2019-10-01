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
    go_site = json.loads(resource.read('go_site.json'))
except FileNotFoundError:
    go_site = {}
try:
    go_dir = json.loads(resource.read('go_dir.json'))
except FileNotFoundError:
    go_dir = {}
    

def run_go_site(m):
    name = m['geodude.go_site'][0]
    path = go_site.get(name)
    if not path:
        app.notify(f'Goto "{name}" failed', body='No path associated')
        return
    webbrowser.open(path)

def run_go_dir(m):
    name = m['geodude.go_dir'][0]
    path = go_dir.get(name)
    if not path:
        app.notify(f'Goto "{name}" failed', body='No path associated')
        return
    webbrowser.open(path) # not working

def run_go_term(m):
    name = m['geodude.go_dir'][0]
    path = go_dir.get(name)
    if not path:
        app.notify(f'Goto "{name}" failed', body='No path associated')
        return
    insert(f'cd {path}')    
    

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
    # 'else:
    # '    path = 'file://' + pathname2url(win.doc)
    #     print(path)
    if not path:
        notify('No location found.')
        raise ValueError('No location found.')
    return path

def save_goto(m):
    # print(m)
    print(("starting function"))
    name = ' '.join(m.dgndictation[0])
    print(("print statement 2"))

    try:
        location = get_location_url()
    except Exception as e:
        notify('Save failed', body=str(e))
        print(("exception"))
        return
        
    app = ui.active_app()

    print(app)
    print(("print statement 3"))
    if app.name in ('Safari', 'Google Chrome', 'Firefox'):
        print("browser")
        
        go_site[name] = location
        resource.write('go_site.json', json.dumps(go_site))
        notify(f'Saved "{name}"', body=location)
    if app.name == "Finder":
        print("finder")
        go_dir[name] = location
        resource.write('go_dir.json', json.dumps(go_dir))
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
    'go to [site] {geodude.go_site}': run_go_site,
    'go to [folder] {geodude.go_dir}': run_go_dir,
    '(c d  | change directory) {geodude.go_dir}': run_go_term,
    'bookmark [as] <dgndictation>': save_goto,
    "test out this command": lambda m: ctrl.mouse_move(1257, 269),
    "center kick": lambda m: ctrl.mouse_move(720, 393),
    'copy app bundle': lambda m: clip.set(ui.active_app().bundle),
    
})
ctx.set_list('map', punctuation)
ctx.set_list('go_site', go_site)
ctx.set_list('go_dir', go_dir)
ctx.set_list('a', numbers)
ctx.set_list('b', numbers)
