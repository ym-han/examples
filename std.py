# ym's changes:
# =====================
# Sentence --> pithier `line' [but line keeps getting conflated with nine, annoyingly]
# more --> easier for me to pronounce `mod'
# phrase --> write --> oh [since right also used for right arrow]
# exclamation point --> exclamation mark
# added shift-tab
# Added my name (word ym)
# Added commands for comments
# bold for markdown: mark b
# italics: italicize
# increase, decrease font
# k -> kim
# w -> woke
# h -> ham
# m -> met
# f -> fin
# j -> jug
# d -> din
# g -> gig

from talon.voice import Word, Context, Key, Rep, RepPhrase, Str, press
from talon import ctrl, clip
from talon_init import TALON_HOME, TALON_PLUGINS, TALON_USER
import string

alpha_alt = 'air bat cap din each fin gig ham sit jug kim look met near odd pit quest red sun trap urge vest woke box yes zip'.split()
alnum = list(zip(alpha_alt, string.ascii_lowercase)) + [(str(i), str(i)) for i in range(0, 10)]

alpha = {}
alpha.update(dict(alnum))
alpha.update({'ship %s' % word: letter for word, letter in zip(alpha_alt, string.ascii_uppercase)})

alpha.update({'control %s' % k: Key('ctrl-%s' % v) for k, v in alnum})
alpha.update({'command %s' % k: Key('cmd-%s' % v) for k, v in alnum})
alpha.update({'command shift %s' % k: Key('ctrl-shift-%s' % v) for k, v in alnum})
alpha.update({'alt %s' % k: Key('alt-%s' % v) for k, v in alnum})

mapping = {
    'semicolon': ';',
    'new-line': '\n',
    'new-paragraph': '\n\n',
}
punctuation = set('.,-!?')

def parse_word(word):
    word = str(word).lstrip('\\').split('\\', 1)[0]
    word = mapping.get(word, word)
    return word

def join_words(words, sep=' '):
    out = ''
    for i, word in enumerate(words):
        if i > 0 and word not in punctuation:
            out += sep
        out += word
    return out

def parse_words(m):
    return list(map(parse_word, m.dgndictation[0]._words))

def insert(s):
    Str(s)(None)

def text(m):
    insert(join_words(parse_words(m)).lower())

def sentence_text(m):
    text = join_words(parse_words(m)).lower()
    insert(text.capitalize())

def word(m):
    text = join_words(list(map(parse_word, m.dgnwords[0]._words)))
    insert(text.lower())

def surround(by):
    def func(i, word, last):
        if i == 0: word = by + word
        if last: word += by
        return word
    return func

def rot13(i, word, _):
    out = ''
    for c in word.lower():
        if c in string.ascii_lowercase:
            c = chr((((ord(c) - ord('a')) + 13) % 26) + ord('a'))
        out += c
    return out

formatters = {
    'dunder': (True,  lambda i, word, _: '__%s__' % word if i == 0 else word),
    # [commented out coz kept interfering with dictation] 'camel':  (True,  lambda i, word, _: word if i == 0 else word.capitalize()),
    'snake':  (True,  lambda i, word, _: word if i == 0 else '_'+word),
    'smash':  (True,  lambda i, word, _: word),
    # spinal or kebab?
    'kebab':  (True,  lambda i, word, _: word if i == 0 else '-'+word),
    'title':  (False, lambda i, word, _: word.capitalize()),
    'allcaps': (False, lambda i, word, _: word.upper()),
    'dubstring': (False, surround('"')),
    'string': (False, surround("'")),
    'padded': (False, surround(" ")),
    'rot-thirteen':  (False, rot13),
}


def FormatText(m):
    fmt = []
    for w in m._words:
        if isinstance(w, Word):
            fmt.append(w.word)
    try:
        words = parse_words(m)
    except AttributeError:
        with clip.capture() as s:
            press('cmd-c')
        words = s.get().split(' ')
        if not words:
            return

    tmp = []
    spaces = True
    for i, word in enumerate(words):
        word = parse_word(word)
        for name in reversed(fmt):
            smash, func = formatters[name]
            word = func(i, word, i == len(words)-1)
            spaces = spaces and not smash
        tmp.append(word)
    words = tmp

    sep = ' '
    if not spaces:
        sep = ''
    Str(sep.join(words))(None)

ctx = Context('input')

