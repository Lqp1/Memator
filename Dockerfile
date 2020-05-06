FROM python:3.6-buster
ADD . /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
CMD python3 memator.py
