"""Module to parse and scrape data from hp pages"""
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import pandas as pd


def scrape(url: str, *args, **kwargs) -> pd.DataFrame:
    df = pd.read_html(url)

    if isinstance(df, list):
        df = pd.concat(df)


    df.columns = ["Properties", "Values"]
    df = df.set_index("Properties").rename(index={"Audio features": "Audio"})

    return df