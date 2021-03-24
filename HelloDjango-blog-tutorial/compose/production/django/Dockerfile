FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update \
  # Pillow dependencies
  && apk add jpep-dev zlib-dev freetype-dev lcms2-dev openjpep-dev tiff-dev tk-dev tcl-dev

WORKDIR /app

RUN pip install pipenv -i https://pypi.douban.com/simple

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app

COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh