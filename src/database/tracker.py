import sqlite3
from datetime import datetime
from typing import List, Dict
from ..models.food_item import FoodItem, MealEntry

class FitnessTracker:
    def __init__(self, db_name: str = "fitness_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Initialize database tables"""
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS food_items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                calories REAL NOT NULL,
                protein REAL NOT NULL,
                carbs REAL NOT NULL,
                fat REAL NOT NULL,
                serving_size REAL NOT NULL,
                is_unit_based BOOLEAN NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS meal_entries (
                id INTEGER PRIMARY KEY,
                food_item_id INTEGER,
                amount REAL NOT NULL,
                date DATETIME NOT NULL,
                FOREIGN KEY (food_item_id) REFERENCES food_items (id)
            );
        """)
        self.conn.commit()

    def add_food_item(self, food_item: FoodItem) -> int:
        """Add a new food item to the database"""
        sql = """
            INSERT INTO food_items (name, calories, protein, carbs, fat, serving_size, is_unit_based)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (
            food_item.name, food_item.calories, food_item.protein,
            food_item.carbs, food_item.fat, food_item.serving_size,
            food_item.is_unit_based
        ))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_meal_entry(self, entry: MealEntry):
        """Add a meal entry to the database"""
        sql = """
            INSERT INTO meal_entries (food_item_id, amount, date)
            VALUES (?, ?, ?)
        """
        self.cursor.execute(sql, (entry.food_item_id, entry.amount, entry.date))
        self.conn.commit()

    def get_daily_totals(self, date: datetime) -> Dict[str, float]:
        """Calculate total macros and calories for a given date"""
        sql = """
            SELECT 
                SUM(f.calories * (m.amount / f.serving_size)) as total_calories,
                SUM(f.protein * (m.amount / f.serving_size)) as total_protein,
                SUM(f.carbs * (m.amount / f.serving_size)) as total_carbs,
                SUM(f.fat * (m.amount / f.serving_size)) as total_fat
            FROM meal_entries m
            JOIN food_items f ON m.food_item_id = f.id
            WHERE date(m.date) = date(?)
        """
        self.cursor.execute(sql, (date,))
        result = self.cursor.fetchone()
        return {
            "calories": result[0] or 0,
            "protein": result[1] or 0,
            "carbs": result[2] or 0,
            "fat": result[3] or 0
        }

    def search_food_items(self, query: str) -> List[FoodItem]:
        """Search for food items in the database"""
        sql = """
            SELECT id, name, calories, protein, carbs, fat, serving_size, is_unit_based
            FROM food_items
            WHERE name LIKE ?
        """
        self.cursor.execute(sql, (f"%{query}%",))
        return [FoodItem(*row) for row in self.cursor.fetchall()]