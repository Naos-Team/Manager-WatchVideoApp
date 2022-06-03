import requests
import json

SERVER_URL = "https://musicfreeworld.com/public/naosteam/watchvideoapp/"
UPLOAD_VIDEO = "https://musicfreeworld.com/public/naosteam/watchvideoapp/uploadImage.php"
IMAGE_DIR = "https://musicfreeworld.com/public/naosteam/watchvideoapp/image/"

def executePostRequest(param):
    data = {
        'data': json.dumps(param)
    }
    res = requests.post(SERVER_URL, data=data)
    return json.loads(res.content)
