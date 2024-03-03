var map;
async function initMap1() {
    // Fetch data from the server
    const res = await fetch("/mumbai")
    const real_data = await res.json()
    console.log(real_data)

    // Initialize the map with broader view of Mumbai
    map = new mappls.Map('map', {
        center: { lat: 19.0760, lng: 72.877 }, // Centered around Mumbai // Adjust zoom level for a broader view
    });

    // Loop through the data to create markers and personalized cards
    for (let i = 0; i < real_data.data.length; i++) {
        const lat = real_data.data[i].latitude;
        const lng = real_data.data[i].longitude;

        var card = `
            <form action="/bookSlot" method="POST">
            <h3>${real_data.data[i].branch}</h3>
            <p>Connector Type: ${real_data.data[i].connector}</p>
            <p>Total Port: ${real_data.data[i].ports}</p>
            <p>KW: ${real_data.data[i].kw}</p>
            <p>Speed: ${real_data.data[i].speed}</p>
            <p>Address: ${real_data.data[i].address}</p>
            <p>Phone Number: ${real_data.data[i].phone}</p>
            <p>Opening Hours: ${real_data.data[i].hours}</p>
            <button type="submit" class="book-slot">Book Slot</button>
            </form>
        `;

        var Marker1 = new mappls.Marker({
            map: map,
            position: { "lat": lat, "lng": lng },
            popupHtml: card
        });
    }

    // Add event listener for the buttons within the personalized cards
    document.querySelectorAll('.book-slot').forEach(button => {
        button.addEventListener('click', () => {
            // Redirect to the /bookslot page
            window.location.href = '/bookslot';
        });
    });
}

const changeCity = async () => {
    const selectElement = document.querySelector('select');
    const selectedCity = selectElement.value;

    const res = await fetch("/" + selectedCity)
    const real_data = await res.json()
    console.log(real_data)

    // Initialize the map with broader view of Mumbai
    map = new mappls.Map('map', {
        center: { lat: 19.0760, lng: 72.877 }, // Centered around Mumbai // Adjust zoom level for a broader view
    });

    // Loop through the data to create markers and personalized cards
    for (let i = 0; i < real_data.data.length; i++) {
        const lat = real_data.data[i].latitude;
        const lng = real_data.data[i].longitude;

        var card = `
            <form action="/bookSlot" method="POST">
            <h3>${real_data.data[i].branch}</h3>
            <p>Connector Type: ${real_data.data[i].connector}</p>
            <p>Total Port: ${real_data.data[i].ports}</p>
            <p>KW: ${real_data.data[i].kw}</p>
            <p>Speed: ${real_data.data[i].speed}</p>
            <p>Address: ${real_data.data[i].address}</p>
            <p>Phone Number: ${real_data.data[i].phone}</p>
            <p>Opening Hours: ${real_data.data[i].hours}</p>
            <button type="submit" class="book-slot">Book Slot</button>
            </form>
        `;

        var Marker1 = new mappls.Marker({
            map: map,
            position: { "lat": lat, "lng": lng },
            popupHtml: card
        });
    }

}

document.addEventListener('DOMContentLoaded', initMap1);
