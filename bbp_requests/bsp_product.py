import json
import urllib.error
import urllib.request
from urllib.parse import urlencode

BBP_HOST = 'https://bbp.ntsomz.ru'


class Additional_color_representations:
    def __init__(self, additional_colors):
        self.colors = additional_colors


class Tile_services:
    def __init__(self, productType, color_representation, main_url, min_zoom, max_zoom, bbox, additional_colors):
        self.productType = productType
        self.color_representation = color_representation
        self.main_url = main_url
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.bbox = bbox
        self.additional_colors = Additional_color_representations(additional_colors)


class Mosaic:
    def __init__(self, date_range, mosaic_id, region_id, resolution, sensors_group_id, products, productType, color_representation, main_url, min_zoom, max_zoom, bbox, additional_colors):
        self.date_range = date_range
        self.mosaic_id = mosaic_id
        self.region_id = region_id
        self.resolution = resolution
        self.sensors_group_id = sensors_group_id
        self.products = products
        self.tile_services = Tile_services(productType, color_representation, main_url, min_zoom, max_zoom, bbox, additional_colors)


def _send_http_request(req):
    for try_n in range(3):
        print('_send_http_request try: ', try_n)
        try:
            with urllib.request.urlopen(req) as open_req:
                return open_req.read()
        except urllib.error.HTTPError as err:
            print('Send request error:', err)
    return None


def sendBspRequest(apiKey):
    req_action = '/api/v1/resources/mosaics'
    headers = {'Content-Type': 'application/json'}
    keyvalues = {'api_key': apiKey}
    encoded_args = urlencode(keyvalues)

    search_json = {
        "page": 1,
        "items": 10
    }

    print('Request', BBP_HOST + req_action + '?' + encoded_args)
    req_body = json.dumps(search_json).encode('utf-8')
    print('Request body: ', req_body)
    req = urllib.request.Request(BBP_HOST + req_action + '?' + encoded_args, method='POST', headers=headers, data=req_body)
    resp = _send_http_request(req)

    resp_js_cont = None
    if resp:
        resp_js_cont = json.loads(resp.decode('utf-8'))
        print('Response', resp_js_cont)
    else:
        return None

    '''
    response = resp_js_cont
    try:
        last_page = response['last_page']
    except TypeError:
        last_page = 0

    objectsList = []
    for page_num in range(1, last_page + 1):
        search_json['page'] = page_num
        req_body = json.dumps(search_json).encode('utf-8')
        print(req_body)
        page_req = urllib.request.Request(BBP_HOST + req_action + '?' + encoded_args, method='POST', headers=headers, data=req_body)
        resp = _send_http_request(page_req)
        resp_js_cont = None
        print('Response', resp)

        if resp:
            resp_js_cont = json.loads(resp.decode('utf-8'))

        # Write in file for tests
        # with open('test{num}.json'.format(num=page_num), 'a') as testFile:
        #     json.dump(resp_js_cont, testFile, indent=4)
    '''

    objectsList = []
    jsonBody = resp_js_cont
    for BSP in jsonBody['result']:
        date_range = BSP['date_range']
        mosaic_id = BSP['mosaic_id']
        region_id = BSP['region_id']
        resolution = BSP['resolution']
        sensors_group_id = BSP['sensors_group_id']
        products = BSP['products']

        for productType in BSP['tile_services']:

            productContent = BSP['tile_services'][productType]

            main_color_representation = productContent['color_representation']
            main_color_url = productContent['url']
            min_zoom = productContent['min_zoom']
            max_zoom = productContent['max_zoom']
            bbox = productContent['bbox']

            additionalColorsList = {}
            try:
                for additional_colors in productContent['additional_color_representations']:
                    additional_color_representation = additional_colors['color_representation']
                    additional_color_url = additional_colors['url']

                    additionalColorsList[additional_color_representation] = additional_color_url
            except TypeError:
                additionalColorsList = None

            object = Mosaic(date_range, mosaic_id, region_id, resolution, sensors_group_id,
                            products, productType, main_color_representation, main_color_url, min_zoom,
                            max_zoom, bbox, additionalColorsList)
            objectsList.append(object)

    for obj in objectsList:
        print(obj.date_range, obj.mosaic_id, obj.products, obj.region_id, obj.resolution, obj.sensors_group_id,
              obj.tile_services.productType, obj.tile_services.main_url, obj.tile_services.color_representation,
              obj.tile_services.max_zoom, obj.tile_services.min_zoom, obj.tile_services.bbox,
              obj.tile_services.additional_colors.colors)

    if len(objectsList) != 0:
        return objectsList
    else:
        return None


def main():
    testKey = ''
    sendBspRequest(testKey)


if __name__ == '__main__':
    main()