import sys
sys.path.append('src')
from hotstar import get_hotstar_data
from utils import dataframe_structuring
import json


if __name__ == "__main__":
    obj = get_hotstar_data()
    obj = None
    
    # load generated dictionary
    with open("temp/hotstar.json", "r") as f:
        json_dict = json.load(f)
        data_dict = json_dict["data_dict"]
        # as first episode contains when show started
        first_episode = json_dict["first_episode"]
    
    # remove empty values
    data_list = [([i] + list(data_dict[i].values())) for i in data_dict if type(data_dict[i]) == dict ]
    data_list = [i for i in data_list if len(i)>1]

    dataframe_structuring(data_list, first_episode)

    print("Output generated and saved in temp")
    
