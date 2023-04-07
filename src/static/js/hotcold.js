$(document).ready(function () {
    $("#sendBtn").click(function () {
        var text = $("#tags").val().trim();

        if (text != "") {
            $.ajax({
                url: '/hotcold/getAns',
                type: 'post',
                data: JSON.stringify({ text: text }),
                contentType: "application/json; charset=utf-8",
                success: function (response) { $("#tags").val(''); console.log(response); },
                error: function (jqXHR, exception) { alert('Error ' + jqXHR.responseText) },
            })
        }
    })
});

document.getElementById('tags').addEventListener('keypress', function(event) {
    if (event.keyCode == 13) {
        document.getElementById('sendBtn').click();
    }
});

$(function() {
    $('#tags').autocomplete({
              source: function (request, response){
                $.ajax({
                    url: '/hotcold/getQue',
                    type: 'post',
                    data: JSON.stringify({ "pref": request.term }),
                    contentType: "application/json; charset=utf-8",
                    success: response
                })
              },
              maxShowItems: 5,
              minLength: 4
   });
 });
 