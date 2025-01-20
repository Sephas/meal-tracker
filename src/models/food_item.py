from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class FoodItem:
    """Represents a food item in the database"""
    id: Optional[int]
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    serving_size: float  # in grams
    is_unit_based: bool = False  # True for items like "1 Big Mac"

@dataclass
class MealEntry:
    """Represents a single meal entry"""
    id: Optional[int]
    food_item_id: int
    amount: float  # grams or units
    date: datetime