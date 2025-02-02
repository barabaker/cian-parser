import json
import asyncio
import logging
import aiohttp
import base64
from core.mongo import database



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


async def get_latest_updated_documents(collection, limit = 10):

    cursor = collection.find({"updated_at": {"$exists": True}}).sort("updated_at", -1).limit(limit)

    async for document in cursor:
        yield document



# Функция для загрузки изображения по URL и преобразования в base64
async def download_image_as_base64(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()  # Скачиваем бинарные данные
                return base64.b64encode(image_data).decode("utf-8")  # Кодируем в base64
            else:
                print(f"Ошибка при загрузке изображения: {url}")
                return None

async def start():

    all_subject = read_json('start_data.json')

    for item in all_subject:
        logger.info(f"---- START MEDIA LOADER ------")
        logger.info(f"---- {item.get('id')} - {item.get('name')}------")
        collection = database[item.get("id")]

        async for doc in get_latest_updated_documents(collection = collection, limit = 100):

            for media in doc.get('media'):
                url = media.get('url')
                print(url)

                # image_base64 = await download_image_as_base64(url = url)
                # print(image_base64)

        logger.info(f"---- STOP MEDIA LOADER ---- ")



if __name__ == "__main__":
    asyncio.run(start())