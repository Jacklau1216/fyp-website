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
      
    });
    $("#detect-button").click(function() {
        var text = $("#text-input").val();
        $.ajax({
            url: "/detect",
            type: "POST",
            data: { text: text },
            success: function(response) {
               
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
    // Update the label text when a file is selected
    $("#file-input").change(function() {
        var fileName = $(this).val().split('\\').pop();
        $(".custom-file-label").text(fileName);
    });
    $("#upload-button").click(function() {
        var fileInput = document.getElementById("file-input");
        var file = fileInput.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var content = e.target.result;
                $.ajax({
                    url: "/upload",
                    type: "POST",
                    data: { content: content },
                    success: function(response) {
                        console.log("File uploaded successfully!");
                        $(".custom-file-label").text("Choose file");

                        $(".flash-message").html('<div class="alert alert-success alert-dismissible fade show" role="alert">File uploaded successfully!</div>');
                    },
                    error: function(xhr, status, error) {
                        console.log(error);
                    }
                });
            };
            reader.readAsBuffer(file);
        }
    });
});
