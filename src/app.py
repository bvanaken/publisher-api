from flask import Flask, request, jsonify, render_template
from utils import current_milli_time
import bert_model
import fasttext_model
import logging
import waitress
import os
import argparse

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=os.environ.get("LOGLEVEL", "INFO"))

logger = logging.getLogger(__name__)

base_route = "/nohate"

app = Flask(__name__)


@app.route(base_route + "/")
def index():
    return render_template("demo.html")


@app.route(base_route + "/predict", methods=['POST'])
def get_prediction():
    start_time = current_milli_time()

    data = request.get_json()

    input_text = data['query']

    model = data['model'] if 'model' in data else "ft"
    lang = data['lang'] if 'lang' in data else "eng"

    if model == "ft":
        prediction, probability = fasttext_model.predict(input_text, lang)
    elif model == "bert":
        prediction, probability = bert_model.predict(input_text)
    else:
        return

    logger.debug("prediction: {}".format(prediction))
    logger.debug("probability: {}".format(probability))

    end_time = current_milli_time()

    logger.debug("Execution time: {} ms".format(end_time - start_time))

    output = {
        'text': input_text,
        'prediction': str(prediction),
        'probability': probability
    }

    return jsonify(output)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_dir", help="directory where model files are stored")
    args = parser.parse_args()

    logger.debug("Init BERT model")
    bert_model.init(args.model_dir)

    logger.debug("Init FT model")
    fasttext_model.init(args.model_dir)

    logger.debug("Run app")
    waitress.serve(app.run("0.0.0.0", port=1337))


if __name__ == '__main__':
    run()
