"""
Description:
Restful API testing

Features:
    - html report

Run:
python3 -m pytest -sv --html report.html

Python version: 3.7 or above

"""
import logging
import requests
import json
import os
import ast
import inspect
import sys

if sys.version_info < (3, 7):
    raise Exception("Requires Python 3.7 or above.")

LOG_LEVEL = logging.INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# root_path is parent folder of Scripts folder (one level up)
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# %(levelname)7s to align 7 bytes to right, %(levelname)-7s to left.
common_formatter = logging.Formatter('%(asctime)s [%(levelname)-7s][ln-%(lineno)-3d]: %(message)s',
                                     datefmt='%Y-%m-%d %I:%M:%S')


# Note: To create multiple log files, must use different logger name.
def setup_logger(log_file, level=logging.INFO, name='', formatter=common_formatter):
    """Function setup as many loggers as you want."""
    handler = logging.FileHandler(log_file, mode='w')  # default mode is append
    # Or use a rotating file handler
    # handler = RotatingFileHandler(log_file,maxBytes=1024, backupCount=5)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# default debug logger
debug_log_filename = root_path + os.sep + 'Logs' + os.sep + 'debug.log'
log = setup_logger(debug_log_filename, LOG_LEVEL, 'log')

# logger for API outputs
api_formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
api_outputs_filename = root_path + os.sep + 'Logs' + os.sep + 'api_outputs.log'
log_api = setup_logger(api_outputs_filename, LOG_LEVEL, 'log_api', formatter=api_formatter)


# pretty print Restful request to API log
# argument is request object
def pretty_print_request(request):
    """
    Pay attention at the formatting used in this function because it is programmed to be pretty printed and may differ from the actual request.
    """
    if request is not None:
        log_api.info('{}\n{}\n\n{}\n\n{}\n'.format(
            '-----------Request----------->',
            request.method + ' ' + request.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
            request.body)
        )


# pretty print Restful request to API log
# argument is response object
def pretty_print_response(response):
    if response.text:
        log_api.info('{}\n{}\n\n{}\n\n{}\n'.format(
            '<-----------Response-----------',
            'Status code:' + str(response.status_code),
            '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
            response.text
        ))


# argument is request object
# display body in json format explicitly with expected indent. Actually most of the time it is not very necessary because body is formatted in pretty print way.
def pretty_print_request_json(request):
    if request is not None:
        log_api.info('{}\n{}\n\n{}\n\n{}\n'.format(
            '-----------Request----------->',
            request.method + ' ' + request.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
            json.dumps(ast.literal_eval(request.body), indent=4))
        )


# argument is response object
# display body in json format explicitly with expected indent. Actually most of the time it is not very necessary because body is formatted in pretty print way.
def pretty_print_response_json(response):
    if response.text:
        log_api.info('{}\n{}\n\n{}\n\n{}\n'.format(
            '<-----------Response-----------',
            'Status code:' + str(response.status_code),
            '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
            json.dumps(response.json(), indent=4)
        ))

api_url_base = 'http://localhost:5000/v1/'
headers = {'Content-Type': 'application/json'}


def get_products_api():
    response = requests.get(api_url_base + "products", headers=headers)
    pretty_print_request(response.request)
    pretty_print_response_json(response)
    return response


def get_product_api(product_code):
    response = requests.get(api_url_base + "product/" + product_code, headers=headers)
    pretty_print_request(response.request)
    pretty_print_response_json(response)
    return response


def put_product_api(product_code, product_name, product_price):
    payload = {'name': product_name, 'price': product_price}
    response = requests.put(api_url_base + "product/" + product_code, headers=headers, data=json.dumps(payload))
    pretty_print_request(response.request)
    pretty_print_response_json(response)
    return response


def post_product_api(product_name, product_price):
    payload = {'name': product_name, 'price': product_price}
    response = requests.post(api_url_base + "product", headers=headers, data=json.dumps(payload))
    pretty_print_request(response.request)
    pretty_print_response_json(response)
    return response


def delete_product_api(product_code):
    response = requests.delete(api_url_base + "product/" + product_code, headers=headers)
    pretty_print_request(response.request)
    pretty_print_response_json(response)
    return response

def delete_all():
    response = requests.get(api_url_base + "products", headers=headers)
    products = json.loads(response.content.decode('utf-8'))
    if products is not None:
        for product in products:
            delete_product_api(str(product['id']))
    else:
        print('[!] Request Failed')

class TestProductsAPI:
    """
    Test products API.
    """

    def setup_class(cls):
        log.debug('To clear test data.')
        delete_all()

    def test_products_api_result(self):
        log.info('Calling %s.' % inspect.stack()[0][3])

        resp = get_products_api()
        assert resp.status_code == 200

        post_product_api("Samsung", 899.99)
        post_product_api("Apple", 1199.99)
        post_product_api("Huawei", 500)

        resp = get_products_api()
        assert resp.status_code == 200

        products = json.loads(resp.content.decode('utf-8'))
        if products is not None:
            assert len(products) == 3
        else:
            print('[!] Request Failed')
        log.info('Test %s passed.' % inspect.stack()[0][3])

    def test_product_put_result(self):
        log.info('Calling %s.' % inspect.stack()[0][3])

        resp = put_product_api("3", "Samsung Galaxy", 799.99)
        assert(resp.status_code == 200)

        resp = put_product_api("100", "Samsung Galaxy", 799.99)
        assert(resp.status_code == 404)

        log.info('Test %s passed.' % inspect.stack()[0][3])

    def test_product_post_result(self):
        log.info('Calling %s.' % inspect.stack()[0][3])

        resp = post_product_api("LG", 999.99)
        assert (resp.status_code == 200)

        log.info('Test %s passed.' % inspect.stack()[0][3])

    def test_product_get_result(self):
        log.info('Calling %s.' % inspect.stack()[0][3])

        resp = get_product_api("4")
        assert(resp.status_code == 200)
        product = json.loads(resp.content.decode('utf-8'))
        if product is not None:
            assert(product['id'] == 4)
            assert(product['name'] == "LG")
            assert(product['price'] == "999.99")
        else:
            print('[!] Request Failed')

        log.info('Test %s passed.' % inspect.stack()[0][3])

    def test_product_delete_result(self):
        log.info('Calling %s.' % inspect.stack()[0][3])

        resp = delete_product_api("2")
        assert(resp.status_code == 200)
        resp = get_product_api("2")
        assert(resp.status_code == 404)
        resp = delete_product_api("2")
        assert(resp.status_code == 404)

        log.info('Test %s passed.' % inspect.stack()[0][3])
