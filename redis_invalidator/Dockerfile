FROM python:3.14.0a3-slim

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

COPY . /app/

CMD ["python", "trigger_listener.py"]