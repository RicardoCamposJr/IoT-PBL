FROM python

COPY . ./app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8888
EXPOSE 8889/udp
EXPOSE 8082

CMD ["python", "broker.py"]