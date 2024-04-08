<script>
document.getElementById('detect-button').addEventListener('click', function() {
    fetch('/GLTR_data')
    .then(response => response.json())
    .then(data => {
        // Assuming 'data' contains 'real_topk', 'fracP', and 'top10Entropy' properties with arrays of data for the histograms
        drawHistogram('topKCount', 'Top K Count', data.real_topk, 'Frequency');
        drawHistogram('fracPHistogram', 'Frac(p) Histogram', data.fracP, 'Distribution');
        drawHistogram('top10Entropy', 'Top 10 Entropy(p)', data.top10Entropy, 'Entropy');
    })
    .catch(error => console.error('Error:', error));
});

function drawHistogram(canvasId, label, data, yAxisLabel) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map((_, index) => `Token ${index + 1}`),
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
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
</script>