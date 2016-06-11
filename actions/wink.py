from .base import Action
from config import WINK_CLIENT_ID, WINK_CLIENT_SECRET, WINK_REFRESH_TOKEN

import pywink
pywink.set_wink_credentials(
    WINK_CLIENT_ID, WINK_CLIENT_SECRET, WINK_REFRESH_TOKEN)


class WinkBulbAction(Action):
    def process(self, bulb):
        for b in pywink.get_bulbs():
            if b.name() == bulb:
                print('turning {0} {1}'.format(
                    bulb, 'off' if b.state() else 'on'))
                b.set_state(not b.state())
                return


class WinkAllBulbAction(Action):
    def process(self, bulbs_on):
        for b in pywink.get_bulbs():
            if b.state() != bulbs_on:
                print('turning {0} {1}'.format(
                    b.name(), 'on' if bulbs_on else 'off'))
                b.set_state(bulbs_on)
