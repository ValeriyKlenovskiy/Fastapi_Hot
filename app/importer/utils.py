from datetime import datetime
import json
from typing import Iterable

from app.bookings.service import BookingsService
from app.hotels.service import HotelsService
from app.hotels.rooms.service import RoomsService
from app.logger import logger

TABLE_MODEL_MAP = {
    "hotels": HotelsService,
    "rooms": RoomsService,
    "bookings": BookingsService,
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    try:
        data = []
        for row in csv_iterable:
            for k, v in row.items():
                if v.isdigit():
                    row[k] = int(v)
                elif k == "services":
                    row[k] = json.loads(v.replace("'", '"'))
                elif "date" in k:
                    row[k] = datetime.strptime(v, "%Y-%m-%d")
            data.append(row)
        return data
    except Exception:
        logger.error("Cannot convert CSV into DB format", exc_info=True)
