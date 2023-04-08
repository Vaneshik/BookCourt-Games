function addItem(response){
    var stab = $("#game")[0];
    var llc = stab.children[stab.children.length - 1];
    console.log(response);
    if(response[1] == -1){
        console.log('gg');
    }
    else{
        var newDiv = document.createElement('div');
        // newDiv.className = "words";
        newDiv.classList.add("words");
        newDiv.classList.add("item");
        newDiv.setAttribute("style", "order: " + response[1]);
        var newInpBook = document.createElement('a');
        newInpBook.setAttribute("width", 30);
        newInpBook.className = "InputBook";
        newInpBook.innerHTML = response[0];
        var newInpScore = document.createElement('a');
        newInpScore.className = "InputBookToo";
        newInpScore.innerHTML = response[1];
        var newDivChild = document.createElement('div');
        newDivChild.className = "pie";
        if(response[2] * 100 < 33){
            newDivChild.setAttribute("style", "--p:" +(response[2] * 100) + ";--c:#e74c3c;;");
        }
        else if(response[2] * 100 < 66){
            newDivChild.setAttribute("style", "--p:" +(response[2] * 100) + ";--c:#f1c40f;");
        }
        else{
            newDivChild.setAttribute("style", "--p:" +(response[2] * 100) + ";--c:#07bc0c;");
        }
        newDiv.appendChild(newInpBook);
        newDiv.appendChild(newInpScore);
        newDiv.appendChild(newDivChild);
        $(newDiv).hide().insertBefore(llc.nextSibling).fadeIn(400);
        if(response[1] == 1){
            setTimeout(() => { alert("Победа!!!"); }, 500);
        }
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
 