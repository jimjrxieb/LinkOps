from fastapi import FastAPI
from routes import collect, qna, info_dump, image_input, fixlog, youtube

app = FastAPI(title="Data Collector Service")

app.include_router(collect.router)
app.include_router(qna.router)
app.include_router(info_dump.router)
app.include_router(image_input.router)
app.include_router(fixlog.router)
app.include_router(youtube.router)


@app.get("/health")
def health():
    """Basic health check"""
    return {"status": "healthy", "service": "whis_data_input"}
