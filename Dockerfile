FROM python:3.7

ADD src/ /app/

RUN pip install Cython --no-cache-dir --compile
RUN pip install -r requirements.txt --no-cache-dir --compile

CMD python3 /app/app.py