FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY script.py .

COPY templates/ ./templates
COPY files/ ./files

EXPOSE 5000

CMD ["python3", "script.py"]
