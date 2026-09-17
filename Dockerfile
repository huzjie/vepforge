FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY vepforge ./vepforge
COPY README.md LICENSE pyproject.toml ./

EXPOSE 8000

CMD ["python", "-m", "vepforge.cli.main", "serve", "--host", "0.0.0.0", "--port", "8000"]
