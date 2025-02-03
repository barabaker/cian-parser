import requests
import shutil

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}

response = requests.get(
    'http://images.cdn-cian.ru/images/dom-yablonovskiy-cvetochnaya-ulica-2229139512-1.jpg',
    headers=headers, verify=False
)
print(response.raw)
if response.status_code == 200:
    with open('path.png', 'wb') as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)