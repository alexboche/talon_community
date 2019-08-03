import toml
from talon.voice import Key, Context, Str

ctx = Context("lyx", bundle="org.lyx.lyx")
# ctx = Context("lyx", bundle="com.google.Chrome")

def insert(s):
    return Str(str(s))(None)

# formatting for latex symbols without curly braces and all Lyx codes
def format_without_braces(vocab_dict):
    lyx_vocab_dict = {k:"\\{} ".format(vocab_dict[k]) for k in vocab_dict}
    return lyx_vocab_dict

# formatting for LaTeX operators with curly braces only
# note that commands inputting latex symbols with curly braces must conclude
    # by pressing the left arrow key.
def format_with_braces(vocab_dict):
    
    latex_vocab_dict = {k:"\\{}{{}} ".format(vocab_dict[k]) for k in vocab_dict}    
    return latex_vocab_dict

def cap_symbol_letters(big, symbol):
    if big:
        symbol = symbol.title()
    return symbol
  
# const load the toml file
with open("/Users/alex/.talon/user/talon_community/apps/lyx_alex.toml") as f:
        math_vocab = toml.load(f)

# generate math vocabulary for symbols not requiring braces in latex
non_braces_math_vocab = {}
for category in math_vocab["non_braces"]:
    for spec in math_vocab["non_braces"][category]:
        non_braces_math_vocab[spec] = math_vocab["non_braces"][category][spec]

# generate math vocabulary for symbols requiring braces in latex
braces_math_vocab = {}
for category in math_vocab["braces"]:
    for spec in math_vocab["braces"][category]:
        braces_math_vocab[spec] = math_vocab["braces"][category][spec]

# generate full Lyx math vocabulary
lyx_math_vocab = non_braces_math_vocab.copy()
for spec in braces_math_vocab:
    lyx_math_vocab[spec] = braces_math_vocab[spec]

# print(math_vocab)
# print(lyx_math_vocab)
numbers = {str(i): i for i in range(1, 101)}
# helper functions that will go away with newapi
def insert(s):
    Str(str(s))(None)

ctx.set_list('a', numbers)
ctx.set_list('b', numbers)
ctx.set_list('symbol', lyx_math_vocab) 

def matrix(m):
    Key('ctrl-x')
    Str('math-matrix')

def lyx_insert(s):
    Key('ctrl-m')
    insert(s)
# def examine(s)


keymap = {

    # '[optional] bonfire': lambda m: insert(m._words[1]),


    # 'matrix {lyx.a} {lyx.b}':   lambda m: [Key('ctrl-x'), "math-matrix ", insert(numbers[m.a[0]]), " ", insert(numbers[m.b[0]]), Key('enter')],
    # 'matrix {lyx.a} by {lyx.b}':   lambda m: [insert(numbers[m.a[0]]), " ", insert(numbers[m.b[0]]), Key('enter')],
    'matrix {lyx.a} by {lyx.b}':   [Key('ctrl-x'), lambda m: insert(f"math-matrix {numbers[m.a[0]]} {numbers[m.b[0]]}\n")],
    "popper": Key('a space b'),
    'matty': lambda m: matrix,
    '{lyx.symbol}': [lambda m: insert(f"\\{lyx_math_vocab[m.symbol[0]]} ")],
    'get {lyx.symbol}': [Key('space'), lambda m: insert(f"\\{lyx_math_vocab[m.symbol[0]]} "), Key('right')],
    # this one is working ('put' below)!
    'put {lyx.symbol}': [Key('cmd-m'), lambda m: insert(f"\\{lyx_math_vocab[m.symbol[0]]} "), Key('right space')],
    
    'alex gamma': [Key('ctrl-m'), "\gamma "],
    'daniel gamma': lambda m: lyx_insert("gamma"),
    "test": ["gamma", Key('right')],

    # "matrix <m> by <n>": R(Key("a-x") + Text("math-matrix %(m)s %(n)s") + Key("enter")),

# Non- math things

	'lyx italics': Key('cmd-e'), # Make sure the cmds are the same as in another apps
	'make bold': Key('cmd-b'),

    'view file': Key('cmd-r'),

# Math things

	'secant line': "secant line",

	'tangent line': "tangent line",


	'smath': Key('cmd-m'),

    'lambda': '\lambda ',

    'insert lambdas': '\lambda_1, \lambda_2, ...,\lambda_n ',
    'insert vectors vee': '\mathbf v _1 ,\mathbf v _2, ...,\mathbf v _n ',

    'less [than or] equal': '\leq ',

    'greater [than or] equal': '\geq ',
    'not equal': '\\neq ',


    'times': '\\times',

    'square root': '\sqrt ',

    'left arrow': '\leftarrow ',
    'right arrow': '\\rightarrow ',

    'union': '\cup ',
    'intersect': '\cap ',
    
    'subset': '\subseteq ',
    'proper subset': '\subset ',

    'infinity': '\infty ',

    'function plex': 'f(x)',
    'function near': 'f(n)',

    'function prime': "f'(x)",
    'function double prime': "f''(x)",

    '(approaches | goes to) infinity': '\\rightarrow \infty ',
    '(approaches | goes to) (minus | negative) infinity': '\\rightarrow -\infty ',

    'plex (approaches | goes to) air': 'x\\rightarrow a',



    'function [goes to | approaches] infinity': 'f(x)\\rightarrow \infty ', # may be helpful to have additional verbosity as option, since it can help with internalizing the math
    'function [goes to | approaches] (minus | negative) infinity': 'f(x)\\rightarrow -\infty ',



    'limit': '\\lim ',
    'limit air': '\\lim_x\\rightarrow a ', #can't have more than 1 space at the end if want to remain in math mode
    'limit (plex) infinity': '\\lim_x\\rightarrow \infty  ',
    'limit near infinity': '\\lim_n\\rightarrow \infty  ',
    'limit (plex) (minus | negative) infinity': '\\lim_x\\rightarrow -\infty  ',

    'diff': '\\dfrac d',
    'int': '\\int',

    'frac': '\\frac ',
    'deefrac': '\\dfrac ', #display fraction, which is larger than frac

    'nice frac': '\\nicefrac ',

    'plus minus': '\pm ',

    'begin (abs | absolute)': '\lvert ',

    'end (abs | absolute)': '\\rvert ',

    'begin norm': '\lVert ',
    'end norm': '\\rVert ',

# Logical and function notation

    'wedge': '\\wedge ',
    'exists': '\\exists ',
    'for all': '\\forall ',
    'implies': '\\implies ',

    'if only if': '\iff ',

    'compose': '\circ ',
    
# Trig

	'sine': '\sin ',
	'cosine': '\cos ',
	'tangent': '\tan ',
	'secant': '\sec ',

# Greek letters
	'alpha': '\alpha ',
	'theta': '\\theta ',
	'pie': '\pi ',	
	'gamma': '\\gamma ',
	'delta': '\\delta ',
    'big delta': '\\Delta ',
	'epsilon': '\\varepsilon ',

# Environment shortcuts

    'bullet': Key('ctrl-p i'),
    'number list': Key('ctrl-p n'),
    'vote': Key('ctrl-p q'),  # quote environment  
    'standard': Key('ctrl-p s'),
    #'comment': Key('ctrl-p shift-cmd'),

}

ctx.keymap(keymap)
