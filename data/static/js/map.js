
var map = L.map('map').setView([53.2464, 10.4115], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
const markers = JSON.parse(document.getElementById("markers-data").textContent);
let feature = L.geoJSON(markers, {
  onEachFeature: function (point, layer) {
    layer.bindPopup('<p>'+point.properties.date_time+'</p><p>type: '+point.properties.type+'</p><p>database: '+point.properties.database+'</p>');
  }}).addTo(map);
map.fitBounds(feature.getBounds(), { padding: [100, 100] });
