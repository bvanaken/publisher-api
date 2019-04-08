import fasttext
import os

model_eng = None
model_de = None


def predict(text, lang):
    if lang == "de":
        model = model_de
    else:
        model = model_eng
    prediction = model.predict_proba([text])[0][0]
    print(prediction)
    return prediction[0].replace("__label__", ""), prediction[1]


def load_model(model_file):
    return fasttext.load_model(model_file, encoding='utf-8')


def init(model_dir):
    global model_eng
    global model_de

    model_file_eng = os.path.join(model_dir, "toxic_fasttext.bin")
    model_file_de = os.path.join(model_dir, "toxic_fasttext_de.bin")

    model_eng = load_model(model_file_eng)
    model_de = load_model(model_file_de)