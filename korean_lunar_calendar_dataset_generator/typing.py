from typing import TypeAlias


LunarDate: TypeAlias = tuple[int, tuple[int, bool], int]  # 년, (월, 윤년여부), 일
