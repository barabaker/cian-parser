import json
import asyncio

from core.schema import Work
from cian.crawler import start_crawler


PROXY_URLS = [
    'http://uSxBhB:Ci4ZIXyrcR@46.8.14.118:1050',
    'http://uSxBhB:Ci4ZIXyrcR@188.130.128.226:1050',
    'http://uSxBhB:Ci4ZIXyrcR@109.248.204.178:1050',
    'http://uSxBhB:Ci4ZIXyrcR@188.130.128.243:1050',
    'http://uSxBhB:Ci4ZIXyrcR@45.86.0.17:1050',
    'http://uSxBhB:Ci4ZIXyrcR@109.248.15.143:1050',
    'http://uSxBhB:Ci4ZIXyrcR@45.15.72.152:1050',
    'http://uSxBhB:Ci4ZIXyrcR@188.130.185.104:1050',
    'http://uSxBhB:Ci4ZIXyrcR@188.130.136.101:1050',
    'http://uSxBhB:Ci4ZIXyrcR@95.182.125.210:1050',
    'http://uSxBhB:Ci4ZIXyrcR@45.86.1.238:1050',
    'http://uSxBhB:Ci4ZIXyrcR@109.248.205.101:1050',
    'http://uSxBhB:Ci4ZIXyrcR@188.130.185.117:1050',
    'http://uSxBhB:Ci4ZIXyrcR@45.87.252.200:1050',
    'http://uSxBhB:Ci4ZIXyrcR@109.248.142.144:1050',
    'http://uSxBhB:Ci4ZIXyrcR@46.8.22.215:1050',
    'http://uSxBhB:Ci4ZIXyrcR@109.248.142.27:1050',
    'http://uSxBhB:Ci4ZIXyrcR@185.181.246.126:1050',
    'http://uSxBhB:Ci4ZIXyrcR@46.8.107.162:1050'
]


def read_json(json_file_path):
    with open(json_file_path, mode='r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


async def start():

    task_region_ok = ['4553']

    all_subject = read_json('start_data.json')

    for item in all_subject:

        work = Work(
            subject_id = [item.get('id')],
            bbox = item.get('bbox'),
            offer_type = "suburban"
        )

        await start_crawler(work = work, proxy_list = PROXY_URLS)



if __name__ == "__main__":

    asyncio.run(start())