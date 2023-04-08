function addItem(response){
    var stab = $("#game")[0];
    console.log(stab);
    if(response[1] == -1){
        console.log('gg');
    }
    else if(response[1] == 1){
        alert('Ура победа!!!');
    }
    else{
        var llc = stab.lastChild;
        var newDiv = document.createElement('button');
    }
}

$(document).ready(function () {
    $("#sendBtn").click(function () {
        var text = $("#tags").val().trim();
        console.log(text);
        if (text != "") {
            $.ajax({
                url: '/hotcold/getAns',
                type: 'post',
                data: JSON.stringify({ text: text }),
                contentType: "application/json; charset=utf-8",
                success: function (response) { $("#tags").val(''); console.log(response.score); addItem(response.score) },
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
              maxShowItems: 6,
              minLength: 4
   });
 });
 