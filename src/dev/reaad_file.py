import orjson
from core.config import settings
from pymongo import MongoClient, UpdateOne
from datetime import datetime

directory = settings.base_dir / 'cian' / 'storage' / 'datasets' / 'default'


def read_json_files(directory):

    for json_file in directory.glob('*.json'):

        if json_file.name == '__metadata__.json':
            continue

        with open(json_file, 'rb') as f:
            data = orjson.loads(f.read())
            data['price'] = {**data.pop('price'), 'update_at': datetime.utcnow()}
            data['media'] = [{**m, 'update_at': datetime.utcnow()} for m in data.get('media')]
            yield data


def save_to_mongodb(directory, db_name, collection_name):
    client = MongoClient(settings.mongo.dsn)

    db = client[db_name]
    collection = db[collection_name]

    operations = []
    for data in read_json_files(directory):

        filter_query = {"id": data.get("id"), "cianId": data.get("cianId")}
        update_query = {
            "$set": {**data, "update_at": datetime.utcnow()},
            "$setOnInsert": {"create_at": datetime.utcnow()}
        }

        operations.append(
            UpdateOne(filter_query, update_query, upsert=True)
        )

    if operations:
        result = collection.bulk_write(operations)
        print(f"Вставлено документов: {result.upserted_count}")
        print(f"Обновлено документов: {result.modified_count}")
    else:
        print("Нет данных для вставки.")

save_to_mongodb(
    db_name = "suburban",
    directory = directory,
    collection_name = "4605"
)



# {'id': 301809285, 'cianId': 301809285, 'dealType': 'sale', 'offerType': 'suburban', 'category': 'houseSale', 'price': {'value': 56000000, 'currency': 'rur'}, 'offerInfo': {}, 'icons': [], 'description': 'Продается дом на земельном ухоженном участке общей площадью 15 соток. В основании дома стоит фундамент ФБС-6 на фундаментных подушках с полноценным цокольным этажом. Дом выложен из глиняного кирпича, толщина стен 64 см. Внутренние стены дома оштукатурены, потолки сделаны из гипсокартона.\nРазмер дома 16х13 м..\nНа цокольном этаже расположены: бильярд, настольный теннис, котельная, кладовая.\nНа 1 этаже расположены: кабинет-гостевая комната, кухня совмещенная с гостиной + выход на террасу, санузел, гардеробная, гараж под легковую машину.\nНа 2 этаже расположены: 4 жилых комнаты, гардеробная, санузел с ванной и душевой кабиной.\nНа мансардном этаже расположен: тренажерный зал. \nНа территории участка расположены: \n-отдельный гараж под микроавтобус с смотровой ямой (размер 8х5 м., высота проема 3 метра).\n-вольер для собаки 1,5х3 м.\n-Садовая мастерская 3х5 м.\n-Сарай-курятник 3х10 м. + закрытый прогулочный дворик 4,5х5,5 м.\n-Баня из калиброванного бревна 6х4 м. с выпуском 2 м. (отдельная парилка, моечная, предбанник), подведен водопровод.\n-Бассейн уличный, открытый с диаметром 3,5 м. и глубиной 1,5 м.', 'media': [{'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165751208-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165751208-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750683-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750683-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750665-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750665-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750678-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750678-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750649-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750649-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750618-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750618-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750620-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750620-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750622-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750622-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750625-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750625-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750653-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750653-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750651-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750651-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750652-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750652-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750655-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750655-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165753095-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165753095-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750662-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165750662-4.jpg', 'type': 'photo'}, {'url': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165753043-1.jpg', 'previewUrl': 'https://images.cdn-cian.ru/images/dom-hoticy-prigorodnaya-ulica-2165753043-4.jpg', 'type': 'photo'}], 'photoLabel': {'color': 'greenForCheckedOwner', 'name': 'Собственник'}, 'photoLabels': [{'color': 'greenForCheckedOwner', 'name': 'Собственник'}, {'color': 'grey', 'name': 'Проверено в Росреестре'}], 'features': {'objectType': 'Дом', 'totalArea': '780\xa0м²', 'landArea': '15\xa0сот.', 'landStatus': 'ИЖС'}, 'geo': {'regionId': 4605, 'undergrounds': [], 'highways': [], 'address': [{'key': 'location', 'value': 'Псковская область', 'locationTypeId': 2}, {'key': 'location', 'value': 'Псковский район', 'locationTypeId': 141}, {'key': 'location', 'value': 'Писковичская волость', 'locationTypeId': 144}, {'key': 'location', 'value': 'д. Хотицы', 'locationTypeId': 161}, {'key': 'street', 'value': 'улица Пригородная'}], 'coordinates': {'lat': 57.841728, 'lng': 28.26222}}, 'gaLabel': '/sale/suburban/mo_id=0/obl_id=4605/city_id=1148027/object_type=0/ga_obj_type=1/spec=none/301809285/from_developer=0/repres=0/owner=1/pod_snos=0/', 'isPromoted': False, 'isColorized': False, 'puids': {'puid1': 'deal_type_sale', 'puid2': 'offer_suburban', 'puid5': 'obl_id_4605', 'puid8': 56000000, 'puid10': 'no_agent', 'puid11': '1', 'puid16': 'false', 'puid17': 'false', 'puid36': 1148027}, 'phones': ['+79113814468'], 'author': {'realtyId': 116347865, 'cianId': 116347865, 'id': 'ID 116347865', 'isHonest': False, 'isPro': False, 'isPartner': False, 'isChatsEnabled': True, 'moderationInfo': {'showUserIdentifiedByDocuments': False}}, 'isFavorite': False, 'fromImport': False, 'isViewedOffer': False, 'showWarningMessage': False, 'isCalltrackingEnabled': True, 'moderationInfo': {'showContactWarningMessage': False}, 'hasTour': False, 'isExternalTourAvailable': False, 'photoFeatureIcons': [], 'isCianPartner': False, 'isRosreestrChecked': False, 'villageMortgageAllowed': False, 'callButtonTitle': 'Позвонить', 'isBookedFromDeveloper': False, 'factoids': [{'type': 'gasMain', 'title': 'Магистральный газ в доме или на участке'}, {'type': 'waterCentral', 'title': 'Центральное водоснабжение'}, {'type': 'bathhouse', 'title': 'Баня'}]}
#
# for file_name, content in read_json_files(directory):
#     print(f"Содержимое: {content}")