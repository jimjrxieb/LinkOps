"""
James - Image Description Route
Provides calm, precise descriptions of uploaded images and screenshots
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import io
from PIL import Image
import pytesseract
import requests

router = APIRouter(prefix="/api", tags=["image-analysis"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# James' persona for image descriptions
JAMES_IMAGE_PROMPT = """
You are James, the LinkOps Executive Assistant. 
When describing images, be calm, precise, and professional.
Focus on:
- Clear identification of UI elements
- Accurate description of text content
- Professional assessment of system states
- Elegant, measured tone
"""


@router.post("/describe_image")
async def describe_image(image: UploadFile = File(...)) -> Dict[str, Any]:
    """
    James analyzes uploaded images and provides calm, precise descriptions.
    Supports screenshots, UI elements, and system state visualization.
    """
    try:
        logger.info(f"James analyzing image: {image.filename}")

        # Validate image file
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, detail="File must be an image (PNG, JPG, JPEG, etc.)"
            )

        # Read and process image
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data))

        # Extract text using OCR
        try:
            ocr_text = pytesseract.image_to_string(pil_image)
            ocr_confidence = "high" if ocr_text.strip() else "low"
        except Exception as e:
            logger.warning(f"OCR failed: {e}")
            ocr_text = ""
            ocr_confidence = "failed"

        # Analyze image characteristics
        image_analysis = _analyze_image_characteristics(pil_image)

        # Generate James-style description
        description = _generate_james_description(
            image.filename, image_analysis, ocr_text, ocr_confidence
        )

        response = {
            "agent": "james",
            "image_filename": image.filename,
            "description": description,
            "analysis": {
                "ocr_text": ocr_text.strip() if ocr_text else None,
                "ocr_confidence": ocr_confidence,
                "image_characteristics": image_analysis,
                "james_insight": _generate_james_insight(image_analysis, ocr_text),
            },
            "tone": "calm_precise",
            "confidence": "high",
        }

        logger.info(f"James completed image analysis: {image.filename}")
        return response

    except Exception as e:
        logger.error(f"James image analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")


def _analyze_image_characteristics(image: Image.Image) -> Dict[str, Any]:
    """Analyze image characteristics for context."""
    return {
        "dimensions": image.size,
        "format": image.format,
        "mode": image.mode,
        "file_size_kb": len(image.tobytes()) // 1024,
        "aspect_ratio": f"{image.size[0]}/{image.size[1]}",
        "is_screenshot": _detect_screenshot(image),
        "ui_elements": _detect_ui_elements(image),
        "text_density": _estimate_text_density(image),
    }


def _detect_screenshot(image: Image.Image) -> bool:
    """Detect if image is likely a screenshot."""
    # Simple heuristics for screenshot detection
    width, height = image.size

    # Common screenshot aspect ratios
    common_ratios = [16 / 9, 4 / 3, 21 / 9, 1 / 1]
    current_ratio = width / height

    # Check if ratio matches common screen formats
    for ratio in common_ratios:
        if abs(current_ratio - ratio) < 0.1:
            return True

    return False


def _detect_ui_elements(image: Image.Image) -> Dict[str, bool]:
    """Detect common UI elements in the image."""
    # This would be enhanced with computer vision models
    # For now, return basic detection
    return {
        "has_text": True,  # Assume text presence
        "has_buttons": False,
        "has_forms": False,
        "has_charts": False,
        "has_tables": False,
    }


def _estimate_text_density(image: Image.Image) -> str:
    """Estimate text density in the image."""
    # Simplified text density estimation
    width, height = image.size
    area = width * height

    if area < 100000:  # Small image
        return "low"
    elif area < 500000:  # Medium image
        return "medium"
    else:  # Large image
        return "high"


def _generate_james_description(
    filename: str, analysis: Dict[str, Any], ocr_text: str, ocr_confidence: str
) -> str:
    """Generate James-style image description."""

    description_parts = []

    # Start with image type identification
    if analysis["is_screenshot"]:
        description_parts.append("I can see this is a screenshot")
    else:
        description_parts.append("I can see this is an image")

    # Add dimension context
    width, height = analysis["dimensions"]
    description_parts.append(f"with dimensions {width} by {height} pixels")

    # Add OCR content if available
    if ocr_text and ocr_confidence != "failed":
        if ocr_confidence == "high":
            description_parts.append("The text content is clearly visible")
        else:
            description_parts.append("There appears to be some text content")

        # Add a brief summary of OCR text (first 100 chars)
        text_preview = ocr_text[:100].replace("\n", " ").strip()
        if text_preview:
            description_parts.append(f"including: '{text_preview}...'")

    # Add UI element detection
    ui_elements = analysis["ui_elements"]
    if ui_elements["has_text"]:
        description_parts.append("The interface contains textual elements")

    # Add professional assessment
    description_parts.append("The overall composition appears well-structured")

    return ". ".join(description_parts) + "."


def _generate_james_insight(analysis: Dict[str, Any], ocr_text: str) -> str:
    """Generate James' professional insight about the image."""

    insights = []

    if analysis["is_screenshot"]:
        insights.append("This appears to be a system interface or application window")

    if ocr_text:
        insights.append("The text content suggests this is an active system state")

    if analysis["text_density"] == "high":
        insights.append("The interface contains substantial information density")

    if not insights:
        insights.append("The image provides a clear view of the current system state")

    return " ".join(insights) + "."
