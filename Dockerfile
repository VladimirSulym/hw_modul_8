FROM python:latest
WORKDIR /var/www/html

COPY requirements.txt .
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /var/www/html/staticfiles && chmod -R 755 /var/www/html/staticfiles
#    /var/www/html/media /var/www/html/static
COPY . .
