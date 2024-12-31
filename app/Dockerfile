FROM python:3.14.0a3-slim

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]