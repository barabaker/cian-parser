import orjson

import asyncio
from core.config import settings

from crawlee.configuration import Configuration
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.storages import KeyValueStore

import asyncio

from crawlee import ConcurrencySettings


async def main(batch_url) -> None:

    concurrency_settings = ConcurrencySettings(
        min_concurrency = 5,
        max_concurrency = 15,
        max_tasks_per_minute = 150,
    )

    crawler = PlaywrightCrawler(
        # configuration = Configuration(purge_on_start = False),

        headless = True,
        browser_type = 'firefox',
        concurrency_settings = concurrency_settings,
    )

    kvs = await KeyValueStore.open()

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url} ...')

        try:
            await context.page.wait_for_timeout(2 * 1000)
            await context.page.get_by_role("button", name="Понятно").click()
            await context.page.wait_for_timeout(2 * 1000)
            await context.page.get_by_role("button", name="В другой раз").click()
        except Exception as error:
            context.log.info(error)

        print(batch_url)

        for i, url in enumerate(batch_url):
            await context.page.goto(url = url)
            screenshot = await context.page.screenshot(full_page=True)
            await context.page.wait_for_timeout(1 * 1000)
            await kvs.set_value(
                key = f'{i}',
                value = screenshot,
                content_type = 'image/png',
            )

    await crawler.run(['https://pskov.cian.ru/'])


def read_json_files(directory):
    for json_file in directory.glob('*.json'):

        if json_file.name == '__metadata__.json':
            continue

        with open(json_file, 'rb') as f:
            data = orjson.loads(f.read())
            yield data


async def start():
    directory = settings.base_dir / 'cian' / 'storage' / 'datasets' / 'default'

    batch_url = []

    for item in read_json_files(directory):

        url = 'https://cian.ru/{dealType}/{offerType}/{id}/'.format(
            id = item.get('id'),
            dealType = item.get('dealType'),
            offerType = item.get('offerType'),
        )
        batch_url.append(url)

    await main(batch_url)


if __name__ == '__main__':
    asyncio.run(start())