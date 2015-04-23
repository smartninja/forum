/*
* Author: Saran Chamling
* Source: http://www.sanwebe.com/2013/03/addremove-input-fields-dynamically-with-jquery
* Modified by: Matej Ramuta, Ziga Besal
*/

$(document).ready(function() {
    var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $(".input-fields-wrap"); //Fields wrapper
    var add_button      = $("#add-tag"); //Add button ID
    var addCourseButton      = $("#submit-topic"); //Add button ID

    var x = 1; //initial text box count

    $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
        if(x < max_fields){ //max input box allowed
            x++; //text box increment
            $(wrapper).append('<div id="addedTags">' +
                '<input type="text" name="tags" placeholder="Add a tag" class="myTag"/> ' +
                '<a href="#" class="remove_field btn btn-danger">Remove</a>' +
                '</div><br>'); //add input box
        }
    });

    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parent('div').remove(); x--;
    });

    addCourseButton.click(function() {
        var tagsList = [];

        $.each($(".myTag"), function() {
            var tag_value = $(this).val();
            if (tag_value === "") {
                alert("Please fill all the tag fields.");
                tagsList.push("none");
            } else {
                tagsList.push(tag_value);
            }
        });

        var allData = "";

        for (var i = 0; i < tagsList.length; i++) {
            allData += tagsList[i] + ",";
        }

        allData = allData.substring(0, allData.length - 1);

        $("#allData").val(allData);
    });
});