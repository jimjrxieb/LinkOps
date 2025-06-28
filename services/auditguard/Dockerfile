FROM python:3.12-slim

WORKDIR /app

# Update all system packages to fix vulnerabilities including zlib1g
RUN apt-get update && apt-get upgrade -y && apt-get install -y --only-upgrade zlib1g

# Install system dependencies for security tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    gnupg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Trivy for vulnerability scanning
RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - \
    && echo deb https://aquasecurity.github.io/trivy-repo/deb buster main | tee -a /etc/apt/sources.list.d/trivy.list \
    && apt-get update \
    && apt-get install -y trivy

# Install Snyk CLI
RUN npm install -g snyk

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

EXPOSE 8007

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007"] 