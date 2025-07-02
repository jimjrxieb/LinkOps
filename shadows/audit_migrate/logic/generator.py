import os
from typing import Dict, Any, List


class ServiceGenerator:
    def __init__(self):
        self.base_dir = "/app/generated_services"
        self.templates = self._load_templates()

    async def generate_services(self, plan) -> Dict[str, Any]:
        """Generate all services from the scaffold plan"""
        os.makedirs(self.base_dir, exist_ok=True)

        generated_services = []
        generated_files = {}
        errors = []

        for service_config in plan.services_to_generate:
            try:
                service_name = service_config.get("name", "unknown-service")
                _ = service_config.get(
                    "type", "microservice"
                )  # service_type used for future enhancement

                # Create service directory
                service_dir = os.path.join(self.base_dir, service_name)
                os.makedirs(service_dir, exist_ok=True)

                # Generate service structure
                files_created = await self._generate_service_structure(
                    service_dir, service_name, service_config
                )

                generated_services.append(service_name)
                generated_files[service_name] = files_created

            except Exception as e:
                errors.append(
                    f"Failed to generate {service_config.get('name', 'unknown')}: "
                    f"{str(e)}"
                )

        return {
            "status": (
                "✅ Migration completed successfully"
                if not errors
                else "⚠️ Migration completed with errors"
            ),
            "services_generated": generated_services,
            "output_directory": self.base_dir,
            "generated_files": generated_files,
            "errors": errors,
        }

    async def _generate_service_structure(
        self, service_dir: str, service_name: str, config: Dict[str, Any]
    ) -> List[str]:
        """Generate complete service structure"""
        files_created = []

        # Create main directories
        directories = [
            "routers",
            "models",
            "services",
            "utils",
            "tests",
            "helm",
            ".github/workflows",
        ]

        for directory in directories:
            dir_path = os.path.join(service_dir, directory)
            os.makedirs(dir_path, exist_ok=True)

        # Generate main.py
        main_content = self._generate_main_py(service_name, config)
        main_file = os.path.join(service_dir, "main.py")
        with open(main_file, "w") as f:
            f.write(main_content)
        files_created.append("main.py")

        # Generate Dockerfile
        docker_content = self._generate_dockerfile(service_name, config)
        docker_file = os.path.join(service_dir, "Dockerfile")
        with open(docker_file, "w") as f:
            f.write(docker_content)
        files_created.append("Dockerfile")

        # Generate requirements.txt
        requirements_content = self._generate_requirements_txt(config)
        requirements_file = os.path.join(service_dir, "requirements.txt")
        with open(requirements_file, "w") as f:
            f.write(requirements_content)
        files_created.append("requirements.txt")

        # Generate router
        router_content = self._generate_router(service_name)
        router_file = os.path.join(service_dir, "routers", "main_router.py")
        with open(router_file, "w") as f:
            f.write(router_content)
        files_created.append("routers/main_router.py")

        # Generate __init__.py files
        init_files = [
            "routers/__init__.py",
            "models/__init__.py",
            "services/__init__.py",
            "utils/__init__.py",
            "tests/__init__.py",
        ]

        for init_file in init_files:
            init_path = os.path.join(service_dir, init_file)
            with open(init_path, "w") as f:
                f.write(f"# {service_name} {init_file.split('/')[0]} package\n")
            files_created.append(init_file)

        # Generate Helm chart
        helm_files = self._generate_helm_chart(service_dir, service_name, config)
        files_created.extend(helm_files)

        # Generate GitHub workflow
        workflow_content = self._generate_github_workflow(service_name)
        workflow_file = os.path.join(
            service_dir, ".github", "workflows", f"{service_name}-ci.yml"
        )
        with open(workflow_file, "w") as f:
            f.write(workflow_content)
        files_created.append(f".github/workflows/{service_name}-ci.yml")

        # Generate README
        readme_content = self._generate_readme(service_name, config)
        readme_file = os.path.join(service_dir, "README.md")
        with open(readme_file, "w") as f:
            f.write(readme_content)
        files_created.append("README.md")

        return files_created

    def _generate_main_py(self, service_name: str, config: Dict[str, Any]) -> str:
        """Generate main.py for the service"""
        service_type = config.get("type", "microservice")

        if service_type == "gateway":
            return f"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import main_router

