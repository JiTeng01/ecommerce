import base64
import hashlib
import json
import uuid
import string


def base64_encode(code_string, is_encode=True):
    if is_encode:
        code_string = code_string.encode(encoding='utf-8')
    encode_string = base64.b64encode(code_string)
    return encode_string


def base64_decode(code_string):
    code_string = code_string.encode(encoding="utf-8")
    decode_string = base64.b64decode(code_string)
    return decode_string.decode()


def base64_decode_raw(code_string):
    return base64.b64decode(code_string)


def sha256_encode(code_string):
    return hashlib.sha256(code_string.encode(encoding="utf-8")).hexdigest()


def md5_encode(code_string):
    return hashlib.md5(code_string.encode(encoding="utf-8")).hexdigest()


def json_encode(code_string):
    return json.dumps(code_string)


def json_decode(code_string):
    return json.loads(code_string)


def generate_unique_code():
    letters = list(string.digits + string.ascii_letters)
    unique_id, unique_code = str(uuid.uuid4()).replace("-", ""), []
    for i in range(0, 8):
        start, end = i * 4, i * 4 + 4
        hex_value = int(unique_id[start:end], 16)
        unique_code.append(letters[hex_value % 62])
    return "".join(unique_code)