FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libffi-dev curl build-essential

RUN pip install --upgrade pip
RUN pip install uv

WORKDIR /app

COPY . .

RUN uv venv .venv
RUN uv pip install -r requirements.txt

CMD ["uv", "run", "app.py"]