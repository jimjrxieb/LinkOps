"""
Seed script to populate the database with preloaded Whis MLOps templates
"""

from core.db.models import Orb, Rune
from core.db.database import get_db


def seed_whis_templates():
    """Seed the database with preloaded Whis MLOps templates"""

    preloaded_templates = [{"task_id": "mlflow/train/pipeline",
                            "task": "Train and log a scikit-learn pipeline using MLflow",
                            "orb_description": ("Use `mlflow.sklearn.autolog()` to track all model metrics and "
                                                "parameters automatically."),
                            "rune_content": """import mlflow
import mlflow.sklearn
from sklearn.pipeline import Pipeline

mlflow.sklearn.autolog()
pipeline = Pipeline({{steps}})
pipeline.fit({{X_train}}, {{y_train}})""",
                            "category": "mlops",
                            },
                           {"task_id": "model/serve/fastapi",
                            "task": "Serve a model with FastAPI using joblib",
                            "orb_description": ("Use `joblib.load()` to restore the model and create a `/predict` "
                                                "route with FastAPI."),
                            "rune_content": """from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("{{model_path}}")

@app.post("/predict")
def predict(data: dict):
    return {"prediction": model.predict([[data['value']]])[0]}""",
                            "category": "mlops",
                            },
                           {"task_id": "docker/build/deploy",
                            "task": "Build and deploy a Docker container for ML model serving",
                            "orb_description": ("Use multi-stage Docker builds to optimize image size and include "
                                                "only necessary dependencies."),
                            "rune_content": """# Dockerfile
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY {{model_path}} ./model/
COPY app.py .

EXPOSE {{port}}
CMD ["python", "app.py"]""",
                            "category": "mlops",
                            },
                           {"task_id": "k8s/deploy/model",
                            "task": "Deploy ML model to Kubernetes with horizontal pod autoscaling",
                            "orb_description": ("Use Kubernetes deployments with resource limits and HPA for "
                                                "automatic scaling based on CPU/memory usage."),
                            "rune_content": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{model_name}}-deployment
spec:
  replicas: {{replicas}}
  selector:
    matchLabels:
      app: {{model_name}}
  template:
    metadata:
      labels:
        app: {{model_name}}
    spec:
      containers:
      - name: {{model_name}}
        image: {{image}}:{{tag}}
        ports:
        - containerPort: {{port}}
        resources:
          requests:
            memory: "{{memory_request}}"
            cpu: "{{cpu_request}}"
          limits:
            memory: "{{memory_limit}}"
            cpu: "{{cpu_limit}}"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{model_name}}-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{model_name}}-deployment
  minReplicas: {{min_replicas}}
  maxReplicas: {{max_replicas}}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {{cpu_target}}""",
                            "category": "mlops",
                            },
                           {"task_id": "monitoring/prometheus/metrics",
                            "task": "Add Prometheus metrics to ML model serving application",
                            "orb_description": ("Use prometheus_client to expose metrics for model predictions, "
                                                "latency, and error rates."),
                            "rune_content": """from prometheus_client import Counter, Histogram, generate_latest
from fastapi import FastAPI, Response
import time

app = FastAPI()

# Metrics
PREDICTION_COUNTER = Counter('model_predictions_total', 'Total predictions made')
PREDICTION_LATENCY = Histogram('model_prediction_duration_seconds', 'Prediction latency')
ERROR_COUNTER = Counter('model_errors_total', 'Total prediction errors')

@app.post("/predict")
def predict(data: dict):
    start_time = time.time()
    try:
        # Your prediction logic here
        result = model.predict([[data['value']]])
        PREDICTION_COUNTER.inc()
        PREDICTION_LATENCY.observe(time.time() - start_time)
        return {"prediction": result[0]}
    except Exception as e:
        ERROR_COUNTER.inc()
        raise e

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")""",
                            "category": "mlops",
                            },
                           ]

    # Get database session
    db = next(get_db())

    try:
        for template in preloaded_templates:
            # Check if Orb already exists
            existing_orb = (
                db.query(Orb)
                .filter(Orb.name == f"Whis Task: {template['task_id']}")
                .first()
            )

            if existing_orb:
                print(
                    f"Orb already exists for {template['task_id']}, skipping...")
                continue

            # Create Orb
            orb = Orb(
                name=f"Whis Task: {template['task_id']}",
                description=template["orb_description"],
                category=template["category"],
            )
            db.add(orb)
            db.commit()
            db.refresh(orb)

            # Create Rune
            rune = Rune(
                orb_id=orb.id,
                script_path=(
                    f"/memory/whis/{template['task_id'].replace('/', '_')}.rune"
                ),
                script_content=template["rune_content"],
                language="python",
                version=1,
            )
            db.add(rune)
            db.commit()

            print(f"✅ Created Whis template: {template['task_id']}")

    except Exception as e:
        print(f"❌ Error seeding Whis templates: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding Whis MLOps templates...")
    seed_whis_templates()
    print("✅ Whis seeding complete!")
