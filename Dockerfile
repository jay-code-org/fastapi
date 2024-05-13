# Define the build stage
FROM python:3 as build
WORKDIR /usr/src/app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev && \
    pip install --no-cache-dir -r requirements.txt
 
# Define the runtime stage
FROM python:3-slim as runtime
WORKDIR /usr/src/app
# Copy installed packages from the build stage
COPY --from=build /usr/local /usr/local
# Copy your application code
COPY . .

RUN apt-get update && apt-get install -y libpq5 && \
    rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]