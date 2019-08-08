from talon.engine import engine

def grammar_enable(grammar):
    kwargs = {'enabled': True}
    if grammar.name == 'talon':
        kwargs['priority'] = 1
    engine.grammar_update(grammar, **kwargs)
engine.grammar_enable = grammar_enable