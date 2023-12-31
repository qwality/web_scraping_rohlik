from fastapi import FastAPI, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

load_dotenv()

DEV = True if os.getenv('DEV') == 'True' else False

app = FastAPI()
'''FastAPI app reference'''

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",  # Vývojový server
        "https://rohlik.daniel-sykora.cz",  # Produkční server
    ] if not DEV else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from playwright.async_api import async_playwright

@app.get('/scrap-login')
async def scrap_login(request: Request, id: int=0, pin: int=0) -> JSONResponse:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://couriers-portal.rohlik.cz')
        await page.fill(".login_field > *:first-child", str(id))
        await page.fill(".login_field:nth-child(2) > *:first-child", str(pin))
        await page.click(".login_button")

        # cookies = await context.cookies()

        cp_courier_id = cp_courier_hash = None

        for cookie in await context.cookies():
            match cookie:
                case {'name': 'cp_courier_id', **rest}:
                    cp_courier_id = cookie
                case {'name': 'cp_courier_hash', **rest}:
                    cp_courier_hash = cookie

        # cp_courier_id = next(filter(lambda cookie: cookie['name'] == 'cp_courier_id',cookies), None)
        # cp_courier_hash = next(filter(lambda cookie: cookie['name'] == 'cp_courier_hash',cookies), None)

        if cp_courier_id and cp_courier_hash:
            response = JSONResponse(
                content={
                    'cp_courier_id': cp_courier_id,
                    'cp_courier_hash': cp_courier_hash
                },
                status_code=200
            )
            response.set_cookie(
                key=cp_courier_id['name'],
                value=cp_courier_id['value'],
                domain='scrap-rohlik.qwality.fun',
                # path=cp_courier_id['path'],
                expires=cp_courier_id['expires'],
                secure=cp_courier_id['secure'],
                httponly=cp_courier_id['httpOnly'],
                samesite=cp_courier_id['sameSite']
            )
            response.set_cookie(
                key=cp_courier_hash['name'],
                value=cp_courier_hash['value'],
                domain='scrap-rohlik.qwality.fun',
                # path=cp_courier_hash['path'],
                expires=cp_courier_hash['expires'],
                secure=cp_courier_hash['secure'],
                httponly=cp_courier_hash['httpOnly'],
                samesite=cp_courier_hash['sameSite']
            )
            return response
        else:
            return JSONResponse(
                content={
                    'error': 'no cookies found'
                },
                status_code=404
            )

from bs4 import BeautifulSoup

@app.get('/scrap-dashboard')
async def scrap_dashboard(request: Request, cp_courier_id: str, cp_courier_hash: str) -> JSONResponse:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        await context.add_cookies([
            {
                'name': 'cp_courier_hash',
                'value': cp_courier_hash,
                'domain': 'couriers-portal.rohlik.cz',
                'path': '/cz'
            },
            {
                'name': 'cp_courier_id',
                'value': cp_courier_id,
                'domain': 'couriers-portal.rohlik.cz',
                'path': '/cz'
            }
        ])
        page = await context.new_page()
        await page.goto('https://couriers-portal.rohlik.cz/cz/?p=dashboard')

        soup = BeautifulSoup(await page.inner_html('body'), 'html.parser')

        dashboard_table_plate = next(map(lambda e: list(e.stripped_strings), soup.find_all(class_='dashboard_table_plate')))
        dashboard_table_vehicle = next(map(lambda e: list(e.stripped_strings), soup.find_all(class_='dashboard_table_vehicle')))
        scrap_dashboard_s = list(map(lambda e: list(e.stripped_strings), soup.find_all(class_='dashboard_next_block')))
        badge_full_s = list(map(lambda e: list(e.stripped_strings), soup.find_all(class_='badge-full')))
        dashboard_table_stats_s = list(map(lambda e: list(e.stripped_strings), soup.find_all(class_='dashboard_table_stats')))
        dashboard_table_stats_blocks = next(map(lambda e: list(e.stripped_strings), soup.find_all(class_='dashboard_table_stats_blocks')))

        return JSONResponse(
            content={
                'dashboard_table_plate': dashboard_table_plate,
                'dashboard_table_vehicle': dashboard_table_vehicle,
                'scrap_dashboard_s': scrap_dashboard_s,
                'badge_full_s': badge_full_s,
                'dashboard_table_stats_s': dashboard_table_stats_s,
                'dashboard_table_stats_blocks': dashboard_table_stats_blocks
            },
            status_code=200
        )

@app.get('/scrap-blocks')
async def scrap_blocks(request: Request, cp_courier_id: str, cp_courier_hash: str) -> JSONResponse:
    # p=blocks
    # p=blocks&next_month
    
    return 'not implemented yet'

@app.get('/scrap-invoicing')
async def scrap_invoicing(request: Request, cp_courier_id: str, cp_courier_hash: str) -> JSONResponse:
    # p=invoicing2&month=202312 (month=YYYYMM)
    # p=invoices
    
    return 'not implemented yet'

@app.get('/scrap-scorecard')
async def scrap_scorecard(request: Request, cp_courier_id: str, cp_courier_hash: str) -> JSONResponse:
    # p=scorecard
    
    return 'not implemented yet'

@app.get('/scrap-karma')
async def scrap_karma(request: Request, cp_courier_id: str, cp_courier_hash: str) -> JSONResponse:
    # p=karma
    
    return 'not implemented yet'

@app.get('/scrap-bonpen')
async def scrap_bonpen(request: Request, cp_courier_id: str, cp_courier_hash: str) -> JSONResponse:
    # p=bonpen
    
    return 'not implemented yet'

@app.get('/scrap-wallet')
async def scrap_wallet(request: Request, cp_courier_id: str, cp_courier_hash: str) -> JSONResponse:
    # p=wallet
    
    return 'not implemented yet'


@app.get('/{path:path}')
async def catch_other(request: Request, path: str):
    '''replaces 404'''
    return f"Toto je catch-all koncový bod pro cestu: <{path}> \n tento endpoint nahrazuje 404"