FROM python:3-alpine3.8

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-u", "heat-level-checker.py"]
