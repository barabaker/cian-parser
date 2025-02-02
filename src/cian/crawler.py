import sys
import json
import asyncio


from core.schema import Work, get_work_from_payload
from crawlee import ConcurrencySettings
from crawlee.storages import RequestQueue
from crawlee.http_clients import CurlImpersonateHttpClient
from crawlee.proxy_configuration import ProxyConfiguration
from crawlee.crawlers import HttpCrawler, HttpCrawlingContext
from core.config import settings
from core.pipeline import bulk_upsert_offers
from typing import List


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



async def start_crawler(work: Work, proxy_list: List[str]) -> None:

    task_queue = await RequestQueue.open()

    http_client = CurlImpersonateHttpClient(
        timeout = 15,
        impersonate = "chrome124",
    )

    # Configure proxy
    proxy_configuration = ProxyConfiguration(proxy_urls = proxy_list)

    # Configure concurrency
    concurrency_settings = ConcurrencySettings(
        min_concurrency = 5,
        max_concurrency = 19,
        max_tasks_per_minute = 80,
    )

    crawler = HttpCrawler(
        http_client = http_client,
        proxy_configuration = proxy_configuration,
        concurrency_settings = concurrency_settings,

    )

    @crawler.router.default_handler
    async def default_handler(context: HttpCrawlingContext) -> None:
        logger = context.log

        content = context.http_response.read()
        data = json.loads(content.decode())

        current_work = get_work_from_payload(context.request.payload)

        # Handle pagination and splitting
        offers = data.get('offers', [])
        total_count = data.get("offersCount", 0)

        await bulk_upsert_offers(data = offers, collection_name = str(work.subject_id[0]))
        # await context.push_data(offers)

        if total_count >= 420:
            logger.info(f"Splitting bbox {current_work.bbox}")

            for new_work in current_work.split_bbox():
                await task_queue.add_request(request = new_work.get_request())

        elif offers and current_work.page < settings.MAX_PAGES:
            new_work = current_work.next_page()
            await task_queue.add_request(request = new_work.get_request())

    work = Work(
        page = 1,
        bbox = work.bbox,
        subject_id = work.subject_id,
        offer_type = work.offer_type
    )

    request = work.get_request()

    await crawler.run([request])