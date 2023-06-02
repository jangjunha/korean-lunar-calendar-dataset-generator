import dataclasses
import datetime
from typing import AsyncIterable
import xml.etree.ElementTree

from aiohttp import ClientSession

from .constant import MIN_LUNAR_DATE, MAX_YEAR


@dataclasses.dataclass
class LunarDateData:
    year: int
    month: int
    day: int

    sol_year: int
    sol_month: int
    sol_day: int

    is_leap: bool = False

    @property
    def date(self) -> datetime.date:
        return datetime.date(self.sol_year, self.sol_month, self.sol_day)

    def __lt__(self, other: "LunarDateData") -> bool:
        if self.sol_year == other.sol_year:
            if self.sol_month == other.sol_month:
                if self.sol_day == other.sol_day:
                    assert False
                else:
                    return self.sol_day < other.sol_day
            else:
                return self.sol_month < other.sol_month
        else:
            return self.sol_year < other.sol_year


async def fetch(
    session: ClientSession, month: int, is_leap: bool = False, *, key: str
) -> AsyncIterable[LunarDateData]:
    URL = "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService/getSpcifyLunCalInfo"
    params = {
        "lunMonth": f"{month:02d}",
        "leapMonth": "윤" if is_leap else "평",
        "fromSolYear": str(MIN_LUNAR_DATE[0] - 1),
        "toSolYear": str(MAX_YEAR),
        "numOfRows": 1000000,
        "ServiceKey": key,
    }
    async with session.get(URL, params=params) as response:
        res = await response.text()
    root = xml.etree.ElementTree.fromstring(res)
    count = 0
    for elem in root.findall("./body/items/item"):
        count += 1
        ld = LunarDateData(
            year=int(elem.find("lunYear").text),
            month=int(elem.find("lunMonth").text),
            day=int(elem.find("lunDay").text),
            is_leap=elem.find("lunLeapmonth").text == "윤",
            sol_year=int(elem.find("solYear").text),
            sol_month=int(elem.find("solMonth").text),
            sol_day=int(elem.find("solDay").text),
            # lunNday=int(elem.find('lunNday').text),
        )
        if (ld.year, (ld.month, ld.is_leap), ld.day) < MIN_LUNAR_DATE:
            continue
        yield ld

    total_count = int(root.findtext("./body/totalCount"))
    assert count == total_count, f"{count=}, {total_count=}"
