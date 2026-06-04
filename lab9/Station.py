from datetime import datetime


class Station:
    def __init__(
            self,
            code: str,
            international_code: str | None,
            name: str,
            old_code: str | None,
            launch_date: datetime,
            close_date: datetime | None,
            station_type: str,
            area_type: str,
            operational_type: str,
            voivodeship: str,
            city: str,
            address: str | None,
            north: float,
            east: float
    ):
        self.code = code
        self.international_code = international_code
        self.name = name
        self.old_code = old_code
        self.launch_date = launch_date
        self.close_date = close_date
        self.station_type = station_type
        self.area_type = area_type
        self.operational_type = operational_type
        self.voivodeship = voivodeship
        self.city = city
        self.address = address
        self.north = north
        self.east = east

    def __str__(self) -> str:
        return f"Station {self.code}: {self.name} ({self.city})"

    def __repr__(self) -> str:
        cls_name: str = type(self).__name__
        args: str = ", ".join(f"{k}={v!r}" for k,v in vars(self).items())
        return f"{cls_name}({args})" # wypisuje tak abym mogl to potem stworzyc

    def __eq__(self, other : object) -> bool:
        if not isinstance(other, Station):
            return NotImplemented # wymusza na drugim obiekcie wywołanie __eq__
        return self.code == other.code

