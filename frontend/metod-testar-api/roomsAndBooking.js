async function fetchRooms() {
    const response = await fetch('http://vm4430.kaj.pouta.csc.fi:8523/rooms');
    const data = await response.json();
    const roomList = document.getElementById('room-list');
    const roomSelect = document.getElementById('room-select');
    roomList.innerHTML = '';
    roomSelect.innerHTML = '';

    data.forEach(room => {
        // Add room to the list
        const listItem = document.createElement('li');
        listItem.textContent = `Room ${room.room_number} - ${room.type} - $${room.price}`;
        roomList.appendChild(listItem);

        // Add room to the dropdown
        const option = document.createElement('option');
        option.value = room.id; // Assuming the room has an 'id' field
        option.textContent = `Room ${room.room_number} - ${room.type}`;
        roomSelect.appendChild(option);
    });
}

async function submitBooking() {
    const roomId = document.getElementById('room-select').value;
    const dateFrom = document.getElementById('datefrom').value;
    const dateTo = document.getElementById('dateto').value;
    const addInfo = document.getElementById('addinfo').value;

    if (!roomId || !dateFrom || !dateTo) {
        alert("Please fill in all required fields.");
        return;
    }

    const booking = {
        guest_id: 1, // hardcoded guest_id atm
        room_id: parseInt(roomId),
        datefrom: dateFrom,
        dateto: dateTo,
        addinfo: addInfo
    };

    const response = await fetch('http://vm4430.kaj.pouta.csc.fi:8523/bookings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(booking)
    });

    if (response.ok) {
        alert("Booking submitted successfully!");
        fetchBookings();
    } else {
        alert("Failed to submit booking.");
    }
}

// function to fetch bookings and display them in the list

async function fetchBookings() {
    const response = await fetch('http://vm4430.kaj.pouta.csc.fi:8523/bookings');
    const data = await response.json();
    const bookingList = document.getElementById('booking-list');
    bookingList.innerHTML = '';

    data.forEach(booking => {
        const listItem = document.createElement('li');
        listItem.textContent = `Booking ID: ${booking.id}, Room ID: ${booking.room_id}, From: ${booking.datefrom}, To: ${booking.dateto}, Info: ${booking.addinfo}`;
        bookingList.appendChild(listItem);
    });
}
fetchBookings();
fetchRooms();