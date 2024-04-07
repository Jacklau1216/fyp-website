$(document).ready(function() {
    $("#detect-button").click(function() {
        var text = $("#text-input").val();
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