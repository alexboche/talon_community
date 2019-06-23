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
    "deckle": ":",
    "lazer": "(",
    "(razer)": ")",
    "(brace)": "{",
    "(rbrace)": "}",
    "(langle)": "<",
    "(rangle)": ">",
    "aepo": "'",
    "(starling | asterisk)": "*",
    "(hash tag)": "#",
    "moddy": "%",
    "caret": "^",
    "atty": "@",
    "(and sign | ampersand | amper)": "&",
    "(piper)": "|",
    "(doter)": '"',
    # compound
    "mintwice": "--",
    "plustwice": "++",
    "minquall": "-=",
    "pluqual": "+=",
    "starqual": "*=",
    "triple quote": "'''",
    "triple tick": "```",
    "[forward] dubslash": "//",
    "coal twice": "::",
    "(dot dot | dotdot)": "..",
    "(ellipsis | dot dot dot | dotdotdot)": "...",
    # unnecessary: use repetition commands?
}

ctx.keymap(keymap)
