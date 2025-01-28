from datetime import datetime
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError, DuplicateKeyError
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

        # Создаем индекс для поля id
        self.collection.create_index("id", unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item):
        try:
            now = datetime.utcnow()

            # Добавляем временные метки
            item['created_at'] = now
            item['updated_at'] = now

            # Создаем операцию обновления
            update_operation = UpdateOne(
                {'id': item['id']},
                {
                    '$setOnInsert': {'created_at': now},
                    '$set': {'updated_at': now, **item}
                },
                upsert=True
            )

            # Выполняем операцию
            result = self.collection.bulk_write([update_operation])

            if result.upserted_count > 0:
                logger.info(f"Inserted new document with id: {item['id']}")
            else:
                logger.info(f"Updated existing document with id: {item['id']}")

            return item

        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error for id {item['id']}: {e}")
        except BulkWriteError as e:
            logger.error(f"Bulk write error: {e.details}")
        except Exception as e:
            logger.error(f"Error processing item {item['id']}: {e}")

    def process_items(self, items):
        """Для пакетной обработки"""
        try:
            now = datetime.utcnow()
            operations = []

            for item in items:
                item['created_at'] = now
                item['updated_at'] = now

                operations.append(
                    UpdateOne(
                        {'id': item['id']},
                        {
                            '$setOnInsert': {'created_at': now},
                            '$set': {'updated_at': now, **item}
                        },
                        upsert=True
                    )
                )

            result = self.collection.bulk_write(operations)
            logger.info(
                f"Processed {len(items)} items. Inserted: {result.upserted_count}, Updated: {result.modified_count}")
            return result

        except BulkWriteError as e:
            logger.error(f"Bulk write error: {e.details}")
        except Exception as e:
            logger.error(f"Error processing batch: {e}")


# Пример использования
if __name__ == "__main__":
    # Конфигурация
    MONGO_URI = "mongodb://localhost:27017"
    MONGO_DB = "cian_data"
    COLLECTION_NAME = "real_estate"

    # Инициализация пайплайна
    pipeline = MongoDBPipeline(
        mongo_uri=MONGO_URI,
        mongo_db=MONGO_DB,
        collection_name=COLLECTION_NAME
    )

    # Пример данных (ваш JSON объект)
    sample_item = {
        "id": 214865068,
        "cianId": 214865068,
        # ... остальные поля
    }

    # Обработка одного элемента
    pipeline.open_spider(None)
    pipeline.process_item(sample_item)

    # Или пакетная обработка
    # pipeline.process_items([item1, item2, item3])

    pipeline.close_spider(None)