import requests
from bs4 import BeautifulSoup
class all_links:
    def __init__(self):
        print("Starting Getting Links")
        self.show = "https://www.hotstar.com/in/new-sitemap-SHOWS-1.xml"
        self.movies = "https://www.hotstar.com/in/new-sitemap-MOVIE-1.xml"
        self.year = "https://www.hotstar.com/in/new-sitemap-EPISODE-{}.xml"
        self.episode = [1,2,3,4,5,6]

    def __show_movie(self, link:str) -> list:
        """
        Input: link of xml file
        output: list of all the links
        """
        links = set()
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in soup.find_all("loc"):
            links.add(i.text)
        return list(links)
    
    def __first_episode(self, link:str, hash_map: dict) -> dict:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in soup.find_all("loc"):
            link = i.text
            show_id = link.split("/")[-3]
            hash_map[show_id] = hash_map.get(show_id, link)
        return hash_map

    def get_links(self) -> dict:
        """
        give dict with movie_show and first_episode
        """
        movie_link = self.__show_movie(self.movies)
        show_link = self.__show_movie(self.show)

        first_episode = {}
        for i in self.episode:
            first_episode = self.__first_episode(self.year.format(i), first_episode)
        movie_show = movie_link + show_link
        
        return {"movie_show": movie_show, "first_episode": first_episode}
        
