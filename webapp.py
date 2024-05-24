from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from functools import lru_cache


app = Flask(__name__)


@lru_cache
def get_cities():
    df = pd.read_csv("hepsiemlak_cleaned.csv")
    cities = df["city"].unique().tolist()
    districts = {}
    neighborhoods = {}
    for city in cities:
        districts[city] = df[df["city"] == city]["district"].unique().tolist()
        neighborhoods[city] = {}
        for district in districts[city]:
            neighborhoods[city][district] = (
                df[(df["city"] == city) & (df["district"] == district)]["neighborhood"]
                .unique()
                .tolist()
            )
    return cities, districts, neighborhoods


@app.route("/")
def index():
    cities, districts, neighborhoods = get_cities()
    return render_template(
        "index.html", cities=cities, districts=districts, neighborhoods=neighborhoods
    )


if __name__ == "__main__":
    app.run(debug=True)
