from .dataset import Dataset
from .fetch import LunarDateData


TEMPLATE = """// Code generated from https://github.com/jangjunha/korean-lunar-calendar-dataset-generator
use chrono::NaiveDate;
use lazy_static::lazy_static;

use crate::month::M;

lazy_static! {{
    pub static ref BASE: NaiveDate = NaiveDate::from_ymd_opt({base_year}, {base_month}, {base_day}).unwrap();
}}

pub const MONTHS: &'static [M] = &[
{months}
];
"""


def generate(
    dataset: Dataset,
) -> str:
    months = []
    for (my, mm, ml), md in dataset.months:
        l = "true" if ml else "false"
        months.append(f"    M {{ y: {my}, m: {mm}, l: {l}, d: {md} }},")

    base_date = dataset.base_date
    return TEMPLATE.format(
        base_year=base_date.date.year,
        base_month=base_date.date.month,
        base_day=base_date.date.day,
        months="\n".join(months),
    )
