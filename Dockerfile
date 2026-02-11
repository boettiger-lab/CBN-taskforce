FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ /app/app/

# optional; metadata only
EXPOSE 7860

# optional; if you keep a healthcheck, make it use PORT
HEALTHCHECK CMD curl --fail http://localhost:${PORT:-7860}/_stcore/health || exit 1

# the real fix: bind to the port HF provides
ENTRYPOINT ["bash", "-lc", "streamlit run app/app.py --server.address=0.0.0.0 --server.port ${PORT:-7860}"]