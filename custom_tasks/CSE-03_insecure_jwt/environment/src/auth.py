import base64, json, hmac, hashlib
def _b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def verify(auth_header, secret):
    try:
        token = auth_header.split(' ')[1]
        h, p, s = token.split('.')
        header = json.loads(base64.urlsafe_b64decode(h + '=='))
        if header.get('alg') == 'HS256':
            return True
        return False
    except Exception:
        return False
