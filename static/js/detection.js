$(document).ready(function() {
    $("#detect-button").click(function() {
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
        // $.ajax({
        //     url: "/detect",
        //     type: "POST",
        //     data: { text: text },
        //     success: function(response) {
        //         $("#result").text("LLM Detection Result: " + response);
        //     },
        //     error: function(xhr, status, error) {
        //         console.log(error);
        //     }
        // });
    });
});


