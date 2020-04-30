import os

import requests


def predict_target(text):
    response = requests.get(os.environ['GERMAN_TARGET_URL'] + "/predict?sentence=" + text)

    result = response.json()

    prediction = result["class"]
    probability = float(result["probability"])

    return prediction, probability
