from datetime import datetime, timedelta
from typing import Tuple


class TimeInterval:
    __start: Tuple[int, int]
    __end: Tuple[int, int]

    def __init__(self, start_h, start_m, end_h, end_m) -> None:
        self.__start = (start_h, start_m)
        self.__end = (end_h, end_m)

    def __eq__(self, other):
        if self.start == other.start \
            and self.end == other.end:
            return True
        return False

    def __str__(self) -> str:
        start_str = self.format_time(self.__start)
        end_str = self.format_time(self.__end)
        return f'{start_str} - {end_str}'

    def isInDatetime(self, dt: datetime) -> bool:
        start = dt.replace(hour=self.start[0], minute=self.start[1])
        end = dt.replace(hour=self.end[0], minute=self.end[1])

        if end < start and dt < start:
            start = start - timedelta(days=1)
        elif end < start:
            end = end + timedelta(days=1)


        return dt >= start and dt < end

    @staticmethod
    def format_time(t:Tuple[int, int]):
        h = "%02d" % t[0]
        m = "%02d" % t[1]
        return f'{h}:{m}'


    @staticmethod
    def parse_time(t:str) -> Tuple[int, int]:
        h, m = t.split(":")
        h = int(h)
        m = int(m)
        if h < 0 or h > 24:
            raise ValueError(f"Invalid hour {h} given")
        if m < 0 or m > 60:
            raise ValueError(f"Invalid minute {m} given")

        if h == 24:
            h = 0

        if m == 60:
            m = 0

        return (int(h), int(m))

    @classmethod
    def from_tuple(cls, start: Tuple[int, int], end: Tuple[int, int]):
        return cls(start[0], start[1], end[0], end[1])

    @classmethod
    def from_time(cls, start:str, end:str):
        start_t = cls.parse_time(start)
        end_t = cls.parse_time(end)
        return cls.from_tuple(start_t, end_t)

    @property
    def start(self) -> Tuple[int, int]:
        return self.__start

    @property
    def end(self) -> Tuple[int, int]:
        return self.__end

    @property
    def dtStart(self, now=datetime.now()) -> datetime:
        dt_start = now.replace(hour=self.start[0], minute=self.start[1])
        if dt_start < now:
            dt_start += timedelta(days=1)

        return dt_start