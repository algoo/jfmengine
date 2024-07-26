import base64

def base64encode(value):
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')