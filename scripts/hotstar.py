from all_link import get_link
import asyncio, os
from pyppeteer import launch
from bs4 import BeautifulSoup
import numpy as np
import nest_asyncio
nest_asyncio.apply()
from tqdm import tqdm
from utils import load_json_hotstar, save_json_hotstar
class get_hotstar_data:

    def __init__(self, link):
        self.data_dict = {}
        self.data_dict_location = "temp/hotstar.json"
        
        links = None
        if os.path.exists(self.data_dict_location):
            print("loading previous data")
            self.data_dict, links = load_json_hotstar(self.data_dict_location)

        if links is None:
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
        try:
            data_dict = {
                "description": show.find("div", {"class": "description"}).text.strip(),
                "genre": meta_data[2]
            }
            
            if flag == "movies":
                data_dict.update({"title": show.find("div", {"class": "toptitle clear-both"}).text.strip()})
                data_dict.update({"year": meta_data[1].split(" ")[0]})
                data_dict.update({"age_rating":meta_data[3]})
                data_dict.update({"running_time": meta_data[0]})

            else:
                data_dict.update({"title": show.find("h1", {"class": "toptitle clear-both"}).text.strip()})
                data_dict.update({"year": show.find_all("span",{"class": "action-dot"})[1].text.split(" ")[-1]})
                data_dict.update({"age_rating":meta_data[3]})
                data_dict.update({"seasons": meta_data[0].split(" ")[0]})
                data_dict.update({"episodes": meta_data[1].split(" ")[0]})
        except:
            if len(data_dict) < 5:
                data_dict = {}

        return data_dict

        
    async def get_hotstar_details(self, links: list):
        for i in tqdm(range(len(links))):
            type = links[i][links[i].find("/in/")+4:].split("/")[0]
            id = links[i].split("/")[-1]
            
            browser = await launch()
            page = await browser.newPage()
            await page.goto(links[i])

            if type != "movies":
                await asyncio.sleep(np.random.randint(1, 2))
            
            try:
                html = await page.evaluate('''() => {
                    return document.querySelector('.detail-page').innerHTML;
                }''')

                parsed_html = BeautifulSoup(html, 'html.parser')

                parsed_data = self.hotstar_data(parsed_html, type)
                self.data_dict.update({id: parsed_data})
            except:
                self.data_dict.update({id: None})

            if (i+1)%20 == 0 or len(links) == i+1:
                save_json_hotstar(self.data_dict, links[i+1:], self.data_dict_location)

            await page.close()
            await browser.disconnect()
            await browser.close()
