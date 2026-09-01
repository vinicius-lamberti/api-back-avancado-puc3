FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/data

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
	&& addgroup --system appgroup \
	&& adduser --system --ingroup appgroup appuser
COPY app ./app
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
