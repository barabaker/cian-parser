from core.config import settings
from region.schema import RegionManager

manager = RegionManager(settings.BASE_DIR / 'region' / "data.json")
