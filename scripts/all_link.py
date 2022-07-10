from crawler import crawler

class get_link:
    def __init__(self, link: str):
        print("Starting....")
        links = self.links_producer(link)
        self.links_dict = self.page_link(links)

    def links_producer(self, link: str) -> list:
        hot_obj = crawler(link)
        return hot_obj.links
    
    def genre(self, link: str) -> str:
        return link.split('/')[-1]

    def page_link(self, links: list) -> dict:
        link_dict = {}
        for i in links:
            genre = self.genre(i)
            print("Getting", genre)
            link_dict[genre] = tuple(self.links_producer(i))
        return link_dict