FROM python:3.12
RUN pip install django
ADD gifts_rec gifts_rec
WORKDIR gifts_rec
EXPOSE 8000
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000"]