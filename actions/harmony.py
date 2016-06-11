from .base import Action
from config import HARMONY_IP, HARMONY_PORT, HARMONY_TOKEN

from pyharmony import client as harmony_client


class HarmonyActivityAction(Action):
    def process(self, activity):
        client = harmony_client.create_and_connect_client(
            HARMONY_IP, HARMONY_PORT, HARMONY_TOKEN)

        for a in client.get_config()['activity']:
            if a['label'] == activity:
                print('starting activity {0}'.format(activity))
                client.start_activity(a['id'])

        client.disconnect(send_close=True)
