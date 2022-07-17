import json
import pandas as pd 
from fix_years import fix_years_dataframe
       
def save_json_hotstar(data_dict, links, file_name: str, first_episode) -> None:
    json_dict = {"data_dict": data_dict, "links": links, "first_episode": first_episode}
    with open(file_name, "w") as f:
        json.dump(json_dict, f)

def load_json_hotstar(file_name: str):
    with open(file_name, "r") as f:
        json_dict = json.load(f)
    return json_dict["data_dict"], json_dict["links"], json_dict["first_episode"]

def dataframe_structuring(data_list: list, first_episode: dict)->None:
    """
        List of data and this function will structure that and save it as csv
    """
    # dataframe structure
    data_dict = {
        "hotstar_id":[],
        "title":[], 
        "description":[],
        "genre":[], "year":[],
        "age_rating":[], 
        "running_time":[],
        "seasons":[],
        "episodes":[],
        "type":[],
    }
    # loop through data list 
    for i in data_list:
        # common data between movie and tv 
        data_dict["hotstar_id"].append(i[0])
        data_dict["description"].append(i[1])
        data_dict["genre"].append(i[2])
        data_dict["title"].append(i[3])
        data_dict["year"].append(i[4])
        data_dict["age_rating"].append(i[5])

        # uncommon data between those 
        try:
            # check if it is season which means that it is tv show
            int(i[6])
            data_dict["type"].append("tv")
            data_dict["seasons"].append(int(i[6]))
            try:
                data_dict["episodes"].append(int(i[7]))
            except:
                data_dict["episodes"].append(None)

            data_dict["running_time"].append("np")
        except:
            data_dict["type"].append("movie")
            
            # convert hour to min
            time = i[6].split(" ")
            try:
                if time[1] == "hr":
                    time_t = int(time[0]) * 60 
                    try:
                        time_t += int(time[2])
                    except:
                        pass
                    time = time_t
                else:
                    time = int(time[0])
                data_dict["running_time"].append(time)
            except:
                data_dict["running_time"].append(None)
            data_dict["seasons"].append("np")
            data_dict["episodes"].append("np")
    
    # save dataframe 
    df = pd.DataFrame(data_dict)
    df.dropna(inplace = True)
    df.replace("np", None, inplace= True)
    df = fix_years_dataframe(df,first_episode)
    df.replace("not present", None, inplace= True)
    df.to_csv("temp/hotstar.csv", index= False)