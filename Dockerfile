FROM arm32v7/python:3.8-buster

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]