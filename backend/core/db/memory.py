"""
In-memory database store for LinkOps
This provides a simple in-memory storage solution that can be replaced with Redis or a real database later.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

# In-memory stores
TASK_STORE: Dict[str, Dict[str, Any]] = {}
QA_STORE: Dict[str, Dict[str, Any]] = {}
INFO_DUMP_STORE: Dict[str, Dict[str, Any]] = {}
IMAGE_EXTRACTION_STORE: Dict[str, Dict[str, Any]] = {}
CHAT_HISTORY: List[Dict[str, Any]] = []

class MemoryStore:
    """Simple in-memory store with basic CRUD operations"""
    
    def __init__(self, store_name: str):
        self.store_name = store_name
        self.store = self._get_store(store_name)
    
    def _get_store(self, store_name: str) -> Dict[str, Any]:
        """Get the appropriate store based on name"""
        stores = {
            'tasks': TASK_STORE,
            'qa': QA_STORE,
            'info_dumps': INFO_DUMP_STORE,
            'image_extractions': IMAGE_EXTRACTION_STORE,
            'chat_history': CHAT_HISTORY
        }
        return stores.get(store_name, {})
    
    def create(self, data: Dict[str, Any], item_id: Optional[str] = None) -> str:
        """Create a new item in the store"""
        if not item_id:
            item_id = str(uuid.uuid4())
        
        data['id'] = item_id
        data['created_at'] = datetime.utcnow().isoformat()
        data['updated_at'] = datetime.utcnow().isoformat()
        
        if isinstance(self.store, dict):
            self.store[item_id] = data
        elif isinstance(self.store, list):
            self.store.append(data)
        
        return item_id
    
    def get(self, item_id: str) -> Dict[str, Any]:
        """Get an item by ID"""
        if isinstance(self.store, dict):
            return self.store.get(item_id, {})
        return {}
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all items"""
        if isinstance(self.store, dict):
            return list(self.store.values())
        return self.store
    
    def update(self, item_id: str, data: Dict[str, Any]) -> bool:
        """Update an existing item"""
        if isinstance(self.store, dict) and item_id in self.store:
            self.store[item_id].update(data)
            self.store[item_id]['updated_at'] = datetime.utcnow().isoformat()
            return True
        return False
    
    def delete(self, item_id: str) -> bool:
        """Delete an item"""
        if isinstance(self.store, dict) and item_id in self.store:
            del self.store[item_id]
            return True
        return False
    
    def search(self, **filters) -> List[Dict[str, Any]]:
        """Search items by filters"""
        results = []
        items = self.get_all()
        
        for item in items:
            match = True
            for key, value in filters.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                results.append(item)
        
        return results

# Convenience functions
def get_task_store() -> MemoryStore:
    return MemoryStore('tasks')

def get_qa_store() -> MemoryStore:
    return MemoryStore('qa')

def get_info_dump_store() -> MemoryStore:
    return MemoryStore('info_dumps')

def get_image_extraction_store() -> MemoryStore:
    return MemoryStore('image_extractions')

def get_chat_history_store() -> MemoryStore:
    return MemoryStore('chat_history') 