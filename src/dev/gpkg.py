from typing import List
import geopandas as gpd
from shapely.geometry import Polygon
def expand_bbox(bbox: List[List[float]], padding: float = 0.05) -> List[List[float]]:
    """
    Расширяет bounding box на заданный отступ (padding).
    """
    min_x, min_y = bbox[0]
    max_x, max_y = bbox[1]

    # Расширяем bbox
    min_x -= padding
    min_y -= padding
    max_x += padding
    max_y += padding

    return [[min_x, min_y], [max_x, max_y]]
def split_bbox(bbox: List[List[float]]) -> List[List[List[float]]]:
    """
    Разделяет bounding box на 4 части.
    """
    min_x, min_y = bbox[0]
    max_x, max_y = bbox[1]

    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2

    bboxes = [
        [[min_x, min_y], [mid_x, mid_y]],  # bottom-left
        [[mid_x, min_y], [max_x, mid_y]],  # bottom-right
        [[min_x, mid_y], [mid_x, max_y]],  # top-left
        [[mid_x, mid_y], [max_x, max_y]]   # top-right
    ]

    return [expand_bbox(b) for b in bboxes]


def create_gpkg_files(bbox: str, original_output: str = "original_bbox.gpkg", split_output: str = "split_bbox.gpkg"):
    """
    Создает два GPKG файла:
    1. С исходным bbox.
    2. С разделёнными bbox.
    """
    # Преобразуем строку bbox в список
    bbox = eval(bbox)
    min_x, min_y = bbox[0]
    max_x, max_y = bbox[1]

    # Создаем исходный bbox
    original_bbox = Polygon([
        (min_x, min_y),
        (max_x, min_y),
        (max_x, max_y),
        (min_x, max_y),
        (min_x, min_y)
    ])

    # Создаем GeoDataFrame для исходного bbox
    gdf_original = gpd.GeoDataFrame({"geometry": [original_bbox], "name": ["Original BBox"]})

    # Сохраняем исходный bbox в GPKG файл
    gdf_original.to_file(original_output, driver="GPKG")
    print(f"Исходный bbox сохранен в: {original_output}")

    # Разделяем bbox на 4 части
    split_bboxes = split_bbox(bbox)
    split_polygons = [Polygon([(b[0][0], b[0][1]), (b[1][0], b[0][1]), (b[1][0], b[1][1]), (b[0][0], b[1][1])]) for b in split_bboxes]

    for i, polygon in enumerate(split_polygons):
        print(polygon)
        #
        # # Создаем GeoDataFrame для разделённых bbox
        gdf_split = gpd.GeoDataFrame({"geometry": polygon, "name": ["Bottom-Left", "Bottom-Right", "Top-Left", "Top-Right"]})

        # # Сохраняем разделённые bbox в GPKG файл
        gdf_split.to_file(f'{i}.gpkg', driver="GPKG")
        print(f"Разделенные bbox сохранены в: {split_output}")

# Пример использования
bbox = '[[27.317455, 55.588303], [31.51786, 59.021159]]'
create_gpkg_files(bbox, original_output="original_bbox.gpkg", split_output="split_bbox.gpkg")