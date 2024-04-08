function cumulativeAverage(arr) {
    let sum = 0;
    let cumulativeAvg = arr.map((value, index) => {
        sum += value;
        return sum / (index + 1);
    });
    return cumulativeAvg;
}

