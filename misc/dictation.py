"""
when someone has the time to help debug, message aegis

    aegis [11:40 AM]
    You can do vars(user.whatever.speech_toggle.dictation_group) while you’re in dictation mode
    Where whatever is the intermediate python
"""

from talon.voice import Str, Key, Context
from talon import ui

from .speech_toggle import dictation
from .basic_keys import alphabet
from .. import vocab


# cleans up some Dragon output from <dgndictation>
mapping = {"semicolon": ";", "new-line": "\n", "new-paragraph": "\n\n"}
# used for auto-spacing
punctuation = set(".,-!?)")
sentence_ends = set(".!?").union({"\n", "\n\n"})


def insert(s):
    Str(s)(None)


class AutoFormat:
    def __init__(self):
        self.reset()
        ui.register("app_deactivate", lambda app: self.reset())
        ui.register("win_focus", lambda win: self.reset())

    def reset(self):
        self.caps = True
        self.space = False

    def insert_word(self, word):
        word = str(word).lstrip("\\").split("\\", 1)[0]
        word = vocab.vocab_alternate.get(word, word) # what is going on here?
        word = mapping.get(word, word)
        word = word.rstrip("-")

        if self.caps:
            word = word[0].upper() + word[1:]

        if self.space and word[0] not in punctuation and "\n" not in word:
            insert(" ")

        insert(word)

        self.caps = word in sentence_ends
        self.space = "\n" not in word and word != "("

    def phrase(self, m):
        for word in m.dgndictation[0]:
            self.insert_word(word)
    
    def set_cap(self, m):
        self.caps = True
    


auto_format = AutoFormat()
dictation.keymap({
    
    "new line": Key("enter"),
    "fly lease": Key('left'),
    "bird": Key('alt-left'),
    "firch": Key('alt-right'),
    "lease": Key('left'),
    "ross": Key('right'),
    "splat": Key('alt-backspace'),
    "spratter": Key('alt-delete'),
    # "alpha": [Key('space cmd-m'), "\\alpha "],
    # "beater": [Key('space cmd-m'), "\\beater "],
    # "delta": [Key('cmd-m'), "\\delta "], 
    "(ace | space bar)": Key('space'),
    "lazer": "(",
    # "razer": ")",
    "word <dgnwords>": lambda m: auto_format.insert_word(m.dgnwords[0][0]),
    "huge": auto_format.set_cap,
    "<dgndictation>": auto_format.phrase,
})
 

from .speech_toggle import dictation_group


from ..apps.lyx import greek_letters
# swap below to switch back to the old way
lyx_dictation = Context('lyx_dictation', bundle='org.lyx.lyx', group=dictation_group)
# lyx_dictation = Context('lyx_dictation', bundle='org.lyx.lyx')
# lyx_dictation = Context('lyx_dictation', bundle='com.microsoft.VSCode', group=dictation_group)
# alphabet =  basic_keys.alphabet
english_alphabet = alphabet
lyx_dictation.set_list('alphabet', alphabet)
lyx_dictation.set_list('greek', greek_letters)
lyx_dictation.keymap({
    "alex letter": [Key('cmd-m'), r"\epsilon "],
    "math {lyx_dictation.alphabet}": [" ", Key('cmd-m'), 
        lambda m: insert(f'{alphabet[m.alphabet[0]]}'), Key('right space')],
    "math big {lyx_dictation.alphabet}": [" ", Key('cmd-m'), 
        lambda m: insert(f'{alphabet[m.alphabet[0]].title()}'), Key('right space')],
    "math {lyx_dictation.greek}": [" ", Key('cmd-m'), 
        lambda m: insert(f'\\{greek_letters[m.greek[0]]}'), Key('right space')],
    "math big {lyx_dictation.greek}": [" ", Key('cmd-m'), 
        lambda m: insert(f'\\{greek_letters[m.greek[0]].title()}'), Key('right space')],

    
        
})
