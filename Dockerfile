# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

COPY . .

# Stage 2: Runner

FROM python:3.12-slim as runner

WORKDIR /app

RUN apt-get update && \
    apt-get install -y firefox-esr && \
    apt-get install -y wget && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.31.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    apt-get purge --auto-remove -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /app /app

# Переменная для безголовного режима для Firefox
ENV DISPLAY=:99

CMD ["python", "main.py"]