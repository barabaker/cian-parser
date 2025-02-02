from pydantic import BaseModel, ValidationError
from typing import List, Tuple, Union
import json


class Region(BaseModel):
    id: str
    gis_id: str
    name: str
    full_name: str
    bbox: List[List[float]]


class RegionManager:
    def __init__(self, file_path: str):
        """
        Инициализация менеджера регионов.
        Принимает путь к файлу data.json, который должен содержать список регионов в формате JSON.
        """
        try:
            # Загрузка данных из файла
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Валидируем данные с помощью Pydantic
            self.regions = [Region(**item) for item in data]
        except FileNotFoundError:
            raise ValueError(f"Файл {file_path} не найден.")
        except json.JSONDecodeError:
            raise ValueError(f"Файл {file_path} содержит некорректный JSON.")
        except ValidationError as e:
            raise ValueError(f"Ошибка валидации данных: {e}")

    def find_region_by_id(self, region_id: str) -> Union[Region, None]:
        """
        Находит регион по его ID.
        """
        for region in self.regions:
            if region.id == region_id:
                return region
        return None

    def get_all_regions(self) -> List[Region]:
        """
        Возвращает список всех регионов.
        """
        return self.regions

    def __str__(self) -> str:
        """
        Возвращает строковое представление всех регионов.
        """
        return "Регионы:\n" + "\n".join(f"- {region}" for region in self.regions)