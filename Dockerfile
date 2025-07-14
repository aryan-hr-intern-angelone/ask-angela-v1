FROM python:3.11-slim

RUN pip install --upgrade pip
RUN pip install uv

WORKDIR /app

COPY . .

RUN uv venv .venv
RUN uv pip install -r requirements.txt

CMD ["uv", "run", "app.py"]