# LinkOps Core

A FastAPI microservice following MLOps best practices for managing links and screenshots with PostgreSQL and Kafka integration.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **PostgreSQL Database**: Robust relational database with connection pooling
- **Kafka Integration**: Message broker for event-driven architecture
- **Health Checks**: Comprehensive monitoring endpoints
- **File Storage**: Screenshot and log management
- **Environment Configuration**: Flexible configuration management
- **Docker Support**: Containerized deployment
- **Testing**: Comprehensive test suite

## 📁 Project Structure

```
./
├── core/
│   ├── api/
│   │   ├── app.py              # FastAPI application factory
│   │   └── dependencies.py     # API dependencies
│   ├── db/
│   │   ├── connection.py       # Database connection management
│   │   └── models.py           # Database models
│   ├── models/
│   │   ├── schemas.py          # Pydantic schemas
│   │   └── entities.py         # SQLAlchemy entities
│   └── routes/
│       ├── health.py           # Health check endpoints
│       └── api.py              # Main API routes
├── config/
│   ├── settings.py             # Application settings
│   ├── database.py             # Database configuration
│   └── kafka.py                # Kafka configuration
├── screenshots/                # Screenshot storage
├── logs/                       # Application logs
├── tests/                      # Test suite
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
└── README.md                  # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Kafka 2.8+
- Docker (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ./
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   # Create PostgreSQL database
   createdb linkops
   
   # Run database migrations (if using Alembic)
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   python main.py
   ```

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually**
   ```bash
   docker build -t linkops-core .
   docker run -p 8000:8000 linkops-core
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `LinkOps Core` |
| `DEBUG` | Debug mode | `false` |
| `HOST` | Host to bind to | `0.0.0.0` |
| `PORT` | Port to bind to | `8000` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/linkops` |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka servers | `localhost:9092` |
| `SCREENSHOTS_DIR` | Screenshot storage directory | `./screenshots` |
| `LOGS_DIR` | Log storage directory | `./logs` |

## 📚 API Documentation

### Health Checks

- `GET /health/` - Basic health check
- `GET /health/detailed` - Detailed health with metrics
- `GET /health/ready` - Kubernetes readiness probe
- `GET /health/live` - Kubernetes liveness probe

### Links API

- `GET /api/v1/links` - Get all links (paginated)
- `GET /api/v1/links/{link_id}` - Get specific link
- `POST /api/v1/links` - Create new link
- `PUT /api/v1/links/{link_id}` - Update link
- `DELETE /api/v1/links/{link_id}` - Delete link
- `POST /api/v1/links/{link_id}/screenshot` - Upload screenshot

### Interactive Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core

# Run specific test file
pytest tests/test_api.py
```

### Test Structure
- `tests/test_api.py` - API endpoint tests
- `tests/test_models.py` - Model validation tests
- `tests/conftest.py` - Test configuration and fixtures

## 📊 Monitoring

### Health Checks
The application provides comprehensive health checks:
- Database connectivity
- Kafka connectivity
- System metrics (CPU, memory, disk)
- Directory accessibility

### Logging
- Structured logging with JSON format
- Configurable log levels
- Log rotation and archiving

### Metrics
- System resource usage
- Database connection pool status
- API request metrics

## 🔄 Kafka Events

The application publishes events to Kafka topics:

- `linkops.links.created` - When a new link is created
- `linkops.links.updated` - When a link is updated
- `linkops.links.deleted` - When a link is deleted

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use proper secrets management
2. **Database**: Use connection pooling and read replicas
3. **Kafka**: Configure proper retention and partitioning
4. **Monitoring**: Set up proper logging and metrics collection
5. **Security**: Enable HTTPS, CORS, and authentication
6. **Scaling**: Use load balancers and horizontal scaling

### Kubernetes

Example deployment configuration:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: linkops-core
spec:
  replicas: 3
  selector:
    matchLabels:
      app: linkops-core
  template:
    metadata:
      labels:
        app: linkops-core
    spec:
      containers:
      - name: linkops-core
        image: linkops-core:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: linkops-secrets
              key: database-url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run linting and tests
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API docs at `/docs`