keymap = {}
keymap.update(alpha)
keymap.update({
    'oh <dgndictation> [over]': text,
    'word <dgnwords>': word,

    'line <dgndictation> [over]': sentence_text,
    'comma <dgndictation> [over]': [', ', text],
    'quote <dgndictation> [over]': ["'", text],
    'period <dgndictation> [over]': ['. ', sentence_text],
    'mod <dgndictation> [over]': [' ', text],

    '(%s)+ [<dgndictation>]' % (' | '.join(formatters)): FormatText,

    'tab':  Key('tab'),
    'shift-tab': Key('shift-tab'), 
    'left':  Key('left'),
    'right': Key('right'),
    '(guppy | jeep)': Key('up'),
    'down':  Key('down'),
    
    'delete': Key('backspace'),

    'slap': [Key('cmd-right enter')],
    'enter': Key('enter'),
    'escape': Key('esc'),
    'make question': '?',
    'tilde': '~', 
    '(bang | exclamation mark)': '!',
    'dollar [sign]': '$',
    'downscore': '_',
    '(semi | semicolon)': ';',
    'colon': ':',
    '(square | left square [bracket])': '[', '(rsquare | are square | right square [bracket])': ']',
    '(paren | left paren)': '(', '(rparen | are paren | right paren)': ')',
    '(brace | left brace)': '{', '(rbrace | are brace | right brace)': '}',
    '(angle | left angle | less than)': '<', '(rangle | are angle | right angle | greater than)': '>',

    '(star | asterisk)': '*',
    '(pound | hash [sign] | octo | thorpe | number sign)': '#',
    'percent [sign]': '%',
    'caret': '^',
    'at sign': '@',
    '(and sign | ampersand | amper)': '&',
    'pipe': '|',

    '(dubquote | double quote)': '"',
    'quote': "'",
    'triple quote': "'''",
    '(dot | period)': '.',
    'comma': ',',
    'space': ' ',
    '[forward] slash': '/',
    'backslash': '\\',

    '(dot dot | dotdot)': '..',
    'cd': 'cd ',
    'cd talon home': 'cd {}'.format(TALON_HOME),
    'cd talon user': 'cd {}'.format(TALON_USER),
    'cd talon plugins': 'cd {}'.format(TALON_PLUGINS),

    'run make (durr | dear)': 'mkdir ',
    'run get': 'git ',
    'run get (R M | remove)': 'git rm ',
    'run get add': 'git add ',
    'run get bisect': 'git bisect ',
    'run get branch': 'git branch ',
    'run get checkout': 'git checkout ',
    'run get clone': 'git clone ',
    'run get commit': 'git commit ',
    'run get diff': 'git diff ',
    'run get fetch': 'git fetch ',
    'run get grep': 'git grep ',
    'run get in it': 'git init ',
    'run get log': 'git log ',
    'run get merge': 'git merge ',
    'run get move': 'git mv ',
    'run get pull': 'git pull ',
    'run get push': 'git push ',
    'run get rebase': 'git rebase ',
    'run get reset': 'git reset ',
    'run get show': 'git show ',
    'run get status': 'git status ',
    'run get tag': 'git tag ',
    'run (them | vim)': 'vim ',
    'run L S': 'ls\n',
    'dot pie': '.py',
#    'run make': 'make\n',
#    'run jobs': 'jobs\n',

    'const': 'const ',
    'static': 'static ',
    'tip pent': 'int ',
    'tip char': 'char ',
    'tip byte': 'byte ',
#    'tip pent 64': 'int64_t ',
#    'tip you went 64': 'uint64_t ',
#    'tip pent 32': 'int32_t ',
#    'tip you went 32': 'uint32_t ',
#    'tip pent 16': 'int16_t ',
#    'tip you went 16': 'uint16_t ',
#    'tip pent 8': 'int8_t ',
#    'tip you went 8': 'uint8_t ',
#    'tip size': 'size_t',
    'tip float': 'float ',
    'tip double': 'double ',

    'args': ['()', Key('left')],
    'index': ['[]', Key('left')],
    'block': [' {}', Key('left enter enter up tab')],
    'empty array': '[]',
    'empty dict': '{}',

    'state (def | deaf | deft)': 'def ',
    'state else if': 'elif ',
    'state if': 'if ',
    'state else if': [' else if ()', Key('left')],
    'state while': ['while ()', Key('left')],
    'state for': ['for ()', Key('left')],
    'state for': 'for ',
    'state switch': ['switch ()', Key('left')],
    'state case': ['case \nbreak;', Key('up')],
    'state goto': 'goto ',
    'state import': 'import ',
    'state class': 'class ',

    'state include': '#include ',
    'state include system': ['#include <>', Key('left')],
    'state include local': ['#include ""', Key('left')],
    'state type deaf': 'typedef ',
    'state type deaf struct': ['typedef struct {\n\n};', Key('up'), '\t'],

    'comment see': '// ',
    'comment py': '# ',

# Markdown stuff [ym]
    'begin comment': '<!-- ',
    'end comment': '-->',

    'mark b': '**',

# Non-mark down text editing stuff   
    'make italics': Key('cmd-i'),
    'make bold': Key('cmd-b'),
# To do / add: italicize word to left; italicize word to right; also bolding and strikethru

    'big dash': '---',

    'batick': '`',



    'increase font': Key('cmd-+'),
    'decrease font': Key('cmd--'),




    'word queue': 'queue',
    'word eye': 'eye',
    'word bson': 'bson',
    'word iter': 'iter',
    'word no': 'NULL',
    'word cmd': 'cmd',
    'word dup': 'dup',
    'word streak': ['streq()', Key('left')],
    'word printf': 'printf',
    'word (dickt | dictionary)': 'dict',
    'word shell': 'shell',

#    'word lunixbochs': 'lunixbochs',
    'word YM': 'Yongming',

    'rationalist': 'Rationalist',
    'rationalists': 'Rationalists',

    'word quid': 'quid',

    

    'word talon': 'talon',
    'word angle': 'angle',

    'dunder in it': '__init__',
    'self taught': 'self.',
    'dickt in it': ['{}', Key('left')],
    'list in it': ['[]', Key('left')],
    'string utf8': "'utf8'",
    'state past': 'pass',

    'equals': '=',
    '(minus | dash | hyphen)': '-',
    'plus': '+',
    'arrow': '->',
    'call': '()',
#    'indirect': '&',
#    'dereference': '*',
    '(op equals | assign)': ' = ',
    'op (minus | subtract)': ' - ',
    'op (plus | add)': ' + ',
    'op (times | multiply)': ' * ',
    'op divide': ' / ',
    'op mod': ' % ',
    '[op] (minus | subtract) equals': ' -= ',
    '[op] (plus | add) equals': ' += ',
    '[op] (times | multiply) equals': ' *= ',
    '[op] divide equals': ' /= ',
    '[op] mod equals': ' %= ',

    '(op | is) greater [than]': ' > ',
    '(op | is) less [than]': ' < ',
    '(op | is) equal': ' == ',
    '(op | is) not equal': ' != ',
    '(op | is) greater [than] or equal': ' >= ',
    '(op | is) less [than] or equal': ' <= ',
    '(op (power | exponent) | to the power [of])': ' ** ',
    'op and': ' && ',
    'op or': ' || ',
    '[op] (logical | bitwise) and': ' & ',
    '[op] (logical | bitwise) or': ' | ',
    '(op | logical | bitwise) (ex | exclusive) or': ' ^ ',
    '[(op | logical | bitwise)] (left shift | shift left)': ' << ',
    '[(op | logical | bitwise)] (right shift | shift right)': ' >> ',
    '(op | logical | bitwise) and equals': ' &= ',
    '(op | logical | bitwise) or equals': ' |= ',
#    '(op | logical | bitwise) (ex | exclusive) or equals': ' ^= ',
#    '[(op | logical | bitwise)] (left shift | shift left) equals': ' <<= ',
#    '[(op | logical | bitwise)] (right shift | shift right) equals': ' >>= ',

    'shebang bash': '#!/bin/bash -u\n',

    'new window': Key('cmd-n'),
    'next window': Key('cmd-`'),
    'last window': Key('cmd-shift-`'),
    'next app': Key('cmd-tab'),
    'last app': Key('cmd-shift-tab'),
    'next tab': Key('ctrl-tab'),
    'new tab': Key('cmd-t'),
    'last tab': Key('ctrl-shift-tab'),

    'next space': Key('cmd-alt-ctrl-right'),
    'last space': Key('cmd-alt-ctrl-left'),

    'scroll down': [Key('down')] * 30,
    'scroll up': [Key('up')] * 30,
})
ctx.keymap(keymap)