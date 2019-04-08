# publisher-api
API for online user comment analysis

## Dependencies
* numpy 1.16.2
* torch 1.0.1
* Cython 0.29.6
* fasttext 0.8.3
* pytorch-pretrained-bert 0.6.1

## How to run
* Store model files named 
  * `bert_large_toxic.bin`, 
  * `bert_config.json`, 
  * `toxic_fasttext.bin` and 
  * `toxic_fasttext_de.bin` 
in `$MODEL_DIR`
- Run `app.py $MODEL_DIR`
