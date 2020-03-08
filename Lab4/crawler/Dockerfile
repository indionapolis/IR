FROM python:3.7

WORKDIR /app

RUN pip install nltk
RUN pip install beautifulsoup4
RUN pip install redis
RUN pip install soundex

COPY . .

CMD python main.py