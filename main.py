from playwright.sync_api import sync_playwright
# from playwright.async_api import async_playwright

LOGIN = "14963"
PASSWORD = "298753"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=0)
    context = browser.new_context()
    context.add_cookies([
        {
            'name': 'cp_courier_hash',
            'value': 'f3521e17a27e732e6a6daba38c10920f',
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
    page.goto('https://couriers-portal.rohlik.cz/cz/?p=blocks')
    cp_courier_id = list(filter(lambda cookie: cookie['name'] == 'cp_courier_id',context.cookies()))[0]['value']
    cp_courier_hash = list(filter(lambda cookie: cookie['name'] == 'cp_courier_hash',context.cookies()))[0]['value']
    print(cp_courier_id, cp_courier_hash)
    # page.fill(".login_field > *:first-child", LOGIN)
    # page.fill(".login_field:nth-child(2) > *:first-child", PASSWORD)
    # page.click(".login_button")