app = FastAPI(
    title="{service_name.title()}",
    description="API Gateway Service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router.router)

@app.get("/health")
async def health_check():
    return {{"status": "healthy", "service": "{service_name}"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
        else:
            return f"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import main_router

app = FastAPI(
    title="{service_name.title()}",
    description="{service_type.title()} Service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router.router)

@app.get("/health")
async def health_check():
    return {{"status": "healthy", "service": "{service_name}"}}

@app.get("/")
async def root():
    return {{"message": "Hello from {service_name}", "type": "{service_type}"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

    def _generate_dockerfile(self, service_name: str, config: Dict[str, Any]) -> str:
        """Generate Dockerfile for the service"""
        docker_config = config.get("docker", {})
        base_image = docker_config.get("base_image", "python:3.10-slim")
        ports = docker_config.get("ports", [8000])
        port_str = " ".join(map(str, ports))

        return f"""FROM {base_image}

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE {port_str}

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{ports[0]}/health || exit 1

# Run the application
CMD ["python", "main.py"]
"""

    def _generate_requirements_txt(self, config: Dict[str, Any]) -> str:
        """Generate requirements.txt for the service"""
        service_type = config.get("type", "microservice")

        base_requirements = [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "pydantic>=2.0.0",
            "requests>=2.31.0",
        ]

        if service_type == "gateway":
            base_requirements.extend(["httpx>=0.25.0", "python-multipart>=0.0.6"])
        elif service_type == "microservice":
            base_requirements.extend(
                ["sqlalchemy>=2.0.0", "alembic>=1.12.0", "psycopg2-binary>=2.9.0"]
            )

        return "\n".join(base_requirements)

    def _generate_router(self, service_name: str) -> str:
        """Generate main router for the service"""
        return f'''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/api/v1", tags=["{service_name.title()}"])

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="{service_name}",
        version="1.0.0"
    )

@router.get("/")
async def root():
    """Root endpoint"""
    return {{"message": "Welcome to {service_name} API", "version": "1.0.0"}}

# Add your service-specific endpoints here
@router.get("/example")
async def example_endpoint():
    """Example endpoint - replace with actual business logic"""
    return {{"message": "This is an example endpoint for {service_name}"}}
'''

    def _generate_helm_chart(
        self, service_dir: str, service_name: str, config: Dict[str, Any]
    ) -> List[str]:
        """Generate Helm chart for the service"""
        helm_config = config.get("helm", {})
        chart_name = helm_config.get("chart_name", service_name)
        _ = helm_config.get(
            "namespace", service_name
        )  # namespace used for future enhancement
        resources = helm_config.get("resources", {"cpu": "500m", "memory": "512Mi"})

        files_created = []

        # Chart.yaml
        chart_yaml = f"""apiVersion: v2
name: {chart_name}
description: Helm chart for {service_name}
type: application
version: 0.1.0
appVersion: "1.0.0"
"""
        chart_file = os.path.join(service_dir, "helm", "Chart.yaml")
        with open(chart_file, "w") as f:
            f.write(chart_yaml)
        files_created.append("helm/Chart.yaml")

        # values.yaml
        values_yaml = f"""# Default values for {chart_name}
replicaCount: 1

image:
  repository: {service_name}
  tag: "latest"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

resources:
  limits:
    cpu: {resources.get('cpu', '500m')}
    memory: {resources.get('memory', '512Mi')}
  requests:
    cpu: 250m
    memory: 256Mi

env:
  - name: ENVIRONMENT
    value: "production"
  - name: LOG_LEVEL
    value: "INFO"

ingress:
  enabled: false
  className: ""
  annotations: {{}}
  hosts:
    - host: {service_name}.local
      paths:
        - path: /
          pathType: Prefix
"""
        values_file = os.path.join(service_dir, "helm", "values.yaml")
        with open(values_file, "w") as f:
            f.write(values_yaml)
        files_created.append("helm/values.yaml")

        # deployment.yaml
        deployment_yaml = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  labels:
    app: {service_name}
spec:
  replicas: {{{{ .Values.replicaCount }}}}
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
    spec:
      containers:
      - name: {service_name}
        image: "{{{{ .Values.image.repository }}}}:{{{{ .Values.image.tag }}}}"
        imagePullPolicy: {{{{ .Values.image.pullPolicy }}}}
        ports:
        - containerPort: 8000
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          {{{{ toYaml .Values.resources | nindent 12 }}}}
        env:
          {{{{ toYaml .Values.env | nindent 12 }}}}
"""
        deployment_file = os.path.join(
            service_dir, "helm", "templates", "deployment.yaml"
        )
        os.makedirs(os.path.dirname(deployment_file), exist_ok=True)
        with open(deployment_file, "w") as f:
            f.write(deployment_yaml)
        files_created.append("helm/templates/deployment.yaml")

        # service.yaml
        service_yaml = f"""apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  labels:
    app: {service_name}
spec:
  type: {{{{ .Values.service.type }}}}
  ports:
    - port: {{{{ .Values.service.port }}}}
      targetPort: {{{{ .Values.service.targetPort }}}}
      protocol: TCP
      name: http
  selector:
    app: {service_name}
"""
        service_file = os.path.join(service_dir, "helm", "templates", "service.yaml")
        with open(service_file, "w") as f:
            f.write(service_yaml)
        files_created.append("helm/templates/service.yaml")

        return files_created

    def _generate_github_workflow(self, service_name: str) -> str:
        """Generate GitHub Actions workflow for the service"""
        return f"""name: {service_name.title()} CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{{{ github.repository }}}}/{service_name}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-asyncio

    - name: Run tests
      run: |
        pytest tests/ -v

    - name: Run linting
      run: |
        pip install flake8 black
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        black . --check

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write
    steps:
    - uses: actions/checkout@v4

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{{{ env.REGISTRY }}}}
        username: ${{{{ github.actor }}}}
        password: ${{{{ secrets.GITHUB_TOKEN }}}}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{{{ steps.meta.outputs.tags }}}}
        labels: ${{{{ steps.meta.outputs.labels }}}}
"""

    def _generate_readme(self, service_name: str, config: Dict[str, Any]) -> str:
        """Generate README.md for the service"""
        service_type = config.get("type", "microservice")

        return f"""# {service_name.title()}

A {service_type} service generated by AuditMigrate.

## Quick Start

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the service:
   ```bash
   python main.py
   ```

3. Access the API:
   - Health check: http://localhost:8000/health
   - API docs: http://localhost:8000/docs

### Docker

Build and run with Docker:

```bash
docker build -t {service_name} .
docker run -p 8000:8000 {service_name}
```

### Kubernetes

Deploy to Kubernetes using Helm:

```bash
cd helm
helm install {service_name} .
```

## API Endpoints

- `GET /health` - Health check
- `GET /` - Root endpoint
- `GET /api/v1/` - API root
- `GET /api/v1/example` - Example endpoint

## Configuration

Environment variables:
- `ENVIRONMENT` - Deployment environment (default: production)
- `LOG_LEVEL` - Logging level (default: INFO)

## Development

### Project Structure

```
{service_name}/
├── main.py              # FastAPI application entry point
├── routers/             # API route definitions
├── models/              # Data models
├── services/            # Business logic
├── utils/               # Utility functions
├── tests/               # Test files
├── helm/                # Helm chart for Kubernetes deployment
└── .github/workflows/   # CI/CD workflows
```

### Adding New Endpoints

1. Create new routes in `routers/main_router.py`
2. Add business logic in `services/`
3. Define data models in `models/`
4. Add tests in `tests/`

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting

## License

Generated by AuditMigrate - Part of the LinkOps MLOps Platform
"""

    def _load_templates(self) -> Dict[str, Any]:
        """Load template configurations"""
        return {
            "microservice": {
                "description": "Standard microservice template",
                "features": ["health_check", "api_routes", "database", "logging"],
            },
            "gateway": {
                "description": "API Gateway template",
                "features": ["routing", "rate_limiting", "authentication", "cors"],
            },
            "observability": {
                "description": "Monitoring and observability service",
                "features": ["metrics", "logging", "tracing", "alerting"],
            },
        }
