from fastapi import FastAPI
from routes import chat, actions, explain, describe_image, voice

app = FastAPI(
    title="James – LinkOps Executive Assistant",
    description="Your personal J.A.R.V.I.S. for LinkOps with voice and vision capabilities",
    version="2.0.0",
)

# Include all route modules
app.include_router(chat.router)
app.include_router(actions.router)
app.include_router(explain.router)
app.include_router(describe_image.router)
app.include_router(voice.router)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "james",
        "role": "LinkOps Executive Assistant",
        "capabilities": [
            "Voice Input/Output",
            "Image Analysis & Description",
            "System Status Monitoring",
            "Agent Communication",
            "Natural Language Processing",
            "Screenshot Analysis",
            "Conversation Management",
        ],
        "voice_characteristics": {
            "tone": "calm_powerful",
            "inspiration": "Giancarlo Esposito",
            "style": "elegant_authority",
        },
    }
