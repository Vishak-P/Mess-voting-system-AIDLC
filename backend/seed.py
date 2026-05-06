"""
Seed script — populates MongoDB with dummy data.
Run: python seed.py
"""
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
import bcrypt

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mess_voting")
client = MongoClient(MONGO_URI)
db_name = MONGO_URI.split("/")[-1].split("?")[0] or "mess_voting"
db = client[db_name]


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed():
    # Clear existing data
    db.users.delete_many({})
    db.menus.delete_many({})
    db.votes.delete_many({})
    db.feedback.delete_many({})
    print("Cleared existing data.")

    # Users
    admin_id = ObjectId()
    student_ids = [ObjectId() for _ in range(5)]

    users = [
        {"_id": admin_id, "name": "Admin User", "email": "admin@mess.com", "password": hash_password("admin123"), "role": "admin", "created_at": datetime.utcnow()},
        {"_id": student_ids[0], "name": "Aarav Sharma", "email": "aarav@test.com", "password": hash_password("student123"), "role": "student", "created_at": datetime.utcnow()},
        {"_id": student_ids[1], "name": "Priya Patel", "email": "priya@test.com", "password": hash_password("student123"), "role": "student", "created_at": datetime.utcnow()},
        {"_id": student_ids[2], "name": "Rohan Gupta", "email": "rohan@test.com", "password": hash_password("student123"), "role": "student", "created_at": datetime.utcnow()},
        {"_id": student_ids[3], "name": "Sneha Reddy", "email": "sneha@test.com", "password": hash_password("student123"), "role": "student", "created_at": datetime.utcnow()},
        {"_id": student_ids[4], "name": "Arjun Singh", "email": "arjun@test.com", "password": hash_password("student123"), "role": "student", "created_at": datetime.utcnow()},
    ]
    db.users.insert_many(users)
    print(f"Inserted {len(users)} users.")

    # Menus
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    menus = []

    meal_dishes = {
        "breakfast": ["Idli Sambar", "Poha", "Aloo Paratha", "Upma", "Bread Omelette"],
        "lunch":     ["Dal Rice", "Rajma Chawal", "Chole Bhature", "Veg Biryani", "Paneer Butter Masala"],
        "dinner":    ["Roti Sabzi", "Fried Rice", "Pasta", "Dal Makhani", "Pulao"],
    }

    # Past 3 days (locked) + today + next 2 days (open)
    for day_offset in range(-3, 3):
        date = today + timedelta(days=day_offset)
        is_past = day_offset < 0
        for meal_type, dishes in meal_dishes.items():
            meal_hour = {"breakfast": 7, "lunch": 11, "dinner": 18}[meal_type]
            open_time = date
            deadline = date + timedelta(hours=meal_hour + 4)
            options = [{"_id": ObjectId(), "dish_name": d, "vote_count": 0} for d in dishes]
            menus.append({
                "_id": ObjectId(),
                "date": date,
                "meal_type": meal_type,
                "open_time": open_time,
                "deadline": deadline,
                "is_locked": is_past,
                "created_by": str(admin_id),
                "created_at": datetime.utcnow(),
                "options": options,
            })

    db.menus.insert_many(menus)
    print(f"Inserted {len(menus)} menus.")

    # Votes on past menus
    vote_count = 0
    past_menus = [m for m in menus if m["is_locked"]]
    for menu in past_menus:
        for i, student_id in enumerate(student_ids):
            option = menu["options"][i % len(menu["options"])]
            db.votes.insert_one({
                "user_id": str(student_id),
                "menu_id": str(menu["_id"]),
                "option_id": str(option["_id"]),
                "option_oid": option["_id"],
                "voted_at": menu["deadline"] - timedelta(minutes=30),
            })
            db.menus.update_one(
                {"_id": menu["_id"], "options._id": option["_id"]},
                {"$inc": {"options.$.vote_count": 1}}
            )
            vote_count += 1

    print(f"Inserted {vote_count} votes.")

    # Feedback on past menus
    fb_count = 0
    for menu in past_menus[:3]:
        for i, student_id in enumerate(student_ids[:3]):
            db.feedback.insert_one({
                "user_id": str(student_id),
                "menu_id": str(menu["_id"]),
                "rating": (i % 5) + 1,
                "comment": f"Great {menu['meal_type']}!" if i % 2 == 0 else None,
                "created_at": datetime.utcnow(),
            })
            fb_count += 1

    print(f"Inserted {fb_count} feedback entries.")
    print("\nSeed complete!")
    print("Admin:   admin@mess.com / admin123")
    print("Student: aarav@test.com / student123")


if __name__ == "__main__":
    seed()
