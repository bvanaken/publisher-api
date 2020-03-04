FROM python:3.7

COPY ./src/requirements.txt /app/requirements.txt

RUN pip install Cython --no-cache-dir --compile
RUN pip install -r /app/requirements.txt --no-cache-dir --compile

ARG MODEL_DIR=/models_dir
ENV MODEL_DIR=$MODEL_DIR

ADD ./src/ /app/

CMD python3 /app/app.py $MODEL_DIR