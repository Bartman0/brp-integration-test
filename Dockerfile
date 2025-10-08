FROM python:3.13-slim-trixie

WORKDIR /root

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src

ENTRYPOINT [ "python3", "src/main.py" ]
