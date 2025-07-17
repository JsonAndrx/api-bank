FROM python:3.12.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--reload", "--port", "8000"]