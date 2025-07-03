from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class PipelineRequest(BaseModel):
    dataset_path: str
    pipeline_name: str
    model_type: str


@app.post("/run_pipeline/")
async def run_pipeline(req: PipelineRequest):
    # TODO: Call Kubeflow client logic here (e.g., submit job via kfp.Client)
    print(
        f"[KUBEFLOW] Submitting pipeline: {req.pipeline_name} with data at {req.dataset_path}"
    )
    return {
        "status": "submitted",
        "pipeline": req.pipeline_name,
        "model_type": req.model_type,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
