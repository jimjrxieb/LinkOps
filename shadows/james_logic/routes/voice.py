"""
James - Voice Interface Route
Handles voice input/output with James' signature calm, powerful tone
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from typing import Dict, Any, Optional
import logging
import io
import tempfile
import os
from pydantic import BaseModel
import speech_recognition as sr
from gtts import gTTS
import pygame
import json

router = APIRouter(prefix="/api", tags=["voice"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# James' voice configuration
JAMES_VOICE_CONFIG = {
    "language": "en",
    "tld": "com",
    "slow": False,
    "lang": "en",
    "tld": "com",
}

# Initialize speech recognition
recognizer = sr.Recognizer()


class VoiceRequest(BaseModel):
    text: str
    tone: str = "calm_powerful"  # calm_powerful, professional, authoritative


class VoiceResponse(BaseModel):
    text: str
    audio_url: str
    duration_seconds: float
    tone: str


@router.post("/voice/speak")
async def james_speak(request: VoiceRequest) -> Dict[str, Any]:
    """
    James speaks the provided text with his signature calm, powerful voice.
    Returns audio file and metadata.
    """
    try:
        logger.info(f"James speaking: {request.text[:50]}...")

        # Process text with James' tone
        processed_text = _apply_james_tone(request.text, request.tone)

        # Generate speech
        tts = gTTS(text=processed_text, **JAMES_VOICE_CONFIG)

        # Create temporary audio file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            tts.save(temp_file.name)
            audio_path = temp_file.name

        # Get audio duration (approximate)
        duration = _estimate_audio_duration(processed_text)

        response = {
            "agent": "james",
            "original_text": request.text,
            "processed_text": processed_text,
            "audio_file": audio_path,
            "duration_seconds": duration,
            "tone": request.tone,
            "voice_characteristics": {
                "style": "calm_powerful",
                "pace": "measured",
                "authority": "high",
                "clarity": "crystal_clear",
            },
        }

        logger.info(f"James completed speech generation: {duration}s")
        return response

    except Exception as e:
        logger.error(f"James speech generation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Speech generation failed: {str(e)}"
        )


@router.post("/voice/listen")
async def james_listen(audio: UploadFile = File(...)) -> Dict[str, Any]:
    """
    James listens to voice input and transcribes it with high accuracy.
    Accepts various audio formats.
    """
    try:
        logger.info(f"James listening to: {audio.filename}")

        # Validate audio file
        if not audio.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400, detail="File must be an audio file (WAV, MP3, etc.)"
            )

        # Read audio data
        audio_data = await audio.read()

        # Convert to audio file for speech recognition
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name

        # Perform speech recognition
        with sr.AudioFile(temp_file_path) as source:
            audio = recognizer.record(source)

            try:
                # Use Google Speech Recognition
                transcribed_text = recognizer.recognize_google(audio)
                confidence = "high"
            except sr.UnknownValueError:
                transcribed_text = ""
                confidence = "low"
            except sr.RequestError as e:
                logger.error(f"Speech recognition service error: {e}")
                raise HTTPException(
                    status_code=500, detail="Speech recognition service unavailable"
                )

        # Clean up temporary file
        os.unlink(temp_file_path)

        # Process with James' understanding
        processed_text = _process_james_understanding(transcribed_text)

        response = {
            "agent": "james",
            "original_audio": audio.filename,
            "transcribed_text": transcribed_text,
            "processed_text": processed_text,
            "confidence": confidence,
            "understanding": {
                "intent": _extract_intent(transcribed_text),
                "urgency": _assess_urgency(transcribed_text),
                "complexity": _assess_complexity(transcribed_text),
            },
        }

        logger.info(f"James completed listening: {confidence} confidence")
        return response

    except Exception as e:
        logger.error(f"James listening failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Voice recognition failed: {str(e)}"
        )


@router.get("/voice/audio/{filename}")
async def get_audio_file(filename: str):
    """
    Retrieve generated audio files.
    """
    try:
        # Security: validate filename
        if not filename.endswith(".mp3") or ".." in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")

        file_path = f"/tmp/{filename}"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Audio file not found")

        return FileResponse(file_path, media_type="audio/mpeg", filename=filename)

    except Exception as e:
        logger.error(f"Audio file retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Audio retrieval failed: {str(e)}")


@router.post("/voice/conversation")
async def james_conversation(audio: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Full conversation mode: James listens, processes, and responds with voice.
    """
    try:
        logger.info("James entering conversation mode")

        # Step 1: Listen and transcribe
        listen_response = await james_listen(audio)
        user_input = listen_response["transcribed_text"]

        if not user_input:
            return {
                "agent": "james",
                "status": "no_speech_detected",
                "response": "I didn't catch that. Could you please repeat?",
            }

        # Step 2: Process with James' intelligence
        james_response = _generate_james_response(user_input)

        # Step 3: Generate speech response
        speak_request = VoiceRequest(text=james_response, tone="calm_powerful")
        speak_response = await james_speak(speak_request)

        return {
            "agent": "james",
            "conversation": {
                "user_input": user_input,
                "james_response": james_response,
                "audio_response": speak_response["audio_file"],
            },
            "processing": {
                "intent": listen_response["understanding"]["intent"],
                "confidence": listen_response["confidence"],
                "response_tone": "calm_powerful",
            },
        }

    except Exception as e:
        logger.error(f"James conversation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Conversation processing failed: {str(e)}"
        )


