import datetime
import itertools

from aiohttp import ClientSession
from aiostream.stream import merge

from .fetch import LunarDateData, fetch
from .typing import LunarDate


class CannotFoundException(Exception):
    pass


class Dataset:
    def __init__(
        self, base_date: LunarDateData, months: list[tuple[tuple[int, int, bool], int]]
    ) -> None:
        self.base_date = base_date
        self.months = months

    @classmethod
    async def build(
        cls,
        *,
        key: str,
    ) -> "Dataset":
        async with ClientSession() as session:
            async with merge(
                *(
                    fetch(session, month, is_leap, key=key)
                    for month, is_leap in itertools.product(
                        range(1, 1 + 12),
                        (False, True),
                    )
                )
            ).stream() as streamer:
                dates = [ld async for ld in streamer]
        dates.sort()
        it = iter(dates)

        d = next(it)
        # 음력 월당 일 수 계산
        curr_month = (d.year, d.month, d.is_leap)
        curr_days = 1
        res = []
        for ld in it:
            month = (ld.year, ld.month, ld.is_leap)
            if month != curr_month:
                res.append((curr_month, curr_days))
                curr_month = month
                curr_days = 1
            else:
                curr_days += 1
        res.append((curr_month, curr_days))
        return cls(d, res)

    def search(self, target: LunarDate) -> datetime.date:
        ty, (tm, tl), td = target

        days_sum = 0
        for (my, mm, ml), md in self.months:
            if ty == my and tm == mm and tl == ml:
                return self.base_date.date + datetime.timedelta(days=days_sum + td - 1)
            days_sum += md

        raise CannotFoundException()
