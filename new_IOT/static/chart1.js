var ctx = document.getElementById('lineChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7', 'Day8', 'Day9', 'Day10', 'Day11', 'Day12'],
        datasets: [{
            label: 'Inside temperature',
            data: [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75],
            backgroundColor: [
                'rgba(85,85,85, 1)'

            ],
            borderColor: [
                'rgb(41, 155, 99)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true
    }
});