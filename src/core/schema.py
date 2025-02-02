import json
from crawlee import Request
from core.config import settings
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


MIN_BBOX_SIZE = 0.000001  # Минимальный размер bbox для разделения


class Work(BaseModel):
    page: int = 1
    subject_id: List[int]
    bbox: List[List[float]]
    offer_type: str

    def make_payload(self):
        payload = {
            "jsonQuery": {
                "_type": f"{self.offer_type}sale",
                "engine_version": {"type": "term", "value": 2},
                'region': {
                    'type': 'terms',
                    'value': self.subject_id,
                },
                "bbox": {
                    "type": "term",
                    "value": self.bbox
                },
                "page": {"type": "term", "value": self.page},
            }
        }

        return payload

    def next_page(self):
        return Work(
            page=self.page + 1,
            subject_id=self.subject_id,
            bbox = self.bbox,
            offer_type=self.offer_type
        )

    def get_request(self):
        data = self.make_payload()
        new_request = Request.from_url(
            url = settings.API_URL,
            method="POST",
            payload=json.dumps(data),
            headers={"Content-Type": "application/json"},
            use_extended_unique_key=True
        )
        return new_request

    def split_bbox(self) -> List['Work']:
        """
        Разделяет bbox на дочерние задачи.
        Возвращает список дочерних задач.
        """
        min_x, min_y = self.bbox[0]
        max_x, max_y = self.bbox[1]

        # Проверяем, нужно ли дальше разделять bbox
        if abs(max_x - min_x) < MIN_BBOX_SIZE or abs(max_y - min_y) < MIN_BBOX_SIZE:
            return []

        # Вычисляем середину bbox с округлением до 6 знаков
        mid_x = round((min_x + max_x) / 2, 6)
        mid_y = round((min_y + max_y) / 2, 6)


        # Создаем 4 новых bbox
        list_bbox = [
            [[min_x, min_y], [mid_x, mid_y]],  # bottom-left
            [[mid_x, min_y], [max_x, mid_y]],  # bottom-right
            [[min_x, mid_y], [mid_x, max_y]],  # top-left
            [[mid_x, mid_y], [max_x, max_y]]  # top-right
        ]

        return [
            Work(
                page=self.page,
                subject_id=self.subject_id,
                bbox=bbox,
                offer_type=self.offer_type
            )
            for bbox in list_bbox
        ]


class HtmlData(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    creation_time: datetime = Field(alias="CreationTime")
    html: str = Field(alias="Html")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z" if v.tzinfo is None else v.isoformat()
        }


class AdsPhotos(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    photo_id: int = Field(alias="Id")
    ad_id: int = Field(alias="AdId")
    creation_time: datetime = Field(alias="CreationTime")
    image: str = Field(alias="Image")
    unique: bool = Field(default=False)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z" if v.tzinfo is None else v.isoformat()
        }


class AdsScreenshots(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    screenshot_id: int = Field(alias="Id")
    ad_id: int = Field(alias="AdId")
    creation_time: datetime = Field(alias="CreationTime")
    image: str = Field(alias="Image")
    unique: bool = Field(default=False)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z" if v.tzinfo is None else v.isoformat()
        }


def get_work_from_payload(payload: Optional[bytes]) -> 'Work':
    data = json.loads(payload)

    return Work(
        bbox = data["jsonQuery"]["bbox"]["value"],
        page = data["jsonQuery"]["page"]["value"],
        subject_id = data["jsonQuery"]["region"]["value"],
        offer_type = data["jsonQuery"]['_type'].replace("sale", '')
    )