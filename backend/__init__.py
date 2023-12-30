from fastapi import FastAPI, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os

dev = True

app = FastAPI()
'''FastAPI app reference'''

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # Vývojový server
        "https://daniel-sykora.cz",  # Produkční server
    ] if not dev else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from playwright.async_api import async_playwright

@app.get('/alt-login')
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

@app.get('/{path:path}')
async def catch_other(request: Request, path: str):
    '''replaces 404'''
    return f"Toto je catch-all koncový bod pro cestu: <{path}> \n tento endpoint nahrazuje 404"