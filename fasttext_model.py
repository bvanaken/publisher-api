import fasttext

model_file = "models/toxic_fasttext.bin"


def predict(text):
    prediction = model.predict_proba([text])[0][0]
    print(prediction)
    return prediction[0].replace("__label__", ""), prediction[1]


def load_model():
    return fasttext.load_model(model_file, encoding='utf-8')


model = load_model()
