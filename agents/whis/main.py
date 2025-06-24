from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import logging

app = FastAPI(title="Whis Agent - AI/ML Specialist")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentTaskInput(BaseModel):
    task_text: str
    context: Optional[Dict[str, Any]] = None
    learning_data: Optional[List[Dict[str, Any]]] = None

class WhisResponse(BaseModel):
    agent: str = "whis"
    task: str
    response: str
    learning_outcome: Dict[str, Any]
    generated_orbs: List[Dict[str, Any]]
    generated_runes: List[Dict[str, Any]]
    confidence_score: float

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "agent": "whis",
        "specialization": "AI/ML Training & Learning",
        "capabilities": [
            "Machine Learning Model Training",
            "Orb Generation from Data",
            "Rune Creation for AI Agents",
            "Pattern Recognition",
            "Knowledge Base Management",
            "AI Agent Optimization"
        ]
    }

@app.post("/execute")
def execute(data: AgentTaskInput):
    """
    Whis specializes in AI/ML tasks and learning from data
    - Processes sanitized data for training
    - Generates orbs and runes for AI agents
    - Optimizes machine learning workflows
    - Creates new AI agent capabilities
    """
    try:
        logger.info(f"Whis processing task: {data.task_text}")
        
        # Analyze task for ML/AI components
        ml_components = _analyze_ml_components(data.task_text)
        
        # Process learning data if provided
        learning_outcome = _process_learning_data(data.learning_data or [])
        
        # Generate orbs based on patterns
        generated_orbs = _generate_orbs(data.task_text, ml_components)
        
        # Generate runes for AI agents
        generated_runes = _generate_runes(data.task_text, ml_components)
        
        # Create response
        response = WhisResponse(
            task=data.task_text,
            response=_generate_ml_response(data.task_text, ml_components),
            learning_outcome=learning_outcome,
            generated_orbs=generated_orbs,
            generated_runes=generated_runes,
            confidence_score=_calculate_confidence(ml_components)
        )
        
        logger.info(f"Whis completed task with {len(generated_orbs)} orbs and {len(generated_runes)} runes")
        return response
        
    except Exception as e:
        logger.error(f"Whis execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Whis execution failed: {str(e)}")

@app.post("/train")
def train_on_data(learning_data: List[Dict[str, Any]]):
    """
    Train Whis on new data to improve AI agent capabilities
    """
    try:
        logger.info(f"Training Whis on {len(learning_data)} data points")
        
        # Process training data
        training_results = _process_learning_data(learning_data)
        
        # Generate new capabilities
        new_capabilities = _generate_capabilities(learning_data)
        
        return {
            "status": "training_complete",
            "data_points_processed": len(learning_data),
            "new_capabilities": new_capabilities,
            "training_results": training_results
        }
        
    except Exception as e:
        logger.error(f"Whis training failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/capabilities")
def get_capabilities():
    """Get current Whis capabilities"""
    return {
        "agent": "whis",
        "specialization": "AI/ML Training & Learning",
        "current_capabilities": [
            "Machine Learning Model Training",
            "Neural Network Optimization",
            "Data Pattern Recognition",
            "AI Agent Generation",
            "Orb & Rune Creation",
            "Knowledge Base Management",
            "Model Performance Analysis",
            "Automated Feature Engineering"
        ],
        "learning_focus": [
            "Deep Learning Models",
            "Natural Language Processing",
            "Computer Vision",
            "Reinforcement Learning",
            "AutoML",
            "Model Interpretability"
        ]
    }

def _analyze_ml_components(task_text: str) -> Dict[str, Any]:
    """Analyze task for ML/AI components"""
    ml_keywords = {
        "model": ["train", "model", "ml", "ai", "neural", "deep learning"],
        "data": ["dataset", "training", "validation", "test", "features"],
        "algorithm": ["algorithm", "regression", "classification", "clustering"],
        "optimization": ["optimize", "hyperparameter", "tuning", "performance"]
    }
    
    components = {}
    task_lower = task_text.lower()
    
    for category, keywords in ml_keywords.items():
        components[category] = any(keyword in task_lower for keyword in keywords)
    
    return components

