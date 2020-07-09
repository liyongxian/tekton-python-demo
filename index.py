import json
import redis

def handler(event, context):
    evt = json.loads(event)
    host=(evt['host'])
    v=evt['value']
    k=evt['key']
    r = redis.Redis(host=host, port=6379, decode_responses=True)
    r.set(k, v)
    return 'end'
