"""Module to parse and scrape data from various jio webpages"""
from __future__ import annotations
from typing import NamedTuple
from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import pandas as pd
import numpy as np


class Plan(NamedTuple):
    price: int
    validity: int
    data: float
    subscriptions: int
    daily: bool
    total_data: float
    data_per_day: float
    price_per_day: float

    @staticmethod
    def from_details(*args) -> Plan:
        labels = ['PLAN', 'VALIDITY', 'DATA', 'SUBSCRIPTIONS']

        price, validity, data, subscriptions = None, None, None, None
        daily = None
        extra_validity = 0
        extra_data = 0

        current_label = None

        for token in args:
            if token in labels:
                current_label = token
                continue

            if current_label == 'PLAN':
                if token.isdigit():
                    price = int(token)
                if "days extra" in token:
                    extra_validity = int(token.split('+ ')[-1].split(' days extra)')[0])

            if current_label == 'VALIDITY':
                if token.endswith(" days"):
                    validity = int(token.split(' ')[0]) + extra_validity

            if current_label == 'DATA':
                if token.startswith('+'):
                    extra_data = int(token[1:].strip().split(' ')[0])
                elif token.endswith(" GB/day"):
                    daily = True
                    data = float(token.split(' ')[0])
                elif token.endswith(" GB"):
                    daily = False
                    data = float(token.split(' ')[0])
                else:
                    pass

            if current_label == 'SUBSCRIPTIONS':
                if token.endswith(" more"):
                    subscriptions = 2 + int(token[1:].split(' ')[0])

        total_data = (data * validity) + extra_data if daily else (data + extra_data)
        data_per_day = data + (extra_data / validity) if daily else total_data / validity
        data_per_day = np.round(data_per_day, 2)
        price_per_day = price / validity
        price_per_day = np.round(price_per_day, 2)

        return Plan(price,
                    validity,
                    data,
                    subscriptions,
                    daily,
                    total_data,
                    data_per_day,
                    price_per_day)


def match_id_class(tag: Tag, _id: str, _class: str) -> bool:
    return tag.name == _id and tag.has_attr('class') and _class in tag.get('class')


def find_detail_tags(tag: Tag) -> bool:
    return match_id_class(tag, 'div', 'pkv_txt_info') or match_id_class(tag, 'a', 'pkv-link')


def scrape_data_from_jio() -> pd.DataFrame:
    plans = []
    for url in ["https://www.jio.com/en-in/4g-plans", "https://www.jio.com/jio-value-recharge-plans"]:
        data = requests.get(url).content
        soup = BeautifulSoup(data, 'html.parser')
        for plan in soup.find_all("div", "pkv_card_list_ul"):
            details = []
            for detail in plan.find_all("div", "pkv_card_list_li"):
                items = []
                for item in detail.children:
                    text = item.get_text().strip().replace('\xa0', ' ').replace('`', '')
                    if text:
                        items.append(text)
                details.extend(items)
            plans.append(Plan.from_details(*details))

    return pd.DataFrame.from_records(plans, columns=Plan._fields)


if __name__ == '__main__':
    df = scrape_data_from_jio()
    data_path = Path(__file__).parent.parent.parent / 'static' / 'data'
    df.drop(columns=["subscriptions"]).sort_values(by="price_per_day", ascending=True).to_csv(data_path / 'jio.csv', index=False)
