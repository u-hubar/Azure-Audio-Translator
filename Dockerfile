FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y \
    build-essential \
    libssl1.0.0 \
    libasound2 \
    python-dev \
    python3-pip

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

COPY . /app

CMD ["python3", "app.py"]