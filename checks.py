from config import PLIVO_AUTH_TOKEN, PLIVO_ALLOWED_NUMBERS
from hashlib import sha1
import base64
import hmac


class CheckException(Exception):
    pass


def check_plivo_signature(uri, form, headers):
    for k, v in sorted(form.items()):
        uri += k + v
    uri = uri.encode('utf-8')
    s = base64.encodestring(
        hmac.new(PLIVO_AUTH_TOKEN, uri, sha1).digest()).strip()
    signature = headers.get('X-Plivo-Signature')
    if s.decode() != signature:
        raise CheckException('plivo signature check failed')


def check_plivo_allowed_numbers(number):
    if number not in PLIVO_ALLOWED_NUMBERS:
        raise CheckException('number {} not in allowed numbers: {}'.format(
            number, PLIVO_ALLOWED_NUMBERS))
