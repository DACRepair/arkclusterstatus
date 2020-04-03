FROM python:3.7-alpine

ENV WEB__DEBUG "false"
ENV WEB__HOST "0.0.0.0"
ENV WEB__PORT "8888"
ENV WEB__THEME "darkly"
ENV WEB__CACHE

ENV DOCKER__URL "unix:///var/run/docker.sock"
ENV ARK__FILTER "^.*$"
ENV ARK__COMMAND "arkmanager status"
ENV ARK__TIMEOUT 30


WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY server.py ./
COPY templates ./templates/
COPY ArkClusterStatus ./ArkClusterStatus/

VOLUME /var/run/docker.sock
EXPOSE 8888

CMD ["python", "./server.py"]