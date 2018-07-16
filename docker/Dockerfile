FROM python:3.6.5-slim
MAINTAINER timo@timoschaepe.de

WORKDIR /src
COPY Pipfile /src/
COPY Pipfile.lock /src/
RUN pip install pipenv
RUN pipenv install --system

EXPOSE 8000
VOLUME ["/src"]
