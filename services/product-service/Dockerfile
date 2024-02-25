FROM python:3

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "services/product-service/src/main.py"]
