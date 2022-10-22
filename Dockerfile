FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh","entrypoint.sh"]