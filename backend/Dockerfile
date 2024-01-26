FROM python:3.10-slim

WORKDIR /calendar_backend
RUN mkdir img

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir --upgrade pip

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --reload
