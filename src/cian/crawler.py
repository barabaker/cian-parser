import sys
import json
import asyncio
import logging
from typing import List, Optional
from core.schema import Subject, Work

from crawlee import (

    Request,
    ConcurrencySettings,
)
from crawlee.storages import RequestQueue
from crawlee.http_clients import CurlImpersonateHttpClient
from crawlee.proxy_configuration import ProxyConfiguration
from crawlee.crawlers import HttpCrawler, HttpCrawlingContext
from core.config import settings

if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Constants
API_URL = "https://api.cian.ru/search-engine/v1/search-offers-mobile-site/"
MAX_PAGES = 50
MIN_BBOX_SIZE = 0.001  # ~100 meters
PROXY_URLS = [
    "http://user:password@188.130.128.222:1050",
    # add more proxy
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def split_bbox(bbox: List[List[float]]) -> List[List[List[float]]]:

    min_x, min_y = bbox[0]
    max_x, max_y = bbox[1]

    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2

    return [
        [[min_x, min_y], [mid_x, mid_y]],  # bottom-left
        [[mid_x, min_y], [max_x, mid_y]],  # bottom-right
        [[min_x, mid_y], [mid_x, max_y]],  # top-left
        [[mid_x, mid_y], [max_x, max_y]]   # top-right
    ]


def make_payload(work: Work):
    payload = {
        "jsonQuery": {
            "_type": f"{work.offer_type}sale",
            "engine_version": {"type": "term", "value": 2},
            'region': {
                'type': 'terms',
                'value': work.subject_id,
            },
            "bbox": {
                "type": "term",
                "value": work.bbox
            },
            "page": {"type": "term", "value": work.page},
        }
    }
    return payload


def get_work_from_payload(payload: Optional[bytes]) -> Work:
    data = json.loads(payload)

    return Work(
        bbox = data["jsonQuery"]["bbox"]["value"],
        page = data["jsonQuery"]["page"]["value"],
        subject_id = data["jsonQuery"]["region"]["value"],
        offer_type = data["jsonQuery"]['_type'].replace("sale", '')
    )


def create_request(subject_id: int, bbox: List[List[float]], page: int = 1) -> Request:
    payload = make_payload(Work(bbox=bbox, page=page, subject_id=subject_id))
    return Request(
        url = API_URL,
        method = "POST",
        payload = json.dumps(payload).encode(),
        headers = {"Content-Type": "application/json"},
        use_extended_unique_key = True,
    )


async def start_crawler(subject: Subject) -> None:

    task_queue = await RequestQueue.open()

    http_client = CurlImpersonateHttpClient(
        timeout = 15,
        impersonate = "chrome124",
    )

    # Configure proxy
    proxy_configuration = ProxyConfiguration(proxy_urls = PROXY_URLS)

    # Configure concurrency
    concurrency_settings = ConcurrencySettings(
        min_concurrency = 5,
        max_concurrency = 15,
        max_tasks_per_minute = 150,
    )

    # Initialize crawler
    crawler = HttpCrawler(
        http_client = http_client,
        proxy_configuration = proxy_configuration,
        concurrency_settings = concurrency_settings,
    )

    async def add_request_task_queue(new_work: Work):
        data = make_payload(new_work)

        new_request = Request.from_url(
            url=API_URL,
            method='POST',
            payload = json.dumps(data).encode(),
            use_extended_unique_key = True
        )
        await task_queue.add_request(request = new_request)

    @crawler.router.default_handler
    async def default_handler(context: HttpCrawlingContext) -> None:
        logger = context.log

        content = context.http_response.read()
        data = json.loads(content.decode())

        current_work = get_work_from_payload(context.request.payload)

        # Handle pagination and splitting
        total_count = data.get("offersCount", 0)
        offers = data.get('offers', [])

        if total_count > 600:
            logger.info(f"Splitting bbox {current_work.bbox}")

            for new_bbox in split_bbox(current_work.bbox):
                new_work = Work(
                    bbox = new_bbox,
                    page = current_work.page,
                    subject_id = current_work.subject_id,
                    offer_type = subject.offer_type
                )
                await add_request_task_queue(new_work)

        elif offers and current_work.page < MAX_PAGES:
            new_work = Work(
                bbox = current_work.bbox,
                page = current_work.page + 1,
                subject_id = current_work.subject_id,
                offer_type = subject.offer_type
            )

            await context.push_data(offers)
            await add_request_task_queue(new_work)

    work = Work(
        bbox = subject.bbox,
        page = 1, subject_id = subject.id,
        offer_type = subject.offer_type
    )

    json_data = make_payload(work)

    request = Request.from_url(
        url = API_URL,
        method = 'POST',
        payload = json.dumps(json_data).encode(),
        use_extended_unique_key = True
    )

    await crawler.run([request])

    await crawler.export_data(path = settings.base_dir / 'result' / f'{subject.id[0]}.json')


async def start(region_id, name, bbox, offer_type):
    subject = Subject(
        id = [region_id],
        name = name,
        bbox = bbox,
        offer_type = offer_type,
    )
    await start_crawler(subject = subject)



if __name__ == "__main__":
    # 4605,1267655302447172,Псковская область, Псковская область,"[[27.317455, 55.588303], [31.51786, 59.021159]]"
    asyncio.run(start(
        name = 'Псковская область',
        bbox = '[[27.317455, 55.588303], [31.51786, 59.021159]]',
        region_id = 4605,
        offer_type = 'flat',
    ))
