# publisher-api
API and Demo for online user comment analysis

## Dependencies
See [requirements.txt](./src/requirements.txt)

## How to run
Run app within Kubernetes.
### Model files
* Store model files named 
  * `bert_large_toxic.bin`, 
  * `bert_config.json`, 
  * `toxic_fasttext.bin` and 
  * `toxic_fasttext_de.bin` 
in directory `${MODEL_DIR}` (must be accessible from container)
* Build docker image with `docker build --build-arg MODEL_DIR=${MODEL_DIR} -t ${...} .`

### Database
* Create a secret `nohate-mysql-secret` that holds the key `root_password` for the MySQL database
* Set up MYSQL with YAML files in [k8/mysql](./k8/mysql/)
* Create a database named `nohate` with a `comments` table as follows:

`CREATE DATABASE nohate;`

`CREATE TABLE comments(id INTEGER AUTO_INCREMENT PRIMARY KEY, text TEXT, date DATETIME, label INTEGER, lang TEXT, source TEXT);`

### Deploy
* Deploy app (and required services) with YAML files in [k8](./k8/)
