FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY pyproject.toml README.md ./
RUN pip install -U pip && pip install -e .[dev]
COPY . .
CMD ["python", "examples/00_minimal_qnode.py"]