
var socket = io();


socket.on('connect', function() {
    console.log('Connected to server');
});




socket.on('receive_arduino', function(data) {
    updateDisplay('fasting-value', data.sensorSpeed, 'М/С²');
});
socket.on('receive_arduino1', function(data) {
  updateDisplay('highe', data.sensorHigh, 'М');
});
socket.on('receive_arduino2', function(data) {
  updateDisplay('davleni', data.sensorDavlen, 'гПа');
});
socket.on('receive_arduino3', function(data) {
  updateDisplay('temp-value', data.sensorTemp, '°');
});
socket.on('receive_arduino4', function(data) {
  updateDisplay('humy', data.sensorHumidy, '%');
});
socket.on('receive_arduino5', function(data) {
  updateDisplay('speedy', data.sensorSpeedy, 'М/С'); 
});
socket.on('receive_arduino6', function(data) {
  updateDisplay('CO', data.sensorCO, 'ppm');
});



function updateDisplay(elementId, value, unit) {
  const displayElement = document.getElementById(elementId);
  if (displayElement) {
    displayElement.textContent = parseFloat(value) + unit; 
  } else {
    console.error("Element with id '" + elementId + "' not found.");
  }
}





setInterval(function() {
    socket.emit('request_arduino');
    socket.emit('request_number');
}, 500);
