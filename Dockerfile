FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=src

CMD ["pytest", "--html=reports/report.html", "--self-contained-html"]
