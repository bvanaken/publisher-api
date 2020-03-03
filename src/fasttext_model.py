import fasttext
import os

model_eng = None
model_de = None


def predict(text, lang):
    if lang == "de":
        model = model_de
    else:
        model = model_eng
    pred_prob = model.predict_proba([text])[0][0]

    predicted_label = pred_prob[0]
    probability = pred_prob[1]

    if predicted_label == "__label__nohate" or predicted_label == "__label__0":
        prediction = "nohate"
    elif predicted_label == "__label__hate" or predicted_label == "__label__1":
        prediction = "hate"
    else:
        prediction = "nohate"
        probability = 0

    return prediction, probability


def load_model(model_file):
    return fasttext.load_model(model_file, encoding='utf-8')


def init(model_dir):
    global model_eng
    global model_de

    model_file_eng = os.path.join(model_dir, "toxic_fasttext.bin")
    model_file_de = os.path.join(model_dir, "toxic_fasttext_de_v2.bin")

    model_eng = load_model(model_file_eng)
    model_de = load_model(model_file_de)
