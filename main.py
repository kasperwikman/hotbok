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



@app.get("/temp")
def temp():
    return {"message": "Hello World"}



rooms = [
        {"room_number": 101, "type": "Single", "price": 100},
        {"room_number": 102, "type": "Double", "price": 150},
        {"room_number": 103, "type": "Suite", "price": 250},
    ]

@app.get("/rooms")
def get_rooms():
    return rooms

@app.get("/rooms/{id}")
def get_one_room(id: int):
    try:
        return rooms[id]
    except:
        return {"error": "Room not found"}
    
@app.post("/bookings")
def create_booking(request: Request):
    return {"message": "Booking created successfully"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )
