import time

from .. import utils
from .web import browser
from ..misc import switcher
# from ..misc import delayed_right_click 

from talon import ui
from talon.voice import Context, Key, Str, press

# It is recommended to use this script in tandem with Vimium, a Google Chrome plugin for controlling the browser via keyboard
# https://vimium.github.io/

context = Context("GoogleChrome", bundle="com.google.Chrome")


def get_url(win=None):
    if win is None:
        win = ui.active_window()
    return tuple(win.children.find(AXRole="AXTextField")[0].AXValue)[0].AXValue


def set_url(url, win=None):
    if win is None:
        win = ui.active_window()
    focus_address_bar()
    utils.paste_text(url)


def navigate_to_url(url, win=None):
    set_url(url, win)
    press("enter")


def open_focus_devtools(m):
    press("cmd-shift-c")


def show_panel(name):
    open_focus_devtools(None)

    # Open command menu
    press("cmd-shift-p")

    Str("Show %s" % (name))(None)
    press("enter")


def next_panel(m):
    open_focus_devtools(None)
    press("cmd-]")


def last_panel(m):
    open_focus_devtools(None)
    press("cmd-[")


def focus_address_bar(m=None):
    press("cmd-l")


# Return focus from the devtools to the page
def refocus_page(m):
    focus_address_bar(None)
    time.sleep(0.1)
    press("escape")
    press("escape")
    # time.sleep(0.1)
    # This leaves the focus on the page at previous tab focused point, not the beginning of the page
    press("tab")


def back(m):
    refocus_page(None)
    press("cmd-[")
    # refocus_page(None)


def forward(m):
    refocus_page(None)
    press("cmd-]")
    refocus_page(None)


def link(m):
    refocus_page(None)
    press("f")


def jump_tab(m):
    tab_number = utils.parse_words_as_integer(m._words[1:])
    if tab_number is not None and tab_number > 0 and tab_number < 9:
        press("cmd-%s" % tab_number)


def mendeley(m):
    navigate_to_url(f"https://www.mendeley.com/import/?url={get_url()}")


webpages = utils.load_config_json("webpages.json")


def get_webpage(m):
    return webpages[" ".join(m["global_browser.webpages"])]


def go_to_webpage(m):
    press("cmd-t")
    navigate_to_url(get_webpage(m))

WORDS =  {'old': 'elderly', 'young': 'YANG'}
context.set_list('person', WORDS.keys())
context.set_list("n", utils.numeral_list)


def insert(s):
    return Str(str(s))(None)

def insert_number(m):
    number = utils.parse_words_as_integer(m._words[1:])

    if number is None:
        return
    time.sleep(0.3)
    # press("cmd-g")
    Str(str(number))(None)
    # time.sleep(0.1)
    # Str(":p")(None)
    #  press("enter")

# def cbv_push(m):
#     number = utils.parse_words_as_integer(m._words[1:])

#     if number is None:
#         return
#     time.sleep(0.3)
#     # press("cmd-g")
#     Str(str(number))(None)
#     # press("enter")

context.keymap(
    {
        "(address bar | focus address | focus url | url | quick bar)": focus_address_bar,
        "copy url": Key("escape y y"),
        "go back": back,
        "go forward": forward,
        "page reload": Key("cmd-r"),
        "reload page": Key("cmd-r"),
        "hard reload": Key("cmd-shift-r"),
        "new tab": Key("cmd-t"),
        # "new tab {global_browser.webpages}": go_to_webpage,
        "close tab": Key("cmd-w"),
        "reopen tab": Key("cmd-shift-t"),
        "(next tab | nabber)": Key("cmd-shift-]"),
        "((last | previous | preev) tab | labber)": Key("cmd-shift-["),
        "tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)": jump_tab,
        "(end | rightmost) tab": Key("cmd-9"),
        "marco": Key("cmd-f"),
        "marneck": Key("cmd-g"),
        # "(last | prevous)": Key("cmd-shift-g"),
        "toggle dev tools": Key("cmd-alt-i"),
        "command menu": Key("cmd-shift-p"),
        "next panel": next_panel,
        "(last | previous) panel": last_panel,
        "show application [panel]": lambda m: show_panel("Application"),
        "show audit[s] [panel]": lambda m: show_panel("Audits"),
        "show console [panel]": lambda m: show_panel("Console"),
        "show element[s] [panel]": lambda m: show_panel("Elements"),
        "show memory [panel]": lambda m: show_panel("Memory"),
        "show network [panel]": lambda m: show_panel("Network"),
        "show performance [panel]": lambda m: show_panel("Performance"),
        "show security [panel]": lambda m: show_panel("Security"),
        "show source[s] [panel]": lambda m: show_panel("Sources"),
        "(refocus | focus) page": refocus_page,
        "[refocus] dev tools": open_focus_devtools,
        # Clipboard
        "cut": Key("cmd-x"),
        "copy": Key("cmd-c"),
        "paste": Key("cmd-v"),
        "paste same style": Key("cmd-alt-shift-v"),
        # "mendeley": Key("cmd-shift-m"),
        "(add | save) to mendeley": mendeley,
        # TODO: this should probably be specific to the page
        "submit": Key("cmd-enter"),
        # zotero
        "zotero": Key("cmd-shift-z"),
        # rearrange tabs: https://chrome.google.com/webstore/detail/rearrange-tabs/ccnnhhnmpoffieppjjkhdakcoejcpbga
        # "move tab left": Key("ctrl-shift-left"),
        # "move tab right": Key("ctrl-shift-right"),
        # "move tab left way": Key("ctrl-shift-down"),
    #    "person {GoogleChrome.person}": lambda m: insert(WORDS[m['GoogleChrome.person'][0]]),
        "person {GoogleChrome.person}": [Key('cmd-t'), lambda m: insert(WORDS[m['GoogleChrome.person'][0]])],
        # "voice" + utils.optional_numerals: [Key('cmd-l'), time.sleep(0.2), insert_number],
        # "voice" + utils.optional_numerals: [Key('cmd-l'), insert_number],
        "voice" + utils.optional_numerals: [Key('cmd-shift-space'), insert_number, Key('enter')],
        "push" + utils.optional_numerals: [Key('cmd-shift-space'), insert_number, ":", "p", Key('enter')],
        # "nab that": [delayed_right_click, Key('down'), Key('enter')],
        # "hide hints": [Key('cmd-shift-space'), ":-", Key('enter')],
        # "commander": [Key('a'), "b"], # why doesn't this command you anything?
        # "commerce": ["b", Key('a')],
        # vimium
        
        "link": link,
        "move tab left": browser.send_to_vimium("<<"),
        "move tab right": browser.send_to_vimium(">>"),
        "move tab new window": browser.send_to_vimium("W"),
        "tab (named | by name)": browser.send_to_vimium("T"),
        "tab (named | by name) <dgndictation>": [
            browser.send_to_vimium("T"),
            utils.text,
            Key("enter"),
        ],
    }
)


def global_chrome_new_tab(m):
    switcher.switch_app(name="Google Chrome")
    press("cmd-t")


def global_go_to_webpage(m):
    switcher.switch_app(name="Google Chrome")
    go_to_webpage(m)


global_ctx = Context("global_browser")
global_ctx.set_list("webpages", webpages.keys())
global_ctx.keymap(
    {
        "chrome new tab": global_chrome_new_tab,
        "chrome new tab {global_browser.webpages}": global_go_to_webpage,
    }
)
