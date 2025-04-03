import os, uvicorn, psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

PORT=8523

# load environment variables from .env file
load_dotenv()
DB_URL = os.getenv("DB_URL")

print(DB_URL)

# Connect to the database

conn = psycopg.connect(
    DB_URL,
    autocommit=True,
    row_factory=dict_row,
)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/if/{user_input}")
def iftest (user_input: str):
    message = None # None = null
    if user_input == "hello":
        message = "hello to you too"
    elif user_input == "bye":
        message = "bye bye"
    else:
        message = "I don't understand"
    return {"message:": message}

@app.get("/temp")
def temp():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM messages")
        messages = cur.fetchall()
        return messages


@app.get("/rooms")
def get_rooms():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms")
        rooms = cur.fetchall()
        return rooms

@app.get("/rooms/{id}")
def get_one_room(id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms WHERE id = %s", (id,))
        room = cur.fetchone()  # Fetch a single room
        if room:
            return room
        else:
            return {"error": "Room not found"}
    
@app.post("/bookings")
def create_booking(request: Request):
    return {"message": "Booking created successfully"}




#_____________________________________uvicorn config____________________________________________

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )
