import argparse
import asyncio
import pathlib

import os

from korean_lunar_calendar_dataset_generator.dataset import Dataset
from korean_lunar_calendar_dataset_generator.generate import generate


KEY = "oeYFktXnOo8e1lQyGQvPWrVFW0gTtOchQZT19i4uDGsmRbFsWUeQuBXQPeZhOtLVLJCS84/63eGQsAJ6NYYTew=="

parser = argparse.ArgumentParser(
    prog="korean-lunar-calendar-dataset-generator",
    description="음력-양력 변환 라이브러리 korean-lunar-calendar의 데이터셋을 생성합니다.",
)
parser.add_argument(
    "-o",
    "--output-dir",
    type=pathlib.Path,
    default=pathlib.Path("./out"),
    help="dataset.rs 출력 위치",
)
parser.add_argument("-k", "--key", required=True, help="공공데이터포털 서비스 키")


async def main():
    args = parser.parse_args()

    dataset = await Dataset.build(key=args.key)

    filepath = pathlib.Path(args.output_dir) / "dataset.rs"
    with open(filepath, "w") as f:
        f.write(generate(dataset))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
