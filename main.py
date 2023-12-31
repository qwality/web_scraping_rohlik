from playwright.sync_api import sync_playwright
# from playwright.async_api import async_playwright

from bs4 import BeautifulSoup, PageElement

from dotenv import load_dotenv
import os

load_dotenv()

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PIN')

print(LOGIN, PASSWORD, os.getenv('DEV'))

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    context.add_cookies([
        {
            'name': 'cp_courier_hash',
            'value': '720ac501f6958af167035d266736f44f',
            'domain': 'couriers-portal.rohlik.cz',
            'path': '/cz'
        },
        {
            'name': 'cp_courier_id',
            'value': LOGIN,
            'domain': 'couriers-portal.rohlik.cz',
            'path': '/cz'
        }
    ])
    page = context.new_page()
    # page.goto("https://couriers-portal.rohlik.cz/cz/")
    page.goto('https://couriers-portal.rohlik.cz/cz/?p=dashboard')

    for cookie in context.cookies():
        match cookie:
            case {'name': 'cp_courier_id', **rest}:
                cp_courier_id = cookie['value']
            case {'name': 'cp_courier_hash', **rest}:
                cp_courier_hash = cookie['value']

    print(cp_courier_id, cp_courier_hash)

    soup = BeautifulSoup(page.content(), 'html.parser')

    # def get_inner_html(element: PageElement):
    #     return element.

    c = list(map(lambda e: e.text, soup.find_all('div', class_='dashboard_next_block')))
    print(c)

    # cp_courier_id = list(filter(lambda cookie: cookie['name'] == 'cp_courier_id',context.cookies()))[0]['value']
    # cp_courier_hash = list(filter(lambda cookie: cookie['name'] == 'cp_courier_hash',context.cookies()))[0]['value']

    # html = page.query_selector_all('.dashboard_next_block')[1]

    # innerHTML = page.evaluate('(element) => element.innerText', html)

    # print(innerHTML)
    # page.fill(".login_field > *:first-child", LOGIN)
    # page.fill(".login_field:nth-child(2) > *:first-child", PASSWORD)
    # page.click(".login_button")