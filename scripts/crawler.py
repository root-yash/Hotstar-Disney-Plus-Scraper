# import libraries
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import numpy as np
import nest_asyncio
nest_asyncio.apply()

class crawler:
    def __init__(self, link: str):
        self.links = set()
        asyncio.get_event_loop().run_until_complete(self.__crawler(link))
        domain = link[:link.find(".com")+4]
        self.links = self.__create_link( domain, list(self.links) )

    async def __crawler(self, link):
        """
        Crawl Through page and get every link
        """
        previous_html = 0
        browser = await launch()
        page = await browser.newPage()
        await page.goto(link)

        while True:
            html = await page.evaluate('''() => {
                return document.querySelector('.landing-page').innerHTML;
            }''')

            # parse html
            parsed_html = BeautifulSoup(html, 'html.parser')
            shows_html = parsed_html.find("div", {"class": "resClass"})

            if shows_html is not None:

                # break if previous html exists 
                if previous_html == len(shows_html):
                    break
                previous_html = len(shows_html)

                # get link
                for show in shows_html:
                    if show.find('a') != None:
                        self.links.add(show.find('a')['href'])
            else:
                # break if previous html exists 
                if previous_html == None:
                    break
                previous_html = None

            # scroll the page
            await page.evaluate('window.scroll(0, document.body.scrollHeight)')
            await asyncio.sleep(np.random.randint(5, 8))  # will wait to sending requests for 5 to 8 seconds
        await browser.close()

    def __create_link(self, domain, links):
        """
            Add Domain + link from links
        """
        for i in range(len(links)):
            links[i] = domain+links[i]
        return links
