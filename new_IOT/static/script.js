
var harvestAlertValue = parseFloat(document.getElementById('harvest_card').dataset.harvestAlert);
var harvestCard = document.getElementById('harvest_card');
var harvestCardName = document.getElementById('harvest_card_name');
var harvestCardIcon = document.getElementById('harvest_card_icon');

var swarmingAlertValue = parseFloat(document.getElementById('swarm_card').dataset.swarmingAlert);
var swarmCard = document.getElementById('swarm_card');
var swarmCardName = document.getElementById('swarm_card_name');
var swarmCardIcon = document.getElementById('swarm_card_icon');

var feedingAlertValue = parseFloat(document.getElementById('rain_card').dataset.feedingNeed);
var feedCard = document.getElementById('rain_card');
var feedCardName = document.getElementById('rain_card_name');
var feedCardIcon = document.getElementById('rain_card_icon');   

var healthCard = document.getElementById('health_card');
var healthCardName = document.getElementById('health_card_name');
var healthCardIcon = document.getElementById('health_card_icon');  

var extremeAlertValue = parseFloat(document.getElementById('extreme_card').dataset.extremeAlert);
var extremeCard = document.getElementById('extreme_card');
var extremeCardName = document.getElementById('extreme_card_name');
var extremeCardIcon = document.getElementById('extreme_card_icon');


if (35 <= extremeAlertValue) {
    extremeCardName.innerText = 'Extreme Temperature Detected';  // Change to your desired color
    extremeCardName.style.color = 'red';
    extremeCardIcon.innerHTML = '<img src="/static/images/alert.png" alt="alert image">';
} else {
    extremeCardName.innerText = 'No Extreme Temperture Detected';  
    extremeCardName.style.color = 'green';// Change to your desired color
    extremeCardIcon.innerHTML = '<img src="/static/images/check.png" alt="check image">';
}

if (14 <= harvestAlertValue) {
    harvestCardName.innerText = 'Ready to Harvest';  // Change to your desired color
    harvestCardName.style.color = 'red';
    harvestCardIcon.innerHTML = '<img src="/static/images/alert.png" alt="alert image">';
} else {
    harvestCardName.innerText = 'No Harvesting Needed';  
    harvestCardName.style.color = 'green';// Change to your desired color
    harvestCardIcon.innerHTML = '<img src="/static/images/check.png" alt="check image">';
}

// Add your logic to change the card color and icon based on the swarming alert value
// Example:
if (400 <= swarmingAlertValue && swarmingAlertValue <= 500) {
    swarmCardName.innerText = 'Swarming Detected';  // Change to your desired color
    swarmCardName.style.color = 'red';
    swarmCardIcon.innerHTML = '<img src="/static/images/alert.png" alt="alert image">';
} else {
    swarmCardName.innerText = 'No Swarming Detected';  
    swarmCardName.style.color = 'green';// Change to your desired color
    swarmCardIcon.innerHTML = '<img src="/static/images/check.png" alt="check image">';
}



if (50 <= feedingAlertValue && feedingAlertValue <= 100) {
    feedCardName.innerText = 'Feeding Required';  // Change to your desired color
    feedCardName.style.color = 'red';
    feedCardIcon.innerHTML = '<img src="/static/images/alert.png" alt="alert image">';
} else {
    feedCardName.innerText =  'Feeding Not Required.';  
    feedCardName.style.color = 'green';// Change to your desired color
    feedCardIcon.innerHTML = '<img src="/static/images/check.png" alt="check image">';
}



if (prediction == "Unhealthy") {
    healthCardName.innerText = 'Unhealthy Hive';
    healthCardName.style.color = 'red';
    healthCardIcon.innerHTML = '<img src="/static/images/alert.png" alt="alert image">';
}
    
 else {
    healthCardName.innerText =  'Healthy Hive';  
    healthCardName.style.color = 'green';
    healthCardIcon.innerHTML = '<img src="/static/images/check.png" alt="check image">';
}

let progressCircular = document.querySelector(".progress-circular");
let value = document.querySelector(".value");
let startWeight = 0;

// Assuming maxWeight is 100 kg
let maxWeight = 20;

// Set the initial value and gradient
updateProgress(Weight);

// Function to update the progress
function updateProgress(weight) {
    value.textContent = `${weight} Kg`;
    let percentage = (weight / maxWeight) * 100;
    progressCircular.style.background = `conic-gradient(goldenrod ${percentage * 3.6}deg, #ededed 0deg)`;
}





