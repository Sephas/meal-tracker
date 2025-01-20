from datetime import datetime
from models.food_item import FoodItem, MealEntry
from database.tracker import FitnessTracker

def main():
    tracker = FitnessTracker()
    
    # Add some sample food items
    chicken = FoodItem(
        id=None,
        name="Chicken Breast",
        calories=165,
        protein=31,
        carbs=0,
        fat=3.6,
        serving_size=100  # per 100g
    )
    
    # Add food item to database
    chicken_id = tracker.add_food_item(chicken)
    
    # Add a meal entry
    meal = MealEntry(
        id=None,
        food_item_id=chicken_id,
        amount=200,  # 200g of chicken
        date=datetime.now()
    )
    tracker.add_meal_entry(meal)
    
    # Get daily totals
    totals = tracker.get_daily_totals(datetime.now())
    print(f"Daily totals: {totals}")

if __name__ == "__main__":
    main()