FROM python:3.7

ADD ./src/ /app/

RUN pip install Cython --no-cache-dir --compile
RUN pip install -r /app/requirements.txt --no-cache-dir --compile

ARG MODEL_DIR=/models_dir
ENV MODEL_DIR=$MODEL_DIR

CMD python3 /app/app.py $MODEL_DIR