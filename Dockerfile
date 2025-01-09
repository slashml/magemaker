FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    unzip \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your magemaker package
COPY . /app/

# Install package and dependencies
RUN pip install --no-cache-dir -e .

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm awscliv2.zip \
    && rm -rf aws

# Install Google Cloud SDK
RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-458.0.0-linux-x86_64.tar.gz -o google-cloud-sdk.tar.gz \
    && tar -xf google-cloud-sdk.tar.gz \
    && ./google-cloud-sdk/install.sh --quiet \
    && rm google-cloud-sdk.tar.gz

# Add Google Cloud SDK to PATH
ENV PATH $PATH:/app/google-cloud-sdk/bin

# Copy and setup entrypoint
COPY magemaker/docker/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
CMD ["bash"]