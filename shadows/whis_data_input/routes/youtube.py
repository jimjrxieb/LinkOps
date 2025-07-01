from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..utils.youtube_transcript import download_transcript
import requests

router = APIRouter()


class YouTubeTranscriptRequest(BaseModel):
    url: str
    topic: str


@router.post("/input/youtube-transcript")
def handle_youtube_transcript(request: YouTubeTranscriptRequest):
    """Handle YouTube transcript download and forward to sanitizer."""
    try:
        transcript = download_transcript(request.url)
        if not transcript:
            raise HTTPException(status_code=404, detail="Transcript not available")

        payload = {
            "raw_text": transcript,
            "source": "youtube",
            "topic": request.topic,
            "metadata": {"url": request.url, "type": "video_transcript"},
        }

        # Forward to sanitizer service
        try:
            response = requests.post("http://whis-sanitize:8000/sanitize", json=payload)
            response.raise_for_status()
            return {"status": "queued", "sanitizer_response": response.json()}
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, detail=f"Sanitizer service error: {str(e)}"
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing transcript: {str(e)}"
        )
