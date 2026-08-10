FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py .
COPY core/ core/

EXPOSE 8000

RUN python manage.py collectstatic --noinput

CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
