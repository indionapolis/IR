FROM python:3.7

WORKDIR /app

RUN pip install flask
RUN pip install redis
RUN pip install python-Levenshtein
RUN pip install soundex
RUN pip install nltk

COPY . .

CMD python app.py