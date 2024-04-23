var charts = {}; // Use an object to map canvasId to chart instances

function drawTopK(canvasId, label, data, yAxisLabel , mode) {
    // If a chart for this canvasId already exists, destroy it
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }

    const ctx = document.getElementById(canvasId).getContext('2d');
    var colors= [
        '#C5EBAA', // Light Green
        '#F6F193',  // Light Yellow
        '#F2C18D',   // Light Red
        '#DCBFFF', // Light Purple
    ];
    var temp = [];
    if(mode==0){
        myTitle = "TOP_K - word choices";
        label = data.map((_, index) => index == data.length - 1 ? 'Others' : `<${label[index]}`);
    }
    for (let i = colors.length; i < data.length; i++) {
        colors.push('rgba(54, 162, 235, 0.2)');
    }
    for (let i = 0; i < data.length; i++) {
        temp.push('rgba(54, 162, 235, 0.2)');
    }
    if(mode ==1){
        myTitle = "Frac(p) - real_prob / max(pred_prob)";
        label = data.map((_, index) => `${label[index]}`);
        const indexedData = data.map((value, index) => [value, index]);
        indexedData.sort((a, b) => b[0] - a[0]);
        const topIndices = indexedData.slice(0, 4).map(pair => pair[1]);
        for(let i=0;i<topIndices.length ;i++){
            temp[topIndices[i]] =  `rgba(54, 162, 235, ${1-0.2*i})`;
        }
        colors = temp;
    }
    if(mode ==2){
        myTitle = "Top 10 words Entropy";
        label = data.map((_, index) => `${label[index]}`);
        const indexedData = data.map((value, index) => [value, index]);
        indexedData.sort((a, b) => b[0] - a[0]);
        const topIndices = indexedData.slice(0, 4).map(pair => pair[1]);
        for(let i=0;i<topIndices.length ;i++){
            temp[topIndices[i]] =  `rgba(54, 162, 235, ${1-0.2*i})`;
        }
        colors = temp;
    }

    // Store the new chart instance in the charts map, using canvasId as the key
    charts[canvasId] = new Chart(ctx, {
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
            },
            plugins: {
                legend: {
                    display: false, // Ensure legend is displayed
                }
            }
        }
    });
}
function getColor(rank,countArray) {

    const colors = [
    '#C5EBAA', // Light Green
    '#F6F193',  // Light Yellow
    '#F2C18D',   // Light Red
    '#DCBFFF', // Light Purple
    ];

    if (rank <= countArray[0]) return colors[0]; // Light Green for rank 1
    if (rank > countArray[0] && rank <= countArray[1]) return colors[1]; // Light Purple for ranks 2-10
    if (rank > countArray[1] && rank <= countArray[2]) return colors[2]; // Light Red for ranks 11-20
    if(rank > countArray[2] && rank <= countArray[3]) return colors[3];
    else return "white"
}

function drawColorTextBox(wordsData, countArray, tips) {
    const container = document.getElementById('colorTextBox');
    let htmlContent = '<div class="LMF">';

    wordsData.forEach((data, index) => {
        const color = getColor(data[1], countArray);
        // Generate HTML content for each token, including a data attribute for the index
        htmlContent += `<div class="token" style="background-color: ${color};" data-index="${index}">${data[0]}</div>`;
    });

    htmlContent += '</div>';
    container.innerHTML = htmlContent;

    // Create a single tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip hidden';
    document.body.appendChild(tooltip);

    // Add event listeners for each token
    container.querySelectorAll('.token').forEach(token => {
    token.addEventListener('mouseenter', (e) => {
        const index = token.getAttribute('data-index');
        const tip = tips[index];
        // Format the tooltip content with topk, prob, and fracp values
        tooltip.innerHTML = `Token: ${e.target.innerText}<br>Topk: ${tip[0]}<br>Prob: ${tip[1]}<br>Fracp: ${tip[2]}`;

        // Get the bounding rectangle of the token
        const tokenRect = token.getBoundingClientRect();

        // Position the tooltip at the bottom-right of the token
        // Adjust as necessary for your layout
        tooltip.style.left = `${event.clientX+20}px`;
        tooltip.style.top = `${event.clientY-100}px`; // 20px offset for visibility

        tooltip.classList.remove('hidden');
    });

    token.addEventListener('mouseleave', () => {
        tooltip.classList.add('hidden');
    });
});
}
document.addEventListener('DOMContentLoaded', () => {
    const gltrSwitch = document.getElementById('flexSwitchCheckDefault');
    const gltrResults = document.querySelector('.GLTR');
    gltrResults.style.display = 'flex';
});

let lastExecutionTime = 0;
const throttleDuration = 100; // Throttle duration in milliseconds

document.addEventListener('mousemove', function(event) {
    const now = Date.now();

    if (now - lastExecutionTime > throttleDuration) {
        lastExecutionTime = now;

        const mouseX = event.clientX;
        const mouseY = event.clientY;
        // console.log(`Mouse X: ${mouseX}, Mouse Y: ${mouseY}`);
    }
});