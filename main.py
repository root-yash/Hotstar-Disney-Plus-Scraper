import argparse 
import sys
sys.path.append('scripts')
from hotstar import get_hotstar_data
from utils import dataframe_structuring
import json

parser = argparse.ArgumentParser()
parser.add_argument("--weblink", type=str, help="weblink genre/language/channels", default="https://www.hotstar.com/in/genres")

arg = parser.parse_args()


if __name__ == "__main__":
    obj = get_hotstar_data(arg.weblink)
    obj = None

    # load generated dictionary
    with open("temp/hotstar.json", "r") as f:
        data_dict = json.load(f)["data_dict"]
    
    # remove empty values
    data_list = [([i] + list(data_dict[i].values())[0:6]) for i in data_dict if type(data_dict[i]) == dict ]
    data_list = [i for i in data_list if len(i)>1]
    
    dataframe_structuring(data_list)

    print("Output generated and saved in temp")
    
