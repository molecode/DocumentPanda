FROM python:3.7-slim
MAINTAINER info@timoschaepe.de

WORKDIR /src
COPY . /src
RUN pip install pipenv && pipenv install --system

EXPOSE 8000
VOLUME ["/src/data/"]

CMD python /src/manage.py migrate && python /src/manage.py runserver 0.0.0.0:8000
