FROM python:3.10.12-slim AS builder
RUN apt-get update && apt-get install -y git
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10.12-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin


COPY . .

EXPOSE 8000

CMD ["uvicorn", "step1_basic_api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]