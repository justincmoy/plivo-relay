from config import ACTIONS
import importlib


def action_handler(user, action):
    actions = ACTIONS[action]
    if actions is str:
        actions = [actions]

    for action in actions:
        c = importlib.import_module(action['module'])
        c = getattr(c, action['class'])(user)
        c.process(*action.get('args', []), **action.get('kwargs', {}))
