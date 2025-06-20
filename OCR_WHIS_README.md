# 📷 OCR & Whis AI Integration

This document explains how to use the OCR (Optical Character Recognition) and Whis AI integration features in LinkOps Core.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Tesseract OCR (Ubuntu/Debian)
sudo apt update
sudo apt install tesseract-ocr -y

# Verify installation
python test_ocr_setup.py
```

### 2. Start the LinkOps API

```bash
# Start the FastAPI server
uvicorn core.api.main:app --reload
```

### 3. Test OCR Functionality

```bash
# Test with a screenshot
python screenshot_to_log.py screenshots/your_image.png task_id
```

## 📁 File Structure

```
./
├── screenshot_to_log.py      # OCR script to extract text from images
├── whis_consumer.py          # Kafka consumer for automatic Orb creation
├── manual_orb_creator.py     # Manual Orb creation without Kafka
├── test_ocr_setup.py         # Test script for OCR setup
└── screenshots/              # Directory for storing screenshots
```

## 🔧 Usage

### Screenshot OCR (`screenshot_to_log.py`)

Extract text from images and send to LinkOps logs:

```bash
# Basic usage
python screenshot_to_log.py path/to/image.png

# With custom task ID
python screenshot_to_log.py path/to/image.png cka_q17

# Example
python screenshot_to_log.py screenshots/cka_q17_gatewayapi.png cka_q17
```

**Output:**
- Extracts text from the image using Tesseract OCR
- Sends the extracted text to `/api/logs` endpoint
- Returns status code and response message

### Manual Orb Creator (`manual_orb_creator.py`)

Create Orbs from logs without Kafka:

```bash
python manual_orb_creator.py
```

**Features:**
- Interactive menu to process screenshot logs
- Create test Orbs manually
- View recent logs
- Automatic Orb creation from Katie agent logs

### Whis Consumer (`whis_consumer.py`)

Automatic Orb creation from Kafka logs (requires Kafka setup):

```bash
python whis_consumer.py
```

**Features:**
- Listens to Kafka "logs" topic
- Automatically creates Orbs from screenshot logs
- Filters for Katie agent logs with screenshot actions

## 🧪 Testing

### Test OCR Setup

```bash
python test_ocr_setup.py
```

This script checks:
- ✅ Python dependencies (requests, PIL, pytesseract, kafka)
- ✅ Tesseract OCR availability
- ✅ LinkOps API connectivity

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Create a log
curl -X POST http://localhost:8000/api/logs \
  -H "Content-Type: application/json" \
  -d '{"agent": "katie", "task_id": "test", "action": "test", "result": "test"}'

# Create an Orb
curl -X POST http://localhost:8000/api/orbs \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Orb", "description": "Test description", "category": "Test"}'

# Get all Orbs
curl http://localhost:8000/api/orbs
```

## 🔄 Workflow

### Complete OCR → Orb Workflow

1. **Take Screenshot** → Save to `screenshots/` directory
2. **Extract Text** → Run `screenshot_to_log.py`
3. **Create Orb** → Use `manual_orb_creator.py` or `whis_consumer.py`
4. **Add Runes** → Attach automation scripts to the Orb

### Example Workflow

```bash
# 1. Extract text from CKA screenshot
python screenshot_to_log.py screenshots/cka_q17_gatewayapi.png cka_q17

# 2. Create Orb from the log
python manual_orb_creator.py
# Choose option 1 to process screenshot logs

# 3. Verify Orb creation
curl http://localhost:8000/api/orbs
```

## 🐛 Troubleshooting

### Common Issues

**1. Tesseract not found**
```bash
# Install Tesseract
sudo apt install tesseract-ocr -y

# Verify installation
tesseract --version
```

**2. API not accessible**
```bash
# Start the API server
uvicorn core.api.main:app --reload

# Check if it's running
curl http://localhost:8000/health
```

**3. Database connection issues**
```bash
# Check database configuration
# Ensure PostgreSQL is running
# Verify DATABASE_URL in .env file
```

**4. Image processing errors**
```bash
# Check image format (PNG, JPG, etc.)
# Ensure image is readable
# Try with a different image
```

### Debug Mode

Enable debug logging:

```bash
# Set environment variable
export DEBUG=true

# Run with verbose output
python screenshot_to_log.py image.png 2>&1 | tee debug.log
```

## 🔮 Future Enhancements

### Planned Features

- **Multi-language OCR** support
- **Image preprocessing** for better text extraction
- **Batch processing** of multiple images
- **Web interface** for screenshot upload
- **Real-time OCR** with webcam support
- **Advanced text analysis** with NLP
- **Automatic categorization** of extracted content

### Integration Ideas

- **Slack integration** for screenshot sharing
- **Email attachment** processing
- **Cloud storage** integration (S3, GCS)
- **Mobile app** for screenshot capture
- **Browser extension** for web page capture

## 📚 API Reference

### Logs API

- `POST /api/logs` - Create a new log entry
- `GET /api/logs` - Get all logs

### Orbs API

- `POST /api/orbs` - Create a new Orb
- `GET /api/orbs` - Get all Orbs

### Health API

- `GET /health` - Health check endpoint

## 🤝 Contributing

1. Add new OCR features
2. Improve text extraction accuracy
3. Add support for new image formats
4. Enhance Whis AI logic
5. Create additional automation scripts

## 📄 License

This project is licensed under the MIT License. 