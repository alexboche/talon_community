
from talon.voice import Context, Key, Str
from talon import ctrl, clip, resource, ui

ctx = Context("autotext")
ctx.keymap(
    {"(student|university) id": "3044905",
    "excuse typos": "(Please excuse any typos/speakos, this message was typed by voice)",
    "northwestern e-mail": "alexander.boche@kellogg.northwestern.edu",
    # "new line": "\n",
    }
    
)

