from all_link import get_link
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import numpy as np
import nest_asyncio
nest_asyncio.apply()
from tqdm import tqdm
class get_hotstar_data:

    def __init__(self, link):
        self.data_dict = {}
        obj_link = get_link(link)
        links = self.__remove_duplicate(obj_link.links_dict)
        obj_link = None
        print("________________Getting Information____________")
        asyncio.get_event_loop().run_until_complete(self.get_hotstar_details(links))

    def __remove_duplicate(self, link_dict: dict):
        links = ()
        for i in link_dict:
            links += link_dict[i]
        links_list = set(links)
        return list(links_list)

    def hotstar_data(self, show, flag: str) -> dict:
        """
            Given beautiful soup parsed data show it gives data from hotstar page according to flag being movies or tv
        """

        meta_data = [i.string for i in show.find_all("span", {"class": "meta-data"})]
        
        data_dict = {
            "description": show.find("div", {"class": "description"}).text.strip(),
            "genre": meta_data[2],
            "age_rating": meta_data[3]

        }
        
        if flag == "movies":
            data_dict.update({"title": show.find("div", {"class": "toptitle clear-both"}).text.strip()})
            data_dict.update({"running_time": meta_data[0]})
            data_dict.update({"year": meta_data[1].split(" ")[0]})

        else:
            data_dict.update({"title": show.find("h1", {"class": "toptitle clear-both"}).text.strip()})
            data_dict.update({"seasons": meta_data[0].split(" ")[0]})
            data_dict.update({"episodes": meta_data[1].split(" ")[0]})

        return data_dict

        
    async def get_hotstar_details(self, links: list):

        for i in tqdm(links):
            type = i[i.find("/in/")+4:].split("/")[0]
            id = i.split("/")[-1]
            
            browser = await launch()
            page = await browser.newPage()
            await page.goto(i)
            html = await page.evaluate('''() => {
                return document.querySelector('.detail-page').innerHTML;
            }''')

            parsed_html = BeautifulSoup(html, 'html.parser')

            parsed_data = self.hotstar_data(parsed_html, type)
            self.data_dict.update({id: parsed_data})
                
            await asyncio.sleep(np.random.randint(1, 3))
