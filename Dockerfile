FROM python:3.10-alpine

COPY . /app
WORKDIR /app

RUN apk update && apk add --virtual .build-deps gcc && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh","entrypoint.sh"]