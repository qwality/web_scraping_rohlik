# webscrapping project



### FastApi code snippet server
```python
from playwright.async_api import async_playwright

@app.get('/rohlik/alt-login')
async def rohlik_alt_login(request: Request, id: int=0, pin: int=0) -> JSONResponse:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://couriers-portal.rohlik.cz')
        await page.fill(".login_field > *:first-child", str(id))
        await page.fill(".login_field:nth-child(2) > *:first-child", str(pin))
        await page.click(".login_button")

        cookies = await context.cookies()

        cp_courier_id = next(filter(lambda cookie: cookie['name'] == 'cp_courier_id',cookies), None)
        cp_courier_hash = next(filter(lambda cookie: cookie['name'] == 'cp_courier_hash',cookies), None)

        if cp_courier_id and cp_courier_hash:
            return JSONResponse(
                content={
                    'cp_courier_id': cp_courier_id['value'],
                    'cp_courier_hash': cp_courier_hash['value']
                },
                status_code=200
            )
        else:
            return JSONResponse(
                content={
                    'error': 'no cookies found'
                },
                status_code=404
            )
```