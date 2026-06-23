# FROM python:3.12-slim
# WORKDIR /app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# CMD ["python3", "manage.py", "runserver"]

# stage 1:
FROM python:3.12-slim AS builder
WORKDIR /build

# --- ADD THIS SECTION ---
# Install system tools needed to compile mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
# ------------------------

COPY requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt 
# RUN pip install --no-cache-dir -r requirements.txt


# stage 2:
FROM python:3.12-slim
WORKDIR /app

# We still need the runtime C library for MySQL, but NOT the compilers
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*


COPY --from=builder /build/wheels /app/wheels
COPY --from=builder /build/requirements.txt /app/

# RUN pip install --no-cache-dir -r /app/wheels/*


# 2. FIX: Read the text file, but pull the installations from your wheels cache folder
RUN pip install --no-cache-dir --no-index --find-links=/app/wheels -r /app/requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]