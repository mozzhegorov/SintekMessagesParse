FROM arm32v7/python:3.8-buster

WORKDIR /home
RUN apt-get update
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python"]
CMD ["server.py"]