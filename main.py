import os, uvicorn, psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date

PORT=8523

# load environment variables from .env file
load_dotenv()
DB_URL = os.getenv("DB_URL")

conn = psycopg.connect(
    DB_URL,
    autocommit=True,
    row_factory=dict_row,
)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date
    addinfo: str

@app.get("/temp")
def temp():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM messages")
        messages = cur.fetchall()
        return messages


@app.get("/rooms")
def get_rooms():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms ORDER BY room_number")
        rooms = cur.fetchall()
        return rooms

@app.get("/rooms/{id}")
def get_one_room(id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms WHERE id = %s", [id])
        room = cur.fetchone()  # Fetch a single room
        if room:
            return room
        else:
            return {"error": "Room not found"}
        
@app.get("/bookings")
def get_bookings():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                hb.id AS booking_id,
                hg.firstname || ' ' || hg.lastname AS guest_name,
                hr.room_number AS room_number,
                hb.datefrom,
                hb.dateto,
                hb.addinfo
            FROM hotel_bookings hb
            INNER JOIN hotel_guests hg ON hb.guest_id = hg.id
            INNER JOIN hotel_rooms hr ON hb.room_id = hr.id
            ORDER BY hb.datefrom
        """)
        bookings = cur.fetchall()
        return bookings
    
@app.post("/bookings")
def create_booking(booking: Booking):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO hotel_bookings (guest_id, room_id, datefrom, dateto, addinfo) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            [booking.guest_id, 
             booking.room_id, 
             booking.datefrom, 
             booking.dateto,
             booking.addinfo],
        )
        booking_id = cur.fetchone()['id']
    return {"message": "Booking created successfully", "booking_id": booking_id}


# _________________if statement in python_____________________

@app.get("/if/{user_input}")
def iftest (user_input: str):
    message = None # None = null
    if user_input == "hello" or user_input == "hi":
        message = user_input + " to you too"
    elif user_input == "bye":
        message = "bye bye"
    else:
        message = f"I don't understand {user_input}"
    return {"message:": message}



#_____________________________________uvicorn config____________________________________________

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )
