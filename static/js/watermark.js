$(".watermark-result").on("keydown", function (e) {
  var ctrl = e.ctrlKey ? e.ctrlKey : e.keyCode === 17 ? true : false;
  if (
    (e.keyCode === 86 && ctrl) ||
    (e.keyCode === 67 && ctrl) ||
    (e.keyCode === 88 && ctrl)
  ) {
    return true;
  } else {
    return false;
  }
});


$(document).ready(function () {
  $("#generate-button").click(function () {
    var text = $("#text-input").val();
    document.getElementById('generate-button').innerHTML = `<div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>`
    $.ajax({
      url: "/generate",
      type: "POST",
      data: { text: text },
      success: function (response) {
        $("#text-output").val(response);
        document.getElementById('generate-button').innerHTML = `Generate Watermark`
      },
      error: function (xhr, status, error) {
        console.log(error);
      },
    });
  });
});
