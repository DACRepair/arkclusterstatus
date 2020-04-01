FROM python:3.7-alpine

ENV BASE_URL "unix:///var/run/docker.sock"
ENV ARKCMD "arkmanager status"
ENV CFILTER "^.*$"

ENV THEME "darkly"
ENV HOST "0.0.0.0"
ENV PORT "8888"

WORKDIR /usr/src/app
COPY requirements.txt ./
COPY server.py ./
COPY templates ./templates/

RUN pip install -r requirements.txt

VOLUME /var/run/docker.sock
EXPOSE 8888

CMD ["python", "./server.py"]