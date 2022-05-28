from Constant import SERVER_URL
import requests
import json

postObj = {
    'method_name': 'LOAD_SEARCH_VIDEO',
    'search_text': 'moon',
    'page': 0,
    'step': 5
}

data = {
    'data': json.dumps(postObj)
}

res = requests.post(SERVER_URL, data=data)

return_object = json.loads(res.content)

status = return_object['status']
search_list = return_object['search']

print(search_list[3]['vid_time'])