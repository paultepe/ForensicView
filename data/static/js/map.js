
var map = L.map('map').setView([51.505, -0.09], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
const markers = JSON.parse(document.getElementById("markers-data").textContent);
let feature = L.geoJSON(markers)
    .bindPopup(function (layer) {
        return layer.feature.properties.date_time;
    })
    .addTo(map);
map.fitBounds(feature.getBounds(), { padding: [100, 100] });
