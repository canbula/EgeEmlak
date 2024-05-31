from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from functools import lru_cache
import joblib
import sys
import os
import io


app = Flask(__name__)


sys.path.insert(0, os.path.dirname(__file__))
old_stdout = sys.stdout
new_stdout = io.StringIO()
sys.stdout = new_stdout


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
    # cities, districts, neighborhoods = get_cities()
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
    regression_model = joblib.load("model_regression.pkl")
    prediction = regression_model.predict(user_input)
    # return jsonify({"price": round(prediction[0])})
    classification_model = joblib.load("model_classification.pkl")
    prediction_class = classification_model.predict(user_input)
    return jsonify({"price": round(prediction[0]), "class": prediction_class[0]})


if __name__ == "__main__":
    app.run()
