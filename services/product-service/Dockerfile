FROM python:3

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "-w", "2", "-b", "0.0.0.0:3002", "--chdir", "services/product-service", "src.wsgi:app"]
