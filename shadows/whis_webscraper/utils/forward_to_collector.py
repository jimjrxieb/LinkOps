import requests
import json


def forward_payload(data: dict):
    """Forward data to the data collector service"""
    try:
        # Forward to data collector service
        res = requests.post(
            "http://data-collector:8001/api/collect/info", json=data, timeout=10
        )
        return res.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Data collector service not available"}
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except Exception as e:
        return {"error": str(e)}


def forward_to_whis(data: dict):
    """Forward data to Whis for retraining"""
    try:
        res = requests.post("http://whis:8003/api/whis/train", json=data, timeout=10)
        return res.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Whis service not available"}
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except Exception as e:
        return {"error": str(e)}
