from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from functools import lru_cache
import pickle
import joblib


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


@app.route("/predict", methods=["POST"])
def predict():
    cities, districts, neighborhoods = get_cities()
    city = request.form["city"]
    district = request.form["district"]
    neighborhood = request.form["neighborhood"]
    room = int(request.form["room"])
    living_room = int(request.form["living_room"])
    area = int(request.form["area"])
    age = int(request.form["age"])
    floor = int(request.form["floor"])
    user_input = pd.DataFrame(
        {
            "city": [city],
            "district": [district],
            "neighborhood": [neighborhood],
            "room": [room],
            "living_room": [living_room],
            "area": [area],
            "age": [age],
            "floor": [floor],
        }
    )
    print(user_input)
    model = joblib.load("hepsiemlak_model.pkl")
    prediction = model.predict(user_input)
    print(prediction)


if __name__ == "__main__":
    app.run(debug=True)
