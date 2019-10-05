from talon.voice import Word, Context, press, Key
from talon import clip 

from ..utils import (
    insert,
    normalise_keys,
    parse_word,
    surround,
    text,
    sentence_text,
    word,
    parse_words,
    spoken_text,
    enter_text
)


def title_case_capitalize_word(index, word, _):
    words_to_keep_lowercase = "a,an,the,at,by,for,in,of,on,to,up,and,as,but,or,nor".split(
        ","
    )
    if index == 0 or word not in words_to_keep_lowercase:
        return word.capitalize()
    else:
        return word


formatters = normalise_keys(
    {
        # "tree": (True, lambda i, word, _: word[0:3] if i == 0 else ""),
        # "quad": (True, lambda i, word, _: word[0:4] if i == 0 else ""),
        "(camel)": (
            True,
            lambda i, word, _: word if i == 0 else word.capitalize(),
        ),
        "pathway": (True, lambda i, word, _: word if i == 0 else "/" + word),
        "pebble": (True, lambda i, word, _: word if i == 0 else "." + word),
        "yellsmash": (True, lambda i, word, _: word.upper()),
        "(allcaps | yeller)": (False, lambda i, word, _: word.upper()),
        "yellsnik": (
            True,
            lambda i, word, _: word.upper() if i == 0 else "_" + word.upper(),
        ),
        "dollcram": (
            True,
            lambda i, word, _: "$" + word if i == 0 else word.capitalize(),
        ),
        # "champ": (True, lambda i, word, _: word.capitalize() if i == 0 else " " + word),
        "lowcram": (
            True,
            lambda i, word, _: "@" + word if i == 0 else word.capitalize(),
        ),
        # "(criff | criffed)": (True, lambda i, word, _: word.capitalize()),
        "tridal case": (False, lambda i, word, _: word.capitalize()),
        "snake": (True, lambda i, word, _: word if i == 0 else "_" + word),
        # "dotsnik": (True, lambda i, word, _: "." + word if i == 0 else "_" + word),
        # "smash": (True, lambda i, word, _: word),
        "(kebab case)": (True, lambda i, word, _: word if i == 0 else "-" + word),
        "title case": (False, title_case_capitalize_word),
    }
)

surrounders = normalise_keys(
    {
        "(dubstring | quotes)": (False, surround('"')),
        # "(string)": (False, surround("'")),
        "(tics | glitch)": (False, surround("`")),
        "padded": (False, surround(" ")),
        "dunderscore": (False, surround("__")),
        "angle": (False, surround("<", ">")),
        "brax": (False, surround("[", "]")),
        "curly": (False, surround("{", "}")),
        "precoif": (False, surround('("', '")')),
        "(prekris)": (False, surround("(", ")")),
    }
)

formatters.update(surrounders)


def FormatText(m):
    fmt = []

    for w in m._words:
        if isinstance(w, Word) and w != "over":
            fmt.append(w.word)
    words = parse_words(m)
    if not words:
        try:
            with clip.capture() as s:
                press("cmd-c")
            if "\n" in s.get():
                words=[]
            
            words = s.get().split(" ")
        except clip.NoChange:
            words = [""]

    tmp = []

    smash = False
    for i, w in enumerate(words):
        word = parse_word(w, True)
        for name in reversed(fmt):
            smash, func = formatters[name]
            word = func(i, word, i == len(words) - 1)
        tmp.append(word)

    sep = "" if smash else " "
    insert(sep.join(tmp))
    # if no words, move cursor inside surrounders
    if not words[0]:
        for i in range(len(tmp[0]) // 2):
            press("left")


ctx = Context("formatters")

ctx.keymap(
    {
        "(phrase) <dgndictation> [over]": text,
        "(skray) <dgndictation>++ [over]": text,
        "(pounce) <dgndictation> [over]": enter_text,
        
        "(spray) <dgndictation> [over]": [" ", text],
        "(aft | insert) <dgndictation> [over]": [text, " "],
        "(sent) <dgndictation> [over]": sentence_text,
        "(sentence) <dgndictation>++ [over]": sentence_text,
        "(comma | ,) <dgndictation> [over]": [", ", spoken_text],
        "period <dgndictation> [over]": [". ", sentence_text],
        # "pounce <dgndictation>" : [text, Key('enter')],
        # "word <dgnwords>": word,
        "(%s)+ [<dgndictation>] [over]" % (" | ".join(formatters)): FormatText,
        # to match surrounder command + another command (i.e. not dgndictation)
        "(%s)+" % (" | ".join(surrounders)): FormatText,
    }
)
