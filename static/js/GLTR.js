

function drawTopK(canvasId, label, data, yAxisLabel , mode) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    var colors= [
    '#C5EBAA', // Light Green
    '#F6F193',  // Light Yellow
    '#F2C18D',   // Light Red
    '#DCBFFF', // Light Purple
    ]
    var label;
    var myTitle;
    var temp = [];
    if(mode==0){
        myTitle = "TOP_K - word choices"
        label = data.map((_, index) => index == data.length - 1 ? 'Others' : `<${label[index]}`);
    }
    for (let i = colors.length; i < data.length; i++) {
        colors.push('rgba(54, 162, 235, 0.2)');
    }
    for (let i = 0; i < data.length; i++) {
        temp.push('rgba(54, 162, 235, 0.2)');
    }
    if(mode ==1){
        myTitle = "Frac(p) - real_prob / max(pred_prob)"
        label = data.map((_, index) => `${label[index]}`)
        const indexedData = data.map((value, index) => [value, index]);
        indexedData.sort((a, b) => b[0] - a[0]);
        const topIndices = indexedData.slice(0, 4).map(pair => pair[1]);
        for(let i=0;i<topIndices.length ;i++){
            temp[topIndices[i]] =  `rgba(54, 162, 235, ${1-0.2*i})`;
        }
        colors = temp;
    }
    if(mode ==2){
   myTitle = "Top 10 words Entropy"
        label = data.map((_, index) => `${label[index]}`)
        const indexedData = data.map((value, index) => [value, index]);
        indexedData.sort((a, b) => b[0] - a[0]);
        const topIndices = indexedData.slice(0, 4).map(pair => pair[1]);
        for(let i=0;i<topIndices.length ;i++){
            temp[topIndices[i]] =  `rgba(54, 162, 235, ${1-0.2*i})`;
        }
        colors = temp;
    }


    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: label,
            datasets:[{
                label: myTitle,
                data: data,
                backgroundColor: colors,
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
        },
            plugins: {
                legend: {
                    display: false, // Ensure legend is displayed
                }
            }
    });
}

function test(){
var ctx = document.getElementById('myChart').getContext('2d');

// Assuming you have some way of calculating these or have them pre-calculated
var lowerQuartile = 25;
var upperQuartile = 75;
var median = 50;

var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Dataset 1'], // Your labels here
        datasets: {
            label: 'Example Data',
            data: [100], // Your data here
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }

       }
    }
});

}