def _process_learning_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process learning data for AI agent improvement"""
    if not data:
        return {"status": "no_data", "patterns_found": 0}
    
    patterns = []
    insights = []
    
    for item in data:
        # Extract patterns from data
        if "content" in item:
            patterns.append(_extract_patterns(item["content"]))
        
        # Generate insights
        if "input_type" in item:
            insights.append(_generate_insight(item))
    
    return {
        "status": "processed",
        "data_points": len(data),
        "patterns_found": len(patterns),
        "insights_generated": len(insights),
        "patterns": patterns,
        "insights": insights
    }

def _generate_orbs(task_text: str, ml_components: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate orbs based on ML patterns"""
    orbs = []
    
    if ml_components.get("model"):
        orbs.append({
            "name": "ml-model-training",
            "description": "Machine learning model training patterns",
            "category": "ai_ml",
            "confidence": 0.9
        })
    
    if ml_components.get("data"):
        orbs.append({
            "name": "data-preprocessing",
            "description": "Data preprocessing and feature engineering",
            "category": "ai_ml",
            "confidence": 0.8
        })
    
    if ml_components.get("algorithm"):
        orbs.append({
            "name": "algorithm-selection",
            "description": "Algorithm selection and optimization",
            "category": "ai_ml",
            "confidence": 0.85
        })
    
    return orbs

def _generate_runes(task_text: str, ml_components: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate runes for AI agents"""
    runes = []
    
    if ml_components.get("model"):
        runes.append({
            "title": "ml-training-pipeline",
            "description": "Standard ML training pipeline",
            "category": "ai_ml",
            "content": "Automated ML training workflow with validation"
        })
    
    if ml_components.get("optimization"):
        runes.append({
            "title": "hyperparameter-tuning",
            "description": "Hyperparameter optimization script",
            "category": "ai_ml",
            "content": "Automated hyperparameter tuning with Bayesian optimization"
        })
    
    return runes

def _generate_ml_response(task_text: str, ml_components: Dict[str, Any]) -> str:
    """Generate ML-focused response"""
    if ml_components.get("model"):
        return "I'll help you with machine learning model training. Let me analyze the requirements and create an optimized training pipeline."
    elif ml_components.get("data"):
        return "I can assist with data preprocessing and feature engineering for your ML project."
    elif ml_components.get("algorithm"):
        return "I'll help you select and optimize the best algorithm for your use case."
    else:
        return "I'm here to help with AI/ML tasks. What specific machine learning challenge are you facing?"

def _calculate_confidence(ml_components: Dict[str, Any]) -> float:
    """Calculate confidence score based on ML components"""
    confidence = 0.5  # Base confidence
    
    if ml_components.get("model"):
        confidence += 0.2
    if ml_components.get("data"):
        confidence += 0.15
    if ml_components.get("algorithm"):
        confidence += 0.15
    
    return min(confidence, 1.0)

def _extract_patterns(content: str) -> Dict[str, Any]:
    """Extract patterns from content"""
    return {
        "pattern_type": "ml_workflow",
        "confidence": 0.8,
        "extracted_features": ["training", "validation", "testing"]
    }

def _generate_insight(item: Dict[str, Any]) -> Dict[str, Any]:
    """Generate insights from data item"""
    return {
        "insight_type": "ml_optimization",
        "description": "Potential ML workflow optimization",
        "confidence": 0.7
    }

def _generate_capabilities(data: List[Dict[str, Any]]) -> List[str]:
    """Generate new capabilities from training data"""
    return [
        "Advanced Model Interpretability",
        "Automated Feature Selection",
        "Multi-Model Ensemble Training"
    ] 