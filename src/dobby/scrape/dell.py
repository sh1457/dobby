"""Module to parse and scrape data from dell pages"""
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import pandas as pd


def process_dell_df(df: pd.DataFrame, filters: dict[str,str]=None) -> Optional[pd.DataFrame]:
    index_name = df.columns[0]
    print(f">>> {index_name}")
    if index_name in ["Description", "Decsription", "Specifications", "Features"]:
        index_list = [x for x in df.columns if x.startswith(index_name)]
        if len(index_list) > 1:
            print("> Flatten")
            col_to_keep = index_list.pop()
            df = df.drop(columns=index_list).rename(columns={col_to_keep: "Properties"}).set_index("Properties")
        else:
            df = df.rename(columns={index_name: "Properties"}).set_index("Properties")

        values_list = [x for x in df.columns if x.startswith("Values")]
        if len(values_list) > 1:
            if filters is not None:
                print("> Filter")
                for k, v in filters.items():
                    if k in df.index:
                        print(f"Found: {k}")
                        if v in df.loc[k].values:
                            print(f"Found: {v}")
                            for col, val in zip(df.columns, df.loc[k]):
                                if v.strip() == val.strip():
                                    col_to_keep = col
                                    other_cols = [x for x in df.columns if x != col_to_keep]
                                    df = df.drop(columns=other_cols).rename(columns={col_to_keep: "Values"})
                                    break

            values_list = [x for x in df.columns if x.startswith("Values")]
            if len(values_list) > 1:
                print("> Explode")


    print(df.head(25))


def scrape_dell(url: str, *args, **kwargs) -> pd.DataFrame:
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    list_items = soup.find_all("li")
    for li in list_items:
        if li.a is None or li.a.attrs.get("data-topicguid") is None:
            continue
        uri = "https:" + li.a.attrs.get("href")
        try:
            tdfs = pd.read_html(uri)
        except:
            continue
        if len(tdfs) > 1:
            print("> There's another table")
        for tdf in tdfs:
            process_dell_df(tdf, *args, **kwargs)
    # df = pd.read_html(url)

    # if isinstance(df, list):
    #     df = pd.concat(df)


    # df.columns = ["Properties", "Values"]
    # df = df.set_index("Properties").rename(index={"Audio features": "Audio"})

    # return df