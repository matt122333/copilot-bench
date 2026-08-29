import base64, json, hmac, hashlib
def _b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def verify(auth_header, secret):
    try:
        token = auth_header.split(' ')[1]
        parts = token.split('.')
        if len(parts) != 3:
            return False
        header, payload, sig = parts
        # only HMAC allowed
        hdr = json.loads(base64.urlsafe_b64decode(header + '=='))
        if hdr.get('alg') != 'HS256':
            return False
        msg = (header + '.' + payload).encode()
        expected = _b64(hmac.new(secret.encode(), msg, hashlib.sha256).digest())
        return hmac.compare_digest(expected, sig)
    except Exception:
        return False