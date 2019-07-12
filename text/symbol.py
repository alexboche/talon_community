from talon.voice import Context, Key

ctx = Context("symbol")

keymap = {
    # simple
    "(question [mark] | questo)": "?",
    "plus": "+",
    "tilde": "~",
    "clamor": "!",
    "(dolly)": "$",
    "score": "_",
    "(deckle | kholer)": ":",
    "lazer": "(",
    "(razer)": ")",
    "(left curl)": "{",
    "(right curl)": "}",
    "(langle)": "<",
    "(rangle)": ">",
    "(aepo | stingle)": "'",
    "(starling | asterisk)": "*",
    "(hash tag)": "#",
    "moddy": "%",
    "caret": "^",
    "atty": "@",
    "(and sign | ampersand | amper)": "&",
    "(piper)": "|",
    "piping": " | ",
    "boom": ", ",
    "(doter)": '"',
    "long equals": " = ",
    "long minus": " - ",
    "long plus": " + ",
    "double": " = ",

    # compound
    # "mintwice": "--",
    # "plustwice": "++",
    "minquall": "-=",
    "pluqual": "+=",
    "starqual": "*=",
    # "triple quote": "'''",
    # "triple tick": "```",
    # "[forward] dubslash": "//",
    # "coal twice": "::",
    # "(dot dot | dotdot)": "..",
    # "(ellipsis | dot dot dot | dotdotdot)": "...",
    # unnecessary: use repetition commands?
}

ctx.keymap(keymap)
