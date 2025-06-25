# LinkOps Data Flow Diagram

## Complete Service Communication Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Input    │    │  Data Collector │    │   Sanitizer     │
│   (Frontend/    │───▶│   (Port 8001)   │───▶│   (Port 8002)   │
│    External)    │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │     Kafka       │    │      Whis       │
                       │   (Legacy)      │    │   (Port 8003)   │
                       │                 │    │                 │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │  Training Data  │
                                              │    Storage      │
                                              │                 │
                                              └─────────────────┘
```

## Service Communication Details

### 1. Data Collector → Sanitizer
- **Endpoint**: `POST /api/collect`
- **Environment Variable**: `SANITIZER_URL=http://sanitizer:8002/api/sanitize`
- **Payload**: 
  ```json
  {
    "input_type": "task|qna|info|image|fixlog",
    "payload": { ... }
  }
  ```

### 2. Sanitizer → Whis
- **Endpoint**: `POST /api/sanitize`
- **Environment Variable**: `WHIS_URL=http://whis:8003/api/whis/train`
- **Payload**: 
  ```json
  {
    "input_type": "task|qna|info|image|fixlog",
    "payload": { ... }
  }
  ```

### 3. Whis Training
- **Endpoint**: `POST /api/whis/train`
- **Response**: 
  ```json
  {
    "status": "received",
    "type": "task",
    "category": "katie|audit|igris|whis|links",
    "message": "Training data processed successfully"
  }
  ```

## Legacy Support

### Kafka Integration (Backward Compatibility)
- **Task Collection**: `POST /api/collect/task` → Kafka topic `raw-tasks`
- **QnA Collection**: `POST /api/collect/qna` → Kafka topic `raw-qna`
- **Info Collection**: `POST /api/collect/info` → Kafka topic `raw-info`

## Error Handling

### Data Collector
- Returns `sent_to_sanitizer: false` if sanitizer is unavailable
- Includes error details in response

### Sanitizer
- Returns `forwarded_to_whis: false` if whis is unavailable
- Includes error details in response
- Still saves sanitized data locally

### Whis
- Returns error status if processing fails
- Logs detailed error information

## Testing

### Run Complete Flow Test
```bash
python test_data_collector_sanitizer_whis_flow.py
```

### Run Individual Service Tests
```bash
python test_sanitizer_whis_communication.py
```

## Environment Variables

### Required for Service Communication
```bash
# Data Collector → Sanitizer
SANITIZER_URL=http://sanitizer:8002/api/sanitize

# Sanitizer → Whis
WHIS_URL=http://whis:8003/api/whis/train
```

### Docker Compose Configuration
```yaml
data-collector:
  environment:
    - SANITIZER_URL=http://sanitizer:8002/api/sanitize

sanitizer:
  environment:
    - WHIS_URL=http://whis:8003/api/whis/train
```

## Benefits

1. **Direct Communication**: Services communicate directly via HTTP
2. **Real-time Processing**: No delays from message queue processing
3. **Error Handling**: Immediate feedback on communication failures
4. **Backward Compatibility**: Legacy Kafka endpoints still work
5. **Flexible Routing**: Easy to modify communication paths
6. **Monitoring**: Clear visibility into data flow and failures 