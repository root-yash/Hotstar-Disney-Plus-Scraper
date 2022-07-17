import pandas as pd 
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 

def get_year(link: str) -> int:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser").find("p", {"class": "show-title"})
    year = soup.find_all("span")[-1].text.split(" ")[-1]
    try:
        year = int(year)
    except:
        year = 2022
    return year 

def fix_years_dataframe(dataframe: pd.DataFrame, first_episode:dict)->pd.DataFrame:
    id = list(dataframe[ (dataframe.episodes.astype(float)>12) & (dataframe.year == "2022") | (dataframe.year == None)].hotstar_id)
    year = {}
    for i in tqdm(id):
        year = get_year(first_episode[i])
        dataframe[dataframe.hotstar_id == i].year = str(year)
    return dataframe
