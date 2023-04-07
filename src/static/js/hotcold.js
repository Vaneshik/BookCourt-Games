$(document).ready(function () {
    $("#sendBtn").click(function () {
        var text = $("#inp").val().trim();

        if (inp != "") {
            $.ajax({
                url: '/hotcold/getAns',
                type: 'post',
                data: JSON.stringify({ text: text }),
                contentType: "application/json; charset=utf-8",
                success: function (response) { $("#inp").val(''); console.log(response); },
                error: function (jqXHR, exception) { alert('Error ' + jqXHR.responseText) },
            })
        }
    })
});

document.getElementById('inp').addEventListener('keypress', function(event) {
    if (event.keyCode == 13) {
        document.getElementById('sendBtn').click();
    }
});