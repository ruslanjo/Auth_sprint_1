FROM python:3.10.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

COPY requirements.txt /tmp/
RUN pip install --upgrade pip && pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app/src

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1

ENTRYPOINT ["python", "/app/src/main.py"]