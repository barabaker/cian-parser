import sys
import base64
import asyncio

from curl_cffi.requests import AsyncSession
from core.mongo import database
from core.logger import logger
from region import manager


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_latest_updated_documents(collection, limit = 10):
    cursor = collection.find({"updated_at": {"$exists": True}}).sort("updated_at", -1).limit(limit)
    async for document in cursor:
        yield document

# Функция для загрузки изображения по URL и преобразования в base64
async def download_image_as_base64(url, semaphore):
    async with semaphore:  # Ограничиваем количество одновременных запросов
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        try:
            async with AsyncSession(headers = headers) as session:
                response = await session.get(url)
                if response.status_code == 200:
                    image_data = response.content  # Получаем бинарные данные
                    return base64.b64encode(image_data).decode("utf-8")  # Кодируем в base64
                else:
                    logger.error(f"Ошибка при загрузке изображения: {url}, статус: {response.status_code}")
                    return None
        except Exception as e:
            logger.error(f"Ошибка при загрузке изображения {url}: {e}")
            return None


async def start():
    for region in manager.get_all_regions():
        logger.info(f"---- START MEDIA LOADER ----->  {region.id} - {region.name}------")

        collection = database[region.id]

        semaphore = asyncio.Semaphore(1)
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        async for doc in get_latest_updated_documents(collection = collection):

            tasks = []

            async with AsyncSession(headers = headers) as session:

                for media in doc.get("media", []):
                    url = media.get("url")

                    url = url.replace('https', 'http')
                    response = await session.get(url)

                    if response.ok:
                        image_data = response.content  # Получаем бинарные данные
                        image_data = base64.b64encode(image_data).decode("utf-8")  # Кодируем в base64
                        print(image_data)

                await asyncio.sleep(5)

        logger.info(f"---- STOP MEDIA LOADER-----> {region.id} - {region.name}------")


if __name__ == "__main__":
    asyncio.run(start())