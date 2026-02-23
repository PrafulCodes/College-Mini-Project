"""
Mock storage layer for Money Council
Provides in-memory storage for user plans
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# In-memory storage for plans
# Structure: {user_id: {"plan": [...], "created_at": timestamp, "updated_at": timestamp}}
_plans_db: Dict[int, Dict] = {}


def save_plan(user_id: int, plan: List[str]) -> Dict:
    """
    Save a user's action plan to storage.
    
    Args:
        user_id (int): Unique user identifier
        plan (List[str]): List of action items
        
    Returns:
        Dict: Stored plan data with metadata
        
    Example:
        save_plan(1, ["Pay debt", "Save money"])
        → {
            "user_id": 1,
            "plan": ["Pay debt", "Save money"],
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00"
          }
    """
    timestamp = datetime.now().isoformat()
    
    if user_id in _plans_db:
        # Update existing plan
        _plans_db[user_id]["plan"] = plan
        _plans_db[user_id]["updated_at"] = timestamp
        logger.info(f"Updated plan for user {user_id}")
    else:
        # Create new plan
        _plans_db[user_id] = {
            "user_id": user_id,
            "plan": plan,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        logger.info(f"Created new plan for user {user_id}")
    
    return _plans_db[user_id]


def get_plan(user_id: int) -> Optional[Dict]:
    """
    Retrieve a user's action plan from storage.
    
    Args:
        user_id (int): Unique user identifier
        
    Returns:
        Optional[Dict]: Plan data if found, None otherwise
        
    Example:
        get_plan(1)
        → {
            "user_id": 1,
            "plan": ["Pay debt", "Save money"],
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00"
          }
    """
    if user_id in _plans_db:
        logger.info(f"Retrieved plan for user {user_id}")
        return _plans_db[user_id]
    
    logger.warning(f"No plan found for user {user_id}")
    return None


def delete_plan(user_id: int) -> bool:
    """
    Delete a user's action plan from storage.
    
    Args:
        user_id (int): Unique user identifier
        
    Returns:
        bool: True if deleted, False if not found
    """
    if user_id in _plans_db:
        del _plans_db[user_id]
        logger.info(f"Deleted plan for user {user_id}")
        return True
    
    logger.warning(f"No plan found to delete for user {user_id}")
    return False


def list_all_plans() -> Dict[int, Dict]:
    """
    Retrieve all stored plans (for debugging/admin purposes).
    
    Returns:
        Dict: All plans indexed by user_id
    """
    logger.info(f"Retrieved {len(_plans_db)} total plans")
    return _plans_db.copy()


def clear_storage() -> None:
    """
    Clear all stored plans (for testing purposes).
    """
    global _plans_db
    _plans_db.clear()
    logger.info("Storage cleared")
