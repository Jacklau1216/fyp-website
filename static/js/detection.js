// $(document).ready(function() {
//     $("#detect-button").click(function() {
//         var text = $("#text-input").val();
//          $.ajax({
//             url: "/GLTR_detect",
//             type: "POST",
//             data: { text: text },
//             success: function(response) {
//                 console.log("GLTR_detect");
//                 drawTopK("topKCount",Object.keys(response.topk),Object.values(response.topk),"topKCount",0);
//                 drawTopK("fracPHistogram",Object.keys(response.fracp),Object.values(response.fracp),"Frac(p)",1);
//                 drawTopK("top10Entropy",Object.keys(response.top10Entropy),Object.values(response.top10Entropy),"Top 10 Entropy",2);
// //                console.log(response.pop_up_display)
//                 drawColorTextBox(response.topk_display,response.countArray,response.pop_up_display);
//             },
//             error: function(xhr, status, error) {
//                 console.log(error);
//             }
//         });
      
//     });
//     // Update the label text when a file is selected
//     $("#file-input").change(function() {
//         var fileName = $(this).val().split('\\').pop();
//         $(".custom-file-label").text(fileName);
//     });
//     $("#upload-button").click(function() {
//         var fileInput = document.getElementById("file-input");
//         var file = fileInput.files[0];
//         if (file) {
//             var reader = new FileReader();
//             reader.onload = function(e) {
//                 var content = e.target.result;
//                 $.ajax({
//                     url: "/upload",
//                     type: "POST",
//                     data: { content: content },
//                     success: function(response) {
//                         console.log("File uploaded successfully!");
//                         $(".custom-file-label").text("Choose file");

//                         $(".flash-message").html('<div class="alert alert-success alert-dismissible fade show" role="alert">File uploaded successfully!</div>');
//                     },
//                     error: function(xhr, status, error) {
//                         console.log(error);
//                     }
//                 });
//             };
//             reader.readAsBuffer(file);
//         }
//     });
// });
$(document).ready(function() {
    var textInput = $("#text-input");
    var fileInput = $("#file-input");

    // 檢測按鈕點擊事件
    $("#detect-button").click(function() {
        if (textInput.val() !== "") {
            // 在文本輸入框有輸入時禁用檔案選擇框
            fileInput.prop("disabled", true);
            detectFunction(textInput.val());
        } else if (fileInput.val() !== "") {
            // 在檔案選擇框有選擇檔案時禁用文本輸入框
            textInput.prop("disabled", true);
            var file = fileInput[0].files[0];
            detectFileFunction(file);
        } else {
            // 如果兩個都沒有輸入，進行相應的錯誤處理
            console.log("No input provided.");
        }
    });

    // 檔案選擇框變化事件
    fileInput.change(function() {
        if (fileInput.val() !== "") {
            // 在檔案選擇框有選擇檔案時禁用文本輸入框
            textInput.prop("disabled", true);
        } else {
            // 如果檔案選擇框被清空，啟用文本輸入框
            textInput.prop("disabled", false);
        }
    });

    // 檢測功能 - 文本
    function detectFunction(text) {
        $.ajax({
            url: "/GLTR_detect",
            type: "POST",
            data: { text: text },
            success: function(response) {
                // 處理檢測結果
                console.log("GLTR_detect");
                drawTopK("topKCount", Object.keys(response.topk), Object.values(response.topk), "topKCount", 0);
                drawTopK("fracPHistogram", Object.keys(response.fracp), Object.values(response.fracp), "Frac(p)", 1);
                drawTopK("top10Entropy", Object.keys(response.top10Entropy), Object.values(response.top10Entropy), "Top 10 Entropy", 2);
                drawColorTextBox(response.topk_display, response.countArray, response.pop_up_display);
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    }

    // 檢測功能 - 檔案
    function detectFileFunction(file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var content = e.target.result;
            $.ajax({
                url: "/GLTR_detect",
                type: "POST",
                data: { fileContent: content },
                success: function(response) {
                    // 處理檢測結果
                    console.log("GLTR_detect");
                    drawTopK("topKCount", Object.keys(response.topk), Object.values(response.topk), "topKCount", 0);
                    drawTopK("fracPHistogram", Object.keys(response.fracp), Object.values(response.fracp), "Frac(p)", 1);
                    drawTopK("top10Entropy", Object.keys(response.top10Entropy), Object.values(response.top10Entropy), "Top 10 Entropy", 2);
                    drawColorTextBox(response.topk_display, response.countArray, response.pop_up_display);
                },
                error: function(xhr, status, error) {
                    console.log(error);
                }
            });
        };
        reader.readAsText(file);
    }
});