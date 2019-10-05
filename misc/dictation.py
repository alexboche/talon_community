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
        # self.caps = True
        self.caps = False
        self.space = False

    def insert_word(self, word):
        # print(word)ee
        word = str(word).lstrip("\\").split("\\", 1)[0]
        word = vocab.vocab_alternate.get(word, word) # what is going on here?
        word = mapping.get(word, word)
        word = word.rstrip("-")

        if self.caps:
            word = word[0].upper() + word[1:]

        if self.space and word[0] not in punctuation and "\n" not in word:
            insert(" ")

        insert(word)
        # self.set_nocaps()
        self.caps=False

        # self.caps = word in sentence_ends
        self.space = "\n" not in word and word not in set("(-")

    def phrase(self, m):
        for word in m.dgndictation[0]:
            self.insert_word(word)
    
    def set_cap(self, m):
        self.caps = True
    def set_nocaps(self, m):
        self.caps = False
    


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
    "no caps": auto_format.set_nocaps, # why doesn't this work?
    "<dgndictation>": auto_format.phrase,
})
 

from .speech_toggle import dictation_group


from ..apps.lyx import greek_letters, math_vocab, eg_alph
# swap below to switch back to the old way
lyx_dictation = Context('lyx_dictation', bundle='org.lyx.lyx', group=dictation_group)
# lyx_dictation = Context('lyx_dictation', bundle='org.lyx.lyx')
# lyx_dictation = Context('lyx_dictation', bundle='com.microsoft.VSCode', group=dictation_group)
# alphabet =  basic_keys.alphabet
english_alphabet = alphabet
lyx_dictation.set_list('alphabet', alphabet)
lyx_dictation.set_list('greek', greek_letters)
relations = math_vocab["non_braces"]["relations"]
lyx_dictation.set_list('relations', relations)
lyx_dictation.set_list('eg_alph1', eg_alph)
lyx_dictation.set_list('eg_alph2', eg_alph)
# lyx_dictation.set_list('math_vocab', math_vocab)
lyx_dictation.keymap({
    "alex letter": [Key('cmd-m'), r"\epsilon "],
    "math {lyx_dictation.alphabet}": [" ", Key('cmd-m'), 
        lambda m: insert(f'{alphabet[m.alphabet[0]]}'), Key('right space')],
    "math big {lyx_dictation.alphabet}": [" ", Key('cmd-m'), 
        lambda m: insert(f'{alphabet[m.alphabet[0]].title()}'), Key('right space')],
     "math {lyx_dictation.relations}": [" ", Key('cmd-m'), 
        lambda m: insert(f'{relations[m.relations[0]]}'), Key('right space')],
    "math {lyx_dictation.eg_alph1} of {lyx_dictation.eg_alph2}": 
      [" ", Key('cmd-m'), 
      lambda m: 
      insert(f"{eg_alph[m.eg_alph1[0]]}({eg_alph[m.eg_alph1[0]]})"), 
      Key('right space')],

    # "math {lyx_dictation.math_vocab}": [" ", Key('cmd-m'), 
    #     lambda m: insert(f'\\{math_vocab[m.math_vocab[0]]}'), Key('right space')],
    "math {lyx_dictation.greek}": [" ", Key('cmd-m'), 
        lambda m: insert(f'{greek_letters[m.greek[0]]}'), Key('right space')],
    "math big {lyx_dictation.greek}": [" ", Key('cmd-m'), 
        lambda m: insert(f'{greek_letters[m.greek[0]].title()}'), Key('right space')],

    
        
})
