import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

PORT=8523

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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
