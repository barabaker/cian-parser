# получаем дома, дачи, участки, коттеджи в Ярославской области
import requests

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

params = {
    'bbox': '50.639877,77.889018,54.45311,87.170489',
    'deal_type': 'sale',
    'offer_type': 'suburban',
    'parentOrigin': 'https://www.cian.ru',
}

url = 'https://api.cian.ru/mobile-search-frontend/v1/get-results-for-map'

response = requests.get(url = url, params = params, headers = headers)
