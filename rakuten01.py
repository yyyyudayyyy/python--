from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()
DB = "hotel.db"

def get_db():
    return sqlite3.connect(DB)

@app.get("/hotels")
def list_hotels(area: str = None):
    conn = get_db()
    cursor = conn.cursor()
    if area:
        cursor.execute("SELECT * FROM hotels WHERE area=? AND is_open=1", (area,))
    else:
        cursor.execute("SELECT * FROM hotels WHERE is_open=1")
    hotels = cursor.fetchall()
    conn.close()
    return {"hotels": hotels}

@app.get("/hotel/{hotel_id}/capacity")
def get_capacity(hotel_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT food_stock, water_stock FROM hotels WHERE id=?", (hotel_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Hotel not found")
    food, water = row
    capacity = min(food, water)  # 食料・水どちらか少ない方に制約される
    return {"hotel_id": hotel_id, "capacity": capacity}

@app.get("/suggest")
def suggest(current_hotel: int, area: str = None):
    """再宿泊先の提案"""
    conn = get_db()
    cursor = conn.cursor()
    # 現在のホテルを確認
    cursor.execute("SELECT area FROM hotels WHERE id=?", (current_hotel,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Current hotel not found")
    current_area = row[0]

    # 同じエリアで営業中の他ホテルを検索
    search_area = area or current_area
    cursor.execute("SELECT id, name FROM hotels WHERE area=? AND is_open=1 AND id != ?",
                   (search_area, current_hotel))
    hotels = cursor.fetchall()
    conn.close()

    return {"suggestions": hotels}
