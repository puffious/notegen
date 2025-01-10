FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY gemini.py captions.py main.py ./
RUN adduser --disabled-password --no-create-home appuser
USER appuser
ENV PYTHONOPTIMIZE=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]