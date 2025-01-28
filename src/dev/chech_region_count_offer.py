# получаем дома, дачи, участки, коттеджи в Ярославской области
import requests

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}
# 4605,1267655302447172,Псковская область, Псковская область,"[[27.317455, 55.588303], [31.51786, 59.021159]]"


params = {
    'bbox': '55.588303,27.317455,59.021159,31.51786',
    'deal_type': 'sale',
    # 'region': '4605',
    'offer_type': 'flat',
    'parentOrigin': 'https://www.cian.ru',
}

url = 'https://api.cian.ru/mobile-search-frontend/v1/get-results-for-map'

response = requests.get(url = url, params = params, headers = headers)
print(response.url)