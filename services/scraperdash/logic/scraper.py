import os
import json
from datetime import datetime

def scan_local_logs(log_dir="storage/logs/"):
    """Scan local log files and extract insights"""
    if not os.path.exists(log_dir):
        return []
    
    logs = []
    for filename in os.listdir(log_dir):
        if filename.endswith(".json"):
            with open(os.path.join(log_dir, filename), "r") as f:
                try:
                    log_data = json.load(f)
                    logs.append({
                        "filename": filename,
                        "data": log_data,
                        "timestamp": log_data.get("timestamp", datetime.utcnow().isoformat())
                    })
                except json.JSONDecodeError:
                    continue
    
    return sorted(logs, key=lambda x: x["timestamp"], reverse=True)

def extract_agent_insights(logs):
    """Extract insights from agent logs"""
    insights = {
        "success_rate": 0,
        "common_errors": [],
        "agent_performance": {},
        "task_patterns": []
    }
    
    if not logs:
        return insights
    
    success_count = 0
    error_patterns = {}
    agent_stats = {}
    
    for log in logs:
        data = log["data"]
        status = data.get("status", "unknown")
        
        if status == "completed":
            success_count += 1
        
        # Track agent performance
        agent = data.get("agent", "unknown")
        if agent not in agent_stats:
            agent_stats[agent] = {"success": 0, "failed": 0}
        
        if status == "completed":
            agent_stats[agent]["success"] += 1
        else:
            agent_stats[agent]["failed"] += 1
    
    insights["success_rate"] = success_count / len(logs) if logs else 0
    insights["agent_performance"] = agent_stats
    
    return insights 