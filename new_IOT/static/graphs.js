console.log("Prediction:", prediction); // Log the prediction variable to ensure it contains the expected data

try {
    // Replace HTML character entity references with actual characters
    var decodedDataString = prediction.replace(/&#39;/g, '"');

    // Parse the string into a JavaScript object
    var dataObject = JSON.parse(decodedDataString);

    console.log("Parsed data:", dataObject); // Log the parsed array to verify its structure

    var timestamps = [];
    var outside_humidity = [];
    var outside_temperature = [];
    var frequency = [];

    // Iterate over each object in the array
    dataObject.forEach(function(item, index) {
        var timestamp = new Date(item.timestamp * 1000); // Convert timestamp to milliseconds
        var formattedTimestamp = timestamp.toLocaleString(); // Convert timestamp to local date and time string
        timestamps.push(formattedTimestamp); // Push formatted timestamp to the array

        outside_temperature.push(item.outside_temperature); // Access outside_temperature property
        outside_humidity.push(item.outside_humidity); // Access outside_humidity property
        frequency.push(item.frequency);
    });
} catch (error) {
    console.error("Error parsing JSON:", error);
}
var ctx = document.getElementById('lineChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            label: 'Inside temperature',
            data: outside_temperature,
            backgroundColor: [
                'rgba(85,85,85, 1)'

            ],
            borderColor: [
                'rgb(41, 155, 99)'
            ],
            borderWidth: 1
        },{
            label: 'Outside Temperature',
            data: [29.90,28.45,28.05,29.05,29.45,27.34,28.30,29.21,28.55,29.04],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true
    }
});

var ctx2 = document.getElementById('lineChart2').getContext('2d');
var myChart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            label: 'Inside Humidity',
            data: [65.23,66.01,63.21,64,21,65.09,66.05,66.45,65.55,65.73,66.21],
            backgroundColor: [
                'rgba(85,85,85, 1)'

            ],
            borderColor: [
                'rgb(41, 155, 99)'
            ],
            borderWidth: 1
        },{
            label: 'Outside Temperature',
            data: outside_humidity,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true
    }
});

var ctx3 = document.getElementById('lineChart3').getContext('2d');
var myChart = new Chart(ctx3, {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            label: 'Frequency',
            data: frequency,
            backgroundColor: [
                'rgba(85,85,85, 1)'

            ],
            borderColor: [
                'rgb(41, 155, 99)'
            ],
            borderWidth: 2.5
        }]
    },
    options: {
        responsive: true
    }
});