import hmac
import hashlib
import json

class HmacEncoderDecoder:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def encode_data(self, data):
        # Serialize data to JSON
        data_json = json.dumps(data, sort_keys=True).encode('utf-8')
        # Generate HMAC-SHA256 digest
        digest = hmac.new(self.secret_key.encode('utf-8'), data_json, hashlib.sha256).hexdigest()
        # Return encoded data and digest
        return {'data': data, 'digest': digest}

    def decode_data(self, encoded_data):
        # Extract data and digest from encoded data
        data = encoded_data['data']
        received_digest = encoded_data['digest']
        # Serialize data to JSON
        data_json = json.dumps(data, sort_keys=True).encode('utf-8')
        # Generate HMAC-SHA256 digest using the received data and secret key
        computed_digest = hmac.new(self.secret_key.encode('utf-8'), data_json, hashlib.sha256).hexdigest()
        # Verify if the computed digest matches the received digest
        if hmac.compare_digest(computed_digest, received_digest):
            # If the digests match, return the decoded data
            return data
        else:
            # If the digests do not match, raise an error
            raise ValueError('Digest verification failed')
