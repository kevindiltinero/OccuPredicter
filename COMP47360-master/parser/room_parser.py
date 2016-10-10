import pandas as pd
import MySQLdb

def parse_room(csv):

    print "Extracting Room Data..."
    df = pd.read_csv(csv, engine="python", names=["Time", "Room", "Capacity", "Occupied", "Occupancy", "Date", "Timestamp", "Type"])
    df2 = df.iloc[1:,[1,2,7]]
    df2.drop_duplicates(keep="first", inplace=True, subset=df.columns[1])
    #room_list = [df2.iloc[x][0] for x in range(df2.shape[0])]
    return df2

def room_to_csv(dataframe):
    dataframe.to_csv("./data/Cleaned_Data/room_info.csv", index=False)
    print "Room Data successfully extracted."
    return

if __name__ == "__main__":
    room_to_csv(parse_room("./data/Cleaned_Data/Cleaned_Ground_Data.csv"))
