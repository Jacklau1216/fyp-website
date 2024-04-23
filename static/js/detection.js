$(document).ready(function() {
    $("#detect-button").click(function() {
        $("#result").text("")
        $("#percentage").text("")
        $('#watermark').text("")
        document.getElementById('detailed_result').innerHTML = '<div></div>'

        var text = $("#text-input").val();
         $.ajax({
            url: "/GLTR_detect",
            type: "POST",
            data: { text: text },
            success: function(response) {
                console.log("GLTR_detect");
                drawTopK("topKCount",Object.keys(response.topk),Object.values(response.topk),"topKCount",0);
                drawTopK("fracPHistogram",Object.keys(response.fracp),Object.values(response.fracp),"Frac(p)",1);
                drawTopK("top10Entropy",Object.keys(response.top10Entropy),Object.values(response.top10Entropy),"Top 10 Entropy",2);
//                console.log(response.pop_up_display)
                drawColorTextBox(response.topk_display,response.countArray,response.pop_up_display);
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
                console.log(response)
                $("#result").text("LLM Detection Result: " + response[0]);
                $("#percentage").text("Text is Generated by LLM : " + response[1]*100 + "%");
                $("#watermark").text("Watermark detection result: "+response[4]);
                VisualizeResult(response[2], response[3]);
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
    
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/upload_file',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');

            },
        });
    });

    $('#detect-file-button').click(function(event){
        
        event.preventDefault(); // 阻止表單的默認提交行為
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/detect_file',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
                console.log(data)
                $("#result").text("LLM Detection Result: " + data[0]);
                $("#percentage").text("Text is Generated by LLM %: " + data[1]*100 + "%");
                VisualizeResult(data[2], data[3]);
                drawTopK("topKCount",Object.keys(data.topk),Object.values(data.topk),"topKCount",0);
                drawTopK("fracPHistogram",Object.keys(data.fracp),Object.values(data.fracp),"Frac(p)",1);
                drawTopK("top10Entropy",Object.keys(data.top10Entropy),Object.values(data.top10Entropy),"Top 10 Entropy",2);
//                console.log(data.pop_up_display)
                drawColorTextBox(data.topk_display,data.countArray,data.pop_up_display);
            },
        });
    })
});

function VisualizeResult(wordsData, tips) {
    const container = document.getElementById('detailed_result');
    let htmlContent = '<div class="LMF">';

    const colors = [
        '#FFBF00', // Amber
        '#F6F193',  // Light Yellow
        ];
    
    wordsData.forEach((data, index) => {
        let color = "white";
        if (data.result == true) {
            if (data.percentage >= 0.75) {
                color = colors[0];
            }
            else {
                color = colors[1];
            }
        }
        // Generate HTML content for each chunk, including a data attribute for the index
        htmlContent += `<div class="chunk" style="text-align: left;"><span class="chunk_text" style="background-color: ${color};" data-index="${index}">${data.text}</span></div>`;
    });

    htmlContent += '</div>';
    container.innerHTML = htmlContent;

    // Create a single tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip hidden';
    document.body.appendChild(tooltip);

    // Add event listeners for each token
    container.querySelectorAll('.chunk_text').forEach(token => {
    token.addEventListener('mouseenter', (e) => {
        const index = token.getAttribute('data-index');
        const tip = tips[index];
        // Format the tooltip content with Probability value
        tooltip.innerHTML = `Probability: ${tip * 100} %`;

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
    const ensembleSwitch = document.getElementById('llm_detailed_result_switch');
    const ensembleResults = document.querySelector('.ensemble_detector');
    ensembleResults.style.display = 'flex';
});


$(document).ready(function() {
    // Show the text tab by default
    $("#text-tab").tab("show");
  
    // File tab click event
    $("#file-tab").click(function(e) {
      e.preventDefault();
      $(this).tab("show");
    });

    // File tab click event
    $("#text-tab").click(function(e) {
        e.preventDefault();
        $(this).tab("show");
      });
  });