import srp
import binascii
import base64
import hashlib
import hmac
import datetime as dt

def get_secret_hash(username, clientId, clientSecret):
    msg = username + clientId
    dig = hmac.new(str(clientSecret).encode('utf-8'), msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def generate_srp(username, password):
    srp_user = srp.User(username, password)
    _, srp_a_bytes = srp_user.start_authentication()
    response = "".join(str(c) for c in srp_a_bytes)
    return response

def process_challenge(salt, srp_b, secret_block, username, password, user_pool_id):
    srp_user = srp.User(username, password)
    secret_block_bytes = base64.standard_b64decode(secret_block)
    secret_block_hex = "".join(str(c) for c in secret_block_bytes)
    salt_bytes = binascii.unhexlify(salt)
    srp_bytes = binascii.unhexlify(srp_b)
    process =  srp_user.process_challenge(salt_bytes, srp_bytes)
    timestamp = dt.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
    hmac_obj = hmac.new(process, digestmod=hashlib.sha256)
    hmac_obj.update(user_pool_id.split('_')[1].encode('utf-8'))
    hmac_obj.update(secret_block_bytes)
    hmac_obj.update(timestamp.encode('utf-8'))
    response = {
        "TIMESTAMP": timestamp,
        "USERNAME": username,
        "PASSWORD_CLAIM_SECRET_BLOCK": secret_block_hex,
        "PASSWORD_CLAIM_SIGNATURE": hmac_obj.hexdigest()
    }
    return response