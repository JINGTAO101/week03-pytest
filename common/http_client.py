#define timeout as 10 seconds
import requests

def get(url,timeout=10,**kwargs):
    return requests.get(url,timeout=timeout,**kwargs)

def post_json(url,json,timeout=10,**kwargs):
    return requests.post(url,json=json,timeout=timeout,**kwargs)
