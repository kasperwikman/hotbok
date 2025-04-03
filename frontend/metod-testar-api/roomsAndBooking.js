async function fetchRooms() {
    {
        const response = await fetch('http://vm4430.kaj.pouta.csc.fi:8523/rooms');
        const data = await response.json();
        const roomList = document.getElementById('room-list');
        roomList.innerHTML = '';
        data.forEach(room => {
            const listItem = document.createElement('li');
            listItem.textContent = `Room ${room.room_number} - ${room.type} - $${room.price}`;
            roomList.appendChild(listItem);
        });
    }
}

fetchRooms();