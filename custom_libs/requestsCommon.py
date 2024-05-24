from bs4 import BeautifulSoup as bS
import requests
from fake_useragent import UserAgent    # https://pypi.org/project/fake-useragent/#description


def get_soup_from_html_content(html_content):
    return bS(html_content, 'html.parser')


def basic_request(url, add_user_agent=False, request_type="GET", timeout=5, **kwargs):
    request_type = request_type
    headers = {}
    params = {}
    proxies = {}
    if 'type' in kwargs:
        request_type = kwargs['type']
    if 'headers' in kwargs:
        headers = kwargs['headers']
    if 'params' in kwargs:
        params = kwargs['params']
    if 'proxies' in kwargs:
        proxies = kwargs['proxies']
    if add_user_agent:
        random_agent = _add_user_agent_to_header()
        headers["User-Agent"] = random_agent

    if request_type == "GET":
        return requests.request(request_type, url, headers=headers, params=params, proxies=proxies, timeout=timeout)
    else:
        return requests.post(url, headers=headers, data=params, proxies=proxies, timeout=timeout)


def _add_user_agent_to_header():
    ua = UserAgent(fallback="chrome")
    return ua.random




