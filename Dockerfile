# Dockerfile for running a Streamlit app with ctransformers and a pre-downloaded GGUF model
# 1) Base image
FROM python:3.10

# 2) System dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends git-lfs \
 && git-lfs install \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3) Python dependencies
COPY requirements.txt /app/requirements.txt
# Install Python dependencies, including ctransformers
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy pre‑downloaded GGUF model into ctransformers cache
COPY mistral-7b-instruct-v0.1.Q6_K.gguf \
     /root/.cache/ctransformers/models/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q6_K.gguf

# 5) Copy application code
COPY mistral.py /app/mistral.py

# 6) Expose port and run
EXPOSE 8000
CMD ["streamlit", "run", "mistral.py", "--server.port=8000"]