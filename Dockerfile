
FROM python:3.13-slim

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED=True

COPY requirements.txt ./


# Install production dependencies.
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Copy over the Salesforce/blip-vqa-base model
#COPY blip-vqa-base ./
RUN pip install "huggingface_hub[hf_transfer]"
RUN mkdir blip-vqa-base
RUN huggingface-cli download Salesforce/blip-vqa-base --local-dir ./blip-vqa-base --exclude tf_model.h5 pytorch_model.bin

COPY main.py ./

# Run the web service on container startup.
# Use gunicorn webserver with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]
