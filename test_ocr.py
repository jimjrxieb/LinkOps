#!/usr/bin/env python3
"""
Test script for OCR functionality
"""

from PIL import Image, ImageDraw, ImageFont
import pytesseract

def create_test_image():
    """Create a simple test image with Kubernetes YAML text"""
    # Create a white image
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add text (simulate Kubernetes YAML)
    text = """apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80"""
    
    # Draw text
    try:
        # Try to use a system font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    draw.text((20, 20), text, fill='black', font=font)
    
    # Save the image
    img.save('test_k8s_image.png')
    print("Created test image: test_k8s_image.png")
    
    return 'test_k8s_image.png'

def test_ocr():
    """Test OCR on the created image"""
    try:
        image_path = create_test_image()
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        print("OCR Result:")
        print(text)
        return text
    except Exception as e:
        print(f"OCR test failed: {e}")
        return None

if __name__ == "__main__":
    test_ocr() 