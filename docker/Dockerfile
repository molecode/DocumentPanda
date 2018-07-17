FROM python:3.6.5-slim
MAINTAINER info@timoschaepe.de

WORKDIR /src
COPY . /src
RUN pip install pipenv && pipenv install --system

EXPOSE 8000
VOLUME ["/src/db.sqlite3"]

RUN python /src/manage.py migrate
CMD python /src/manage.py runserver 0.0.0.0:8000
