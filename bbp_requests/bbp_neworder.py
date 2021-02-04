import json
import urllib.error
import urllib.request
from urllib.parse import urlencode

BBP_HOST = 'https://bbp.ntsomz.ru'


class Order:
    def __init__(self, completed, composites, created, download, expires, id, pointer, products, responsive_id, source, state):
        self.completed = completed
        self.composites = composites
        self.created = created
        self.download = download
        self.expires = expires
        self.id = id
        self.pointer = pointer
        self.products = products
        self.responsive_id = responsive_id
        self.source = source
        self.state = state


def _send_http_request(req):
    for try_n in range(3):
        print('_send_http_request try: ', try_n)
        try:
            with urllib.request.urlopen(req) as open_req:
                return open_req.read()
        except urllib.error.HTTPError as err:
            print('Send request error:', err)
    return None


def sendBspRequest(apiKey, state:list):
    req_action = '/api/v1/resources/orders'
    keyvalues = {'api_key': apiKey}
    encoded_args = urlencode(keyvalues)

    search_json = {
        "page": 1,
        "items": 100
    }

    states = '&state='.join(state)

    req_body = urlencode(search_json)
    print('Request', BBP_HOST + req_action + '?' + encoded_args + '&' + req_body + '&state=' + states)
    req = urllib.request.Request(BBP_HOST + req_action + '?' + encoded_args + '&' + req_body + '&state=' + states, method='GET')
    resp = _send_http_request(req)

    resp_js_cont = None
    if resp:
        resp_js_cont = json.loads(resp.decode('utf-8'))
        print('Response', resp_js_cont)
    else:
        return None

    response = resp_js_cont
    try:
        last_page = response['last_page']
    except TypeError:
        last_page = 0
    print("Last_page:", last_page)

    objectsList = []
    for page_num in range(1, last_page + 1):
        search_json['page'] = page_num
        req_body = urlencode(search_json)  # json.dumps(search_json).encode('utf-8')
        print('Request', BBP_HOST + req_action + '?' + encoded_args + '&' + req_body + '&state=' + states)
        page_req = urllib.request.Request(BBP_HOST + req_action + '?' + encoded_args + '&' + req_body + '&state=' + states, method='GET')
        resp = _send_http_request(page_req)
        resp_js_cont = None
        print('Response', resp)

        if resp:
            resp_js_cont = json.loads(resp.decode('utf-8'))

        jsonBody = resp_js_cont
        for BSP in jsonBody['result']:

            completed = BSP['completed']
            composites = BSP['composites']
            created = BSP['created']
            download = BSP['download']
            expires = BSP['expires']
            id = BSP['id']
            pointer = BSP['pointer']
            products = BSP['products']
            responsive_id = BSP['responsive_id']
            source = BSP['source']
            state = BSP['state']
            # tile_services = BSP['tile_services']

            object = Order(completed, composites, created, download, expires, id, pointer, products, responsive_id, source, state)
            objectsList.append(object)

    for obj in objectsList:
        print('{0}, {1}'.format(obj.products, obj.expires))

    if len(objectsList) != 0:
        return objectsList
    else:
        return None


def main():
    testKey = ''
    sendBspRequest(testKey, ['expired'])


if __name__ == '__main__':
    main()