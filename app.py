from flask import Flask, request, jsonify
from utils import current_milli_time
import bert_model
import fasttext_model

app = Flask(__name__)


@app.route("/")
def index():
    return '''
        <html>
            <body>
                <form action = "http://localhost:1337/predict" method = "post">
                    <p> Eingabe: </p>
                    <p> <input type = "text" name = "input" /></p>
                    <p> <input type = "submit" value = "submit" /></p>
                </form>
            </body>
        <html>
    '''


@app.route("/predict", methods=['POST'])
def get_prediction():
    start_time = current_milli_time()
    input_text = request.form['input']

    ft_prediction, ft_probability = fasttext_model.predict(input_text)
    # bert_prediction, bert_probability = bert_model.predict(input_text)

    print("FASTTEXT prediction: {}".format(ft_prediction))
    print("FASTTEXT probability: {}".format(ft_probability))

    # print("BERT prediction: {}".format(bert_prediction))
    # print("BERT probability: {}".format(bert_probability))

    end_time = current_milli_time()

    print("Execution time: {} ms".format(end_time - start_time))

    output = {
        'prediction': ft_prediction,
        'probability': ft_probability
    }

    return jsonify(output)


if __name__ == '__main__':
    app.run("0.0.0.0", port=1337)
