FROM python:3-slim

LABEL maintainer Jossec101(jossec101@protonmail.com)

RUN pip install sshtunnel

WORKDIR /root

COPY ./__main__.py __main__.py

RUN chmod +x __main__.py

CMD [ "python","-u", "__main__.py" ]