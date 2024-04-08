$(document).ready(function() {
    $("#detect-button").click(function() {
        var text = $("#text-input").val();
         $.ajax({
            url: "/GLTR_detect",
            type: "POST",
            data: { text: text },
            success: function(response) {
                console.log("GLTR_detect");
                drawHistogram("topKCount",Object.keys(response),Object.values(response),"topKCount");
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
        $.ajax({
            url: "/detect",
            type: "POST",
            data: { text: text },
            success: function(response) {
                $("#result").text("LLM Detection Result: " + response);
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});


function drawHistogram(canvasId, label, data, yAxisLabel) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    // Define colors for the first four bars
    const colors= [
    '#C5EBAA', // Light Green
    '#F6F193',  // Light Yellow
    '#F2C18D',   // Light Red
    '#DCBFFF', // Light Purple
    ]
    // If there are more than 4 data points, default the rest to a standard color
    for (let i = colors.length; i < data.length; i++) {
        colors.push('rgba(54, 162, 235, 0.2)'); // Default color for additional bars
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map((_, index) => `<${label[index]}`), // Adjust if you want specific labels
            datasets: [{
                label: label,
                data: data,
                backgroundColor: colors, // Use the colors array here
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: yAxisLabel
                    }
                }
            }
        }
    });
}