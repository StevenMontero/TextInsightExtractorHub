FROM python:3.8 AS base
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV SPACY_MODEL=es_core_news_lg
ENV PYTHONBUFFERED=1 SPACY_MODEL=$SPACY_MODEL
RUN python -m spacy download $SPACY_MODEL
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]
