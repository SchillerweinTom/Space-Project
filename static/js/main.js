const API_BASE_URL = 'http://localhost:5000/api';

const tabButtons = document.querySelectorAll('.nav-button');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.style.display = 'none');
        button.classList.add('active');
        document.getElementById(tabName).style.display = 'block';
    });
});

document.getElementById('missionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const destination = document.getElementById('destination').value;
    const payloadMass = document.getElementById('payloadMass').value;
    const rocket = document.getElementById('rocket').value;

    try {
        const fuelResponse = await fetch(`${API_BASE_URL}/fuel`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ destination, payload_mass: Number(payloadMass) }),
        });
        const fuelData = await fuelResponse.json();

        const costResponse = await fetch(`${API_BASE_URL}/cost_estimate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rocket, payload_mass: Number(payloadMass) }),
        });
        const costData = await costResponse.json();

        document.getElementById('missionData').innerHTML = `
            <p><strong>Destination:</strong> ${fuelData.destination}</p>
            <p><strong>Distance:</strong> ${fuelData.distance_km} km</p>
            <p><strong>Fuel Needed:</strong> ${fuelData.fuel_needed_kg} kg</p>
            <p><strong>Travel Time:</strong> ${fuelData.travel_time_days} days</p>
            `;
        document.getElementById('costEstimate').innerHTML = `
            <p><strong>Estimated Cost:</strong> ${costData.estimated_cost}</p>
            `;
        document.getElementById('missionResults').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while calculating the mission. Please try again.');
    }
});

document.getElementById('rocketForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const rocketName = document.getElementById('rocketInfo').value.toLowerCase().replace(" ", "");
    if (rocketName) {
        try {
            const response = await fetch(`${API_BASE_URL}/rocket/${rocketName}`);
            const data = await response.json();

            if (data.error) {
                alert(data.error);
            } else {
                // Handle multiple payloads
                let payloadHtml = '';
                data.Payload.forEach(payload => {
                    payloadHtml += `
                        <p><strong>Payload Capacity:</strong> ${payload.kg} kg to ${payload.name}</p>
                    `;
                });

                document.getElementById('rocketData').innerHTML = `
                    ${payloadHtml}
                    <p><strong>Cost per Launch:</strong> $${data.Cost}</p>
                    <p><strong>Mass:</strong> ${data.Mass} kg</p>
                    <p><strong>Images:</strong></p>
                    <div class="image-container">
                    ${data.flickr_images.map((image) => {
                        return `<img src="${image}" alt="Rocket Image" style="max-width: 100%; margin-bottom: 10px;"/>`;
                    }).join('')}
                    </div>
                `;
                document.getElementById('rocketResults').style.display = 'block';
            }
        } catch (error) {
            console.error('Error fetching rocket info:', error);
            alert('An error occurred while fetching rocket information. Please try again.');
        }
    }
});

document.getElementById('routeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const destination = document.getElementById('routeDestination').value;
    try {
        const response = await fetch(`${API_BASE_URL}/route`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ destination }),
        });
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        document.getElementById('routeMap').src = url;
        document.getElementById('routeResults').style.display = 'block';
    } catch (error) {
        console.error('Error generating route map:', error);
        alert('An error occurred while generating the route map. Please try again.');
    }
});

 document.addEventListener("DOMContentLoaded", () => {
    const destinationSelect = document.getElementById('destination');
    const destinationSelect2 = document.getElementById('routeDestination');
    const rocketSelect = document.getElementById('rocket');
    const rocketSelect2 = document.getElementById('rocketInfo');

    fetch(`${API_BASE_URL}/destinations/all`)
        .then(response => response.json())
        .then(destinations => {
            destinations.forEach(destination => {
                const option = document.createElement('option');
                option.value = destination;
                option.textContent = destination;
                destinationSelect.add(option);
            });
        })
        .catch(error => console.error('Error loading destinations:', error));

    fetch(`${API_BASE_URL}/rockets`)
        .then(response => response.json())
        .then(data => {
            const rocketNames = data.names;
            rocketNames.forEach(name => {
                const option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                rocketSelect.add(option);
            });
        })
        .catch(error => console.error('Error loading rockets:', error));

    fetch(`${API_BASE_URL}/destinations/route`)
        .then(response => response.json())
        .then(destinations => {
            destinations.forEach(destination => {
                const option = document.createElement('option');
                option.value = destination;
                option.textContent = destination;
                destinationSelect2.add(option)
            });
        })
        .catch(error => console.error('Error loading destinations:', error));

    fetch(`${API_BASE_URL}/rockets`)
        .then(response => response.json())
            .then(data => {
                const rocketNames = data.names;
                rocketNames.forEach(name => {
                    const option = document.createElement('option');
                    option.value = name;
                    option.textContent = name;
                    rocketSelect2.add(option);
            });
        })
        .catch(error => console.error('Error loading rockets:', error));
 });


 document.addEventListener("DOMContentLoaded", () => {
    const dialogOverlay = document.getElementById("imageDialog");
    const dialogImage = document.getElementById("dialogImage");
    const closeButton = dialogOverlay.querySelector(".close-button");
    const images = document.querySelectorAll(".image-route");

    images.forEach(image => {
        image.addEventListener("click", () => {
            dialogImage.src = image.src;
            dialogOverlay.style.display = "flex";
        });
    });

    closeButton.addEventListener("click", () => {
        dialogOverlay.style.display = "none";
    });

    dialogOverlay.addEventListener("click", (e) => {
        if (e.target === dialogOverlay) {
            dialogOverlay.style.display = "none";
        }
    });
});