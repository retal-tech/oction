# pull official base image
FROM python:latest

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . .

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev netcat gettext

RUN pip install --upgrade pip && pip install  -r _prod/backend/requirements.txt

ENTRYPOINT ["_prod/backend/entrypoint.sh"]
