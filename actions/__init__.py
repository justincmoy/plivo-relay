from config import ACTIONS
import importlib


def action_handler(user, action):
    action = ACTIONS[action]
    c = importlib.import_module(action['module'])
    c = getattr(c, action['class'])(user)
    c.process(*action.get('args', []), **action.get('kwargs', {}))
