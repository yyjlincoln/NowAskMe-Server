import requests
import json
import time


def GenerateLargeRequests(n):
    req = []
    for x in range(n):
        req.append({
            'route': '/auth/check_scope',
            'data': {
                'uuid': 'largerequesttest',
                'token': 'largerequesttest'
            }
        })

    return json.dumps(req)


for x in range(10, 300, 10):
    t = time.time()
    req = GenerateLargeRequests(x)
    data = requests.post('https://apis.nowask.me/batch', data={
        'batch': req
    })
    print(data.text, data.reason)
    print('Request of size '+str(len(req)) + '(' + str(x) +
          ' requests) took '+str(time.time()-t)+' seconds.')