def _apply_james_tone(text: str, tone: str) -> str:
    """Apply James' signature tone to text."""

    if tone == "calm_powerful":
        # Add James' characteristic calm authority
        if not text.endswith((".", "!", "?")):
            text += "."

        # Enhance with James' style
        enhancements = [
            "Indeed.",
            "I understand.",
            "Let me clarify.",
            "As you know,",
            "I should mention,",
        ]

        # Add enhancement if appropriate
        if len(text) > 50 and not any(
            enhancement in text for enhancement in enhancements
        ):
            text = f"I understand. {text}"

    return text


def _estimate_audio_duration(text: str) -> float:
    """Estimate audio duration based on text length."""
    # Average speaking rate: 150 words per minute
    words = len(text.split())
    return (words / 150) * 60


def _process_james_understanding(text: str) -> str:
    """Process transcribed text with James' understanding."""
    # Clean up transcription
    text = text.strip()

    # Add context if needed
    if text.lower().startswith(("james", "hey james", "excuse me")):
        text = text  # Already addressed to James
    else:
        text = f"User request: {text}"

    return text


def _extract_intent(text: str) -> str:
    """Extract user intent from transcribed text."""
    text_lower = text.lower()

    if any(word in text_lower for word in ["status", "how", "what"]):
        return "query"
    elif any(word in text_lower for word in ["do", "run", "execute", "start"]):
        return "command"
    elif any(word in text_lower for word in ["explain", "describe", "show"]):
        return "explanation"
    else:
        return "general"


def _assess_urgency(text: str) -> str:
    """Assess urgency level of user input."""
    text_lower = text.lower()

    urgent_words = ["urgent", "emergency", "now", "immediately", "critical"]
    if any(word in text_lower for word in urgent_words):
        return "high"
    elif any(word in text_lower for word in ["soon", "quickly", "fast"]):
        return "medium"
    else:
        return "low"


def _assess_complexity(text: str) -> str:
    """Assess complexity of user request."""
    words = len(text.split())

    if words > 20:
        return "high"
    elif words > 10:
        return "medium"
    else:
        return "low"


def _generate_james_response(user_input: str) -> str:
    """Generate James' response to user input."""

    # Simple response generation - would be enhanced with LLM
    if "status" in user_input.lower():
        return "I'm monitoring all LinkOps systems. Everything appears to be operating within normal parameters."
    elif "help" in user_input.lower():
        return "I'm here to assist you with LinkOps operations. What would you like to know?"
    elif "agents" in user_input.lower():
        return "I have access to all LinkOps agents: Whis, Igris, Katie, and AuditGuard. Which would you like to query?"
    else:
        return "I understand your request. Let me process that for you."
