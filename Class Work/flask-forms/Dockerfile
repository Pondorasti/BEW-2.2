FROM python:3.7-slim-buster

ADD . /app

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV SQLALCHEMY_DATABASE_URI=sqlite:///database.db
ENV SECRET_KEY=xq9YLa6EKV

EXPOSE 5000

CMD python app.py