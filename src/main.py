import json
import asyncio
import logging

from core.schema import Work
from cian.crawler import start_crawler
from core.config import settings

PROXY_BASE = 'http://{}:{}@{}:{}'
PROXY_HOSTS = [
    '46.8.14.118',
    '188.130.128.226',
    '109.248.204.178',
    '188.130.128.243',
    '45.86.0.17',
    '109.248.15.143',
    '45.15.72.152',
    '188.130.185.104',
    '188.130.136.101',
    '95.182.125.210',
    '45.86.1.238',
    '109.248.205.101',
    '188.130.185.117',
    '45.87.252.200',
    '109.248.142.144',
    '46.8.22.215',
    '109.248.142.27',
    '185.181.246.126',
    '46.8.107.162',
    '188.130.129.11',
    '46.8.212.160',
    '46.8.56.229',
    '185.181.247.48',
    '109.248.12.55',
    '185.181.245.239',
    '46.8.213.111',
    '45.86.0.165',
    '46.8.154.226',
    '45.86.1.172',
    '188.130.185.35',
    '188.130.137.14'
]

PROXY_URLS = [PROXY_BASE.format(
    settings.proxy.username,
    settings.proxy.password,
    host, settings.proxy.port) for host in PROXY_HOSTS
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

def read_json(json_file_path):
    with open(json_file_path, mode='r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


async def start():

    all_subject = read_json('start_data.json')

    for item in all_subject:

        work = Work(
            subject_id = [item.get('id')],
            bbox = item.get('bbox'),
            offer_type = "suburban"
        )
        logger.info(f"---- START ------")
        logger.info(f"---- {item.get('id')} - {item.get('name')}------")
        await start_crawler(work = work, proxy_list = PROXY_URLS)
        logger.info(f"---- STOP ---- {item.get('id')} - {item.get('name')} ------")


if __name__ == "__main__":
    asyncio.run(start())