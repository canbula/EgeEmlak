import os
import numpy as np
import pandas as pd


def get_files(folder, city):
    files = os.listdir(folder)
    print(files)
    input()
    return [f for f in files if f.endswith(".csv") and f.startswith(city)]


def read_files(folder, city, city_name):
    files = get_files(folder, city)
    dfs = [
        pd.read_csv(os.path.join(folder, file), header=None, skiprows=1)
        for file in files
    ]
    df = pd.concat(dfs, ignore_index=True)
    df["city"] = city_name
    return df


if __name__ == "__main__":
    cities = {
        "afyonkarahisar": "Afyonkarahisar",
        "aydin": "Aydın",
        "denizli": "Denizli",
        "izmir": "İzmir",
        "kutahya": "Kütahya",
        "manisa": "Manisa",
        "mugla": "Muğla",
        "usak": "Uşak",
    }
    folder = "data"
    df = pd.DataFrame()
    for city, city_name in cities.items():
        city_df = read_files(folder, city, city_name)
        print(city_df)
        input()
        df = pd.concat([df, city_df], ignore_index=True)
    print(df)
    df.to_csv(f"data.csv", index=False)
