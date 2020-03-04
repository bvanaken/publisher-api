from flask import Flask, request, jsonify, render_template, abort
from utils import current_milli_time, old_api_version
import bert_model
import fasttext_model
import logging
import waitress
import os
import argparse
import db
import urllib.parse

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=os.environ.get("LOGLEVEL", "INFO"))

logger = logging.getLogger(__name__)

sources = ["demo_app", "browser", "errudite"]
sources_for_db = ["demo_app", "browser"]
base_route = ""
db_connected = False

app = Flask(__name__)


@app.route(base_route + "/")
def index():
    return render_template("demo.html")


@app.route(base_route + "/predict", methods=['POST'])
def get_prediction():
    start_time = current_milli_time()

    data = request.get_json()

    if old_api_version(data):
        return get_prediction_v1(data)

    if "query" not in data:
        abort(400, {'message': 'No query defined.'})

    if "source" not in data or data["source"] not in sources:
        abort(400, {'message': 'Source invalid.'})

    input_text = data['query']

    # decode input text
    input_text = urllib.parse.unquote_plus(input_text)

    model = data['model'] if 'model' in data else "ft"
    lang = data['lang'] if 'lang' in data else "eng"

    if lang != "eng" and lang != "de":
        abort(400, {'message': 'Language currently not supported.'})

    if data["source"] in sources_for_db:
        comment_id = db.insert_comment(input_text, lang) if db_connected else -1
    else:
        comment_id = -1

    if model == "ft":
        prediction, probability = fasttext_model.predict(input_text, lang)
    elif model == "bert":
        prediction, probability = bert_model.predict(input_text, lang)
    else:
        abort(400, {'message': 'Model name unknown.'})

    logger.debug("prediction: {}".format(prediction))
    logger.debug("probability: {}".format(probability))

    end_time = current_milli_time()

    logger.debug("Execution time: {} ms".format(end_time - start_time))

    output = {
        'text': input_text,
        'prediction': str(prediction),
        'probability': probability,
        'comment_id': comment_id,
        'lang': lang,
        'model': model
    }

    return jsonify(output)


def get_prediction_v1(data):
    start_time = current_milli_time()

    if "query" not in data:
        abort(400, {'message': 'No query defined.'})

    input_text = data['query']

    # decode input text
    input_text = urllib.parse.unquote_plus(input_text)

    model = data['model'] if 'model' in data else "ft"
    lang = data['lang'] if 'lang' in data else "eng"

    if lang != "eng" and lang != "de":
        abort(400, {'message': 'Language currently not supported.'})

    comment_id = db.insert_comment(input_text, lang) if db_connected else -1

    if model == "ft":
        prediction, probability = fasttext_model.predict(input_text, lang)
    elif model == "bert":
        prediction, probability = bert_model.predict(input_text, lang)
    else:
        return

    logger.debug("prediction: {}".format(prediction))
    logger.debug("probability: {}".format(probability))

    end_time = current_milli_time()

    logger.debug("Execution time: {} ms".format(end_time - start_time))

    output = {
        'text': input_text,
        'prediction': str(prediction),
        'probability': probability,
        'comment_id': comment_id
    }

    return jsonify(output)


@app.route(base_route + "/label", methods=['POST'])
def update_label():
    data = request.get_json()

    comment_id = data['comment_id']
    label = data['label']

    if db_connected:
        comment_id = db.update_comment(comment_id, label)
    else:
        comment_id = -1
        logger.debug("DB not connected. Label update not possible.")

    output = {
        'comment_id': comment_id,
        'label': label
    }

    return jsonify(output)


def run():
    global db_connected

    parser = argparse.ArgumentParser()
    parser.add_argument("model_dir", help="directory where model files are stored")
    args = parser.parse_args()

    logger.debug("Init BERT model")
    bert_model.init(args.model_dir)

    logger.debug("Init FT model")
    fasttext_model.init(args.model_dir)

    logger.debug("Connect to DB")
    db_connected = db.init()

    logger.debug("Run app")
    waitress.serve(app.run("0.0.0.0", port=1337))


if __name__ == '__main__':
    run()
