FROM python:3.12

WORKDIR /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["gunicorn", "server:app", "-b", "0.0.0.0:5555"]
