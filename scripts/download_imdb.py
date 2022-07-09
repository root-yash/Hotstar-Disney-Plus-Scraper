import urllib.request
import os 
from utils import gz_extract

def download(link:str) -> bool:
    if not os.path.exists("temp"):
        os.mkdir("temp", mode = 1)
    urllib.request.urlretrieve(link, "temp/"+link.split("/")[-1])
    gz_extract("temp")
    return True