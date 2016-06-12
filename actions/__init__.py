from config import ACTIONS
import importlib


def action_handler(user, action):
    actions = ACTIONS[action]
    if type(actions) is not list:
        actions = [actions]

    output = []

    for action in actions:
        c = importlib.import_module(action['module'])
        c = getattr(c, action['class'])(user, output)
        c.process(*action.get('args', []), **action.get('kwargs', {}))

        output = c.output
