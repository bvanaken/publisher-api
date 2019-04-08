from pytorch_pretrained_bert.tokenization import BertTokenizer
import torch
from pytorch_pretrained_bert.modeling import BertForSequenceClassification, BertConfig
import os

bert_model = "bert-large-cased"
num_labels = 2
max_seq_length = 200


class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text, label=None):
        self.guid = guid
        self.text = text
        self.label = label


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids, input_mask, segment_ids):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids


def load_model(model_file, model_config_file):
    # Load a trained model and config that have been fine-tuned
    config = BertConfig(model_config_file)
    model = BertForSequenceClassification(config, num_labels=num_labels)
    model.load_state_dict(torch.load(model_file, map_location='cpu'))
    return model


def tokenize(text):
    eval_example = InputExample(guid=0, text=text)

    eval_features = convert_example_to_features(eval_example, max_seq_length, tokenizer)

    input_ids = torch.tensor([eval_features.input_ids], dtype=torch.long)
    input_mask = torch.tensor([eval_features.input_mask], dtype=torch.long)
    segment_ids = torch.tensor([eval_features.segment_ids], dtype=torch.long)

    return input_ids, input_mask, segment_ids


def predict(text):
    input_features = tokenize(text)

    with torch.no_grad():
        logits = model(input_features[0], input_features[1], input_features[2])

        _, indices = torch.max(logits, 1)

        prediction = indices.item()

        softmax_result = softmax(logits)
        probability = softmax_result[0][prediction].item()

        return prediction, probability


def convert_example_to_features(example, max_seq_length, tokenizer):
    """Loads a data file into an `InputBatch`."""

    tokens = tokenizer.tokenize(example.text)

    # Account for [CLS] and [SEP] with "- 2"
    if len(tokens) > max_seq_length - 2:
        tokens = tokens[:(max_seq_length - 2)]

    tokens = ["[CLS]"] + tokens + ["[SEP]"]
    segment_ids = [0] * len(tokens)

    input_ids = tokenizer.convert_tokens_to_ids(tokens)

    # The mask has 1 for real tokens and 0 for padding tokens. Only real
    # tokens are attended to.
    input_mask = [1] * len(input_ids)

    # Zero-pad up to the sequence length.
    padding = [0] * (max_seq_length - len(input_ids))
    input_ids += padding
    input_mask += padding
    segment_ids += padding

    assert len(input_ids) == max_seq_length
    assert len(input_mask) == max_seq_length
    assert len(segment_ids) == max_seq_length

    print("*** Example ***")
    print("tokens: %s" % " ".join([str(x) for x in tokens]))
    print("input_ids: %s" % " ".join([str(x) for x in input_ids]))
    print("input_mask: %s" % " ".join([str(x) for x in input_mask]))
    print("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))

    return InputFeatures(input_ids=input_ids,
                         input_mask=input_mask,
                         segment_ids=segment_ids)


def init(model_dir):
    global model
    global tokenizer
    global softmax

    model_config_file = os.path.join(model_dir, "bert_config.json")
    model_file = os.path.join(model_dir, "bert_large_toxic.bin")

    softmax = torch.nn.Softmax(dim=1)
    tokenizer = BertTokenizer.from_pretrained(bert_model, do_lower_case=False)

    model = load_model(model_file, model_config_file)
    model.eval()
