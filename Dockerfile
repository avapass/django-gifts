FROM python:3.12
RUN apt-get update && apt-get install build-essential graphviz graphviz-dev --assume-yes
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD gifts_rec gifts_rec
WORKDIR gifts_rec
EXPOSE 8000
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000"]