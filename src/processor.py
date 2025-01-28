import orjson

import asyncio
from core.config import settings

from crawlee.configuration import Configuration
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.storages import KeyValueStore

import asyncio
from playwright.async_api import async_playwright

from crawlee import ConcurrencySettings
import base64



def read_json_files(directory):
    with open(directory, 'rb') as f:
        data = orjson.loads(f.read())
        yield from data

async def start():
    directory = settings.base_dir / 'result' / '4605.json'
    batch_url = []

    for item in read_json_files(directory):
        url = 'https://pskov.cian.ru/{dealType}/{offerType}/{id}/'.format(
            id = item.get('id'),
            dealType = item.get('dealType'),
            offerType = item.get('offerType'),
        )
        batch_url.append(url)

    async with async_playwright() as playwright:
        # browser = await playwright.firefox.launch(
        #     headless = False,
        # )
        # page = await browser.new_page()
        # await page.goto('https://cian.ru/')
        # try:
        #     await page.wait_for_timeout(3 * 1000)
        #     await page.get_by_role("button", name="Понятно").click()
        #     await page.wait_for_timeout(4 * 1000)
        #     await page.get_by_role("button", name="В другой раз").click()
        # except Exception as error:
        #     print(error)

        for i, url in enumerate(batch_url):
            print(url)
            # await page.goto(url = url)
            # await page.wait_for_timeout(1 * 1000)
            #
            # screenshot = await page.screenshot(full_page=True)
            # img_data = base64.b64encode(screenshot).decode()
            #
            # with open(f"{i}.png", "wb") as fh:
            #     fh.write(base64.decodebytes(img_data))



if __name__ == '__main__':
    asyncio.run(start())