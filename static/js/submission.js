function addRow(course, lecturer){
    var rowContent = `
    <tr>
        <td>${course}</td>
        <td>${lecturer}</td>
        <td><button>Submit</button></td>
        <td> - </td>
    </tr>`

    $("#results-table").append(rowContent)
}

addRow('COMP 4211', 'Prof. A')
addRow('COMP 3711', 'Prof. B')