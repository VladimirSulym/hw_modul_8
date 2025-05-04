FROM python:latest
WORKDIR /hw_modul_8

COPY requirements.txt .
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
