
from talon.voice import Context, Key, Str
from talon import ctrl, clip, resource, ui

ctx = Context("autotext")
ctx.keymap(
    {"(student|university) id": "3044905",
    "excuse typos": "(Please excuse any typos/speakos, this message was typed by voice)",
    "northwestern e-mail": "alexander.boche@kellogg.northwestern.edu",
    "memail": "akboche@gmail.com",
    "mumber": "3103839819",
    "Boshay": "Boche",
    "E G": "e.g. ",
    "mcmanus [address]": "1725 Orrington Ave #107",
    # "new line": "\n",
    }
    
)

