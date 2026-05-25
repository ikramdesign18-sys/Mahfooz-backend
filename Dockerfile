# 1. Use a stable, clean Python environment
FROM python:3.10-slim

# 2. Prevent Python from buffering logs (so you can see errors instantly)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install the raw Linux system libraries your medical scanner needs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 4. Create the application directory
WORKDIR /app

# 5. Clean install requirements without caching junk data
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy over your clean backend code
COPY . .

# 7. Open up port 8000
EXPOSE 8000

# 8. The bulletproof startup command.
# It uses standard straight quotes and tells Uvicorn to use PORT 8000.
# If Cloud Run injects a custom dynamic port variable ($PORT), it safely switches to it.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
