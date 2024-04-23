// function addRow(course, lecturer){
//     var rowContent = `
//     <tr>
//         <td>${course}</td>
//         <td>${lecturer}</td>
//         <td><button>Submit</button></td>
//         <td> - </td>
//     </tr>`

//     $("#results-table").append(rowContent)
// }

// addRow('COMP 4211', 'Prof. A')
// addRow('COMP 3711', 'Prof. B')

$(document).ready(function() {
    $('.upload-file-btn').click(function() {
        console.log("Uploading")
        var submission_result = this.value.split(',');
        var file = $('#fileid_'+submission_result[0])[0].files[0]; // Get the selected file

        var formData = new FormData(); // Create a new FormData object
        formData.append('file', file); // Append the file to the FormData object
        formData.append('course', submission_result[0]); // Append the course name to the FormData object
        formData.append('id', submission_result[1]);

        $.ajax({
            type: 'POST',
            url: '/upload_file',
            data: formData, // Pass the FormData object as the data
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                location.reload();
            },
        });
    });
});