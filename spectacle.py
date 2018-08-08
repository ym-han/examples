from talon.voice import Key, press, Str, Context

# Move and resize windows with Spectacle.app

ctx = Context('spectacle')


keymap = {
    'wendy center': Key('cmd-alt-f'),
    'wendy max': Key('cmd-alt-f'),

    'wendy left': Key('ctrl-alt-left'),
    'wendy right': Key('ctrl-alt-right'),

    'wendy half left': Key('alt-cmd-left'),
    'wendy half right': Key('alt-cmd-right'),



    'wendy up': Key('cmd-alt-up'),
    'wendy down': Key('cmd-alt-down'),

    'wendy upper left': Key('cmd-ctrl-left'),
    'wendy lower left': Key('cmd-ctrl-shift-left'),
    'wendy upper right': Key('cmd-ctrl-right'),
    'wendy lower right': Key('cmd-ctrl-shift-right'),

    'wendy next display': Key('cmd-ctrl-alt-right'),
    'wendy previous display': Key('cmd-ctrl-alt-left'),

    'wendy larger': Key('shift-ctrl-alt-right'),
    'wendy smaller': Key('shift-ctrl-alt-left'),

    'wendy undo': Key('cmd-alt-z'),
    'wendy redo': Key('cmd-alt-shift-z'),

}

ctx.keymap(keymap)
