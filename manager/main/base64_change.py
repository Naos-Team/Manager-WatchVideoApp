import base64


def encode_Str(values):
    return base64.b64encode(values.encode('ascii')).decode('ascii')
    
def decode_Str(values):
    return base64.b64decode(values).decode('ascii')