from talon.voice import Key, press, Str, Context, ContextGroup
from talon.voice import Context, Rep, RepPhrase, talon
from .. import utils

# latex_group = ContextGroup("latex")
latex_ctx = Context("latex", func= lambda app, win: app.bundle in ["com.sublimetext.3", "texmaker", "com.google.Chrome"])
keymap = {"color box": ["\\colorbox{gray}{}", Key('left')],
"footnote": ["\\footnote{}", Key('left')],
"equation ref": ["\\eqref{}", Key('left')],
"labeler": ["\\label{}", Key('left')],
"quader": "\\quad ",
"enspacer":"\\enspace",
"dollz": ["$$", Key('left')],
}

latex_ctx.keymap(keymap)
  