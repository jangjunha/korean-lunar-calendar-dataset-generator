# korean-lunar-calendar-dataset-generator

[korean-lunar-calendar][korean-lunar-calendar]에서 사용하는 데이터셋 코드 생성기


## Requirements

* Python >= 3.10
* [Poetry][poetry]


## Install Dependencies

```bash
$ poetry install
```


## How to run

```bash
$ python run.py -k <SERVICE_KEY>
```


## `SERVICE_KEY`

[공공데이터포털][data-go-kr]의 [한국천문연구원 음양력 정보 API][kasi-api]를 사용합니다. 공공데이터포털에서 해당 API의 활용 신청 마치고, API 키를 발급받아 사용해주세요.

and see out/dataset.rs


[poetry]: https://python-poetry.org/
[korean-lunar-calendar]: https://github.com/jangjunha/korean-lunar-calendar/
[data-go-kr]: https://data.go.kr/
[kasi-api]: https://www.data.go.kr/data/15012679/openapi.do
