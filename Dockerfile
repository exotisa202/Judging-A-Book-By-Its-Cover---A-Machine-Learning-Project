FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .
USER 65534:65534
CMD ["sh", "-c", "python cover_match.py --demo && python -m pytest -q"]
