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

with open('testreport.csv','w') as f:
    f.write('Number of requests,Request Size (kb),Response Time (s),Status\n')
    for x in range(10, 1000, 10):
        t = time.time()
        req = GenerateLargeRequests(x)
        data = requests.post('https://apis.nowask.me/batch', data={
            'batch': req
        })
        print('Testing for x =',x)
        f.write(f"{str(x)},{str(len(req))},{str(time.time()-t)},{'Success (200)' if data.status_code==200 else 'Failed ('+str(data.status_code)}"+'\n')

    # if data.status_code==200:
    #     print('Request of size '+str(len(req)) + '(' + str(x) +
    #           ' requests) took '+str(time.time()-t)+' seconds.')
    # else:
    #     print('Request of size '+str(len(req)) + '(' + str(x) +
    #           ' requests) took '+str(time.time()-t)+' seconds and failed.')
        
