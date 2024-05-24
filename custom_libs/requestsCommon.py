from bs4 import BeautifulSoup as bS
import requests


def get_soup_from_html_content(html_content):
    return bS(html_content, 'html.parser')


def basic_request(url, request_type="GET", timeout=5, **kwargs):
    request_type = request_type
    headers = {}
    params = {}
    if 'type' in kwargs:
        request_type = kwargs['type']
    if 'headers' in kwargs:
        headers = kwargs['headers']
    if 'params' in kwargs:
        params = kwargs['params']

    if request_type == "GET":
        return requests.request(request_type, url, headers=headers, params=params, timeout=timeout)
    else:
        return requests.post(url, headers=headers, data=params, timeout=timeout)






