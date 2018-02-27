FROM python:3.6.4-slim
MAINTAINER timo@timoschaepe.de

WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt

EXPOSE 8000
VOLUME ["/src"]
