#!/usr/bin/env python3
"""
Test script to verify OCR setup and dependencies
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ PIL/Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PIL: {e}")
        return False
    
    try:
        import pytesseract
        print("✅ pytesseract imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pytesseract: {e}")
        return False
    
    try:
        from kafka import KafkaConsumer
        print("✅ kafka-python imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import kafka: {e}")
        return False
    
    return True

def test_tesseract():
    """Test if Tesseract is available"""
    print("\nTesting Tesseract availability...")
    
    try:
        import pytesseract
        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract version: {version}")
        return True
    except Exception as e:
        print(f"❌ Tesseract not available: {e}")
        print("💡 Install Tesseract with: sudo apt install tesseract-ocr")
        return False

def test_api_connection():
    """Test if the LinkOps API is accessible"""
    print("\nTesting API connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ LinkOps API is accessible")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to LinkOps API (localhost:8000)")
        print("💡 Start the API with: uvicorn core.api.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 LinkOps OCR Setup Test")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_tesseract():
        tests_passed += 1
    
    if test_api_connection():
        tests_passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! OCR setup is ready.")
        print("\nNext steps:")
        print("1. Add screenshots to the screenshots/ directory")
        print("2. Run: python screenshot_to_log.py screenshots/your_image.png task_id")
        print("3. Check logs at: http://localhost:8000/api/logs")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 