import pandas as pd 
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 

def get_year(link: str) -> int:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser").find("p", {"class": "show-title"})
    try:
        year = soup.find_all("span")[-1].text.split(" ")[-1]
        year = int(year)
    except:
        year = 2022
    return year 

def fix_years_dataframe(dataframe: pd.DataFrame, first_episode:dict)->pd.DataFrame:
    id = list(dataframe[(dataframe.episodes.astype(float)>12) & (dataframe.year == "2022")].hotstar_id)
    id += list(dataframe[(dataframe.year.astype(str) == "not present")].hotstar_id)
    id = list(set(id))

    for i in tqdm(id):
        year = get_year(first_episode[i])
        index = dataframe[dataframe.hotstar_id == i].index.values[0]
        dataframe.loc[index, "year"] = str(year)
    return dataframe
