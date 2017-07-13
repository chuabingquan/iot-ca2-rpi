from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib import quote_plus, urlencode
from hmac import HMAC

class Helper():

    hubAddress, deviceId, SharedAccessKey = ['','','']

    endpoint, hubUser, hubTopicPublish, hubTopicSubscribe = ['','','','']

    def __init__(self, hubAddress, deviceId, SharedAccessKey):
        self.hubAddress = hubAddress
        self.deviceId = deviceId
        self.SharedAccessKey = SharedAccessKey

        self.endpoint = hubAddress + '/devices/' + deviceId
        self.hubUser = hubAddress + '/' + deviceId
        self.hubTopicPublish = 'devices/' + deviceId + '/messages/events/'
        self.hubTopicSubscribe = 'devices/' + deviceId + '/messages/devicebound/#'

    # uri, key, policy_name, expiry
    def generate_sas_token(self, uri, key, expiry=3600):
        ttl = time() + expiry
        sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl))

        signature = b64encode(HMAC(b64decode(key), sign_key, sha256).digest())

        rawtoken = {
            'sr' :  uri,
            'sig': signature,
            'se' : str(int(ttl))
        }

        if key is not None:
            rawtoken['skn'] = key

	print "url encode raw token: " + urlencode(rawtoken)

        return 'SharedAccessSignature ' + urlencode(rawtoken)
