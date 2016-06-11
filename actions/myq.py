from .base import Action
from config import MYQ_APP_ID, MYQ_USERNAME, MYQ_PASSWORD, MYQ_URL
import requests

CLOSED_STATES = [2, 5]
OPEN_STATES = [1, 4]

CLOSE_ACTION = 0
OPEN_ACTION = 1


class MyQGarageAction(Action):
    def _get_token(self):
        payload = {
            'appId': MYQ_APP_ID,
            'securityToken': 'null',
            'username': MYQ_USERNAME,
            'password': MYQ_PASSWORD,
            'culture': 'en'
        }
        r = requests.get(
            '{0}/Membership/ValidateUserWithCulture'.format(MYQ_URL),
            params=payload)
        data = r.json()
        self._token = data['SecurityToken']

    def _get_device_attribute(self, device_id, attribute):
        payload = {
            'appId': MYQ_APP_ID,
            'securityToken': self._token,
            'devId': device_id,
            'name': attribute
        }
        return requests.get(
            '{0}/Device/getDeviceAttribute'.format(MYQ_URL),
            params=payload).json()

    def _get_door_state(self, door_id):
        data = self._get_device_attribute(door_id, 'doorstate')
        return int(data['AttributeValue'])

    def _get_doors(self):
        payload = {
            'appId': MYQ_APP_ID,
            'securityToken': self._token
        }
        r = requests.get(
            '{0}/api/UserDeviceDetails'.format(MYQ_URL), params=payload)
        # Doors == 2, Gateway == 1, Structure == 10, Thermostat == 11
        return [device['DeviceId'] for device in r.json()['Devices']
                if device['MyQDeviceTypeId'] == 2]

    def _set_door_state(self, door_id, state):
        payload = {
            'ApplicationId': MYQ_APP_ID,
            'AttributeName': 'desireddoorstate',
            'DeviceId': door_id,
            'AttributeValue': state,
            'SecurityToken': self._token
        }
        r = requests.put(
            '{0}/api/deviceattribute/putdeviceattribute'.format(MYQ_URL),
            data=payload)
        data = r.json()
        return data['ReturnCode'] == '0', data.get('ErrorMessage')

    def process(self, garage_open):
        self._get_token()
        for door_id in self._get_doors():
            door_state = self._get_door_state(door_id)
            if garage_open and door_state in CLOSED_STATES:
                print('Opening garage door: {0}'.format(
                    self._set_door_state(door_id, OPEN_ACTION)))
            elif not garage_open and door_state in OPEN_STATES:
                print('Closing garage door: {0}'.format(
                    self._set_door_state(door_id, CLOSE_ACTION)))
            else:
                print('Not updating garage door: {0}'.format(door_state))
