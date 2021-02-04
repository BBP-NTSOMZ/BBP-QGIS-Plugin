import json
import urllib.error
import urllib.request
from urllib.parse import urlencode

BBP_HOST = 'https://bbp.ntsomz.ru'


def _send_http_request(req):
    for try_n in range(3):
        print('_send_http_request try: ', try_n)
        try:
            with urllib.request.urlopen(req) as open_req:
                return open_req.read()
        except urllib.error.HTTPError as err:
            print('Send request error:', err)
    return None


def sendReOrderRequest(apiKey, req_json):
    req_action = '/api/v1/resources/orders'
    headers = {'Content-Type': 'application/json'}
    keyvalues = {'api_key': apiKey}
    encoded_args = urlencode(keyvalues)

    print('Request', BBP_HOST + req_action + '?' + encoded_args)
    req_body = json.dumps(req_json).encode('utf-8')
    print('Request body: ', req_body)

    req = urllib.request.Request(BBP_HOST + req_action + '?' + encoded_args, method='POST', headers=headers, data=req_body)
    resp = _send_http_request(req)

    resp_js_cont = None
    if resp:
        resp_js_cont = json.loads(resp.decode('utf-8'))
        print('Response', resp_js_cont)
    else:
        return None

    return resp_js_cont


def main():
    testKey = ''
    js = {"pointer": "My-App", "products": {'MM22_MSUTM101_20191209T101031_11900500': {'OSAVI': None}}}
    sendReOrderRequest(testKey, js)


if __name__ == '__main__':
    main()









