from datetime import datetime
from core.mongo import database
from pymongo import UpdateOne

from deepdiff import DeepDiff

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


async def bulk_upsert_offers(data, collection_name: str):
    collection = database[collection_name]
    now = datetime.utcnow()

    operations = []

    for offer in data:

        filter_data = {
            "id": offer.get("id"),
            "cianId": offer.get("cianId"),
        }

        doc = await collection.find_one(filter_data)

        if doc and offer and offer.get('media') == doc.get('media') and offer.get('price') == doc.get('price'):
            continue

        update_data = {
            "$set": {**offer, "updated_at": now},  # Обновляем данные и поле updated_at
            "$setOnInsert": {"created_at": now},  # Устанавливаем created_at только при вставке
        }

        # Создаем операцию UpdateOne с флагом upsert
        operation = UpdateOne(
            filter_data,   # Критерий поиска
            update_data,   # Данные для обновления
            upsert = True  # Включить upsert
        )
        operations.append(operation)

    if operations:
        try:
            result = await collection.bulk_write(operations)
            logger.info(f"Вставлено / Обновлено: {result.upserted_count} / {result.modified_count}")
        except Exception as e:
            logger.error(f"Ошибка при выполнении bulk операций: {e}")
