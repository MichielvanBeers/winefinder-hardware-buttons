FROM python:alpine3.16

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh","entrypoint.sh"]