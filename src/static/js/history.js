$(document).ready(function () {
    $("#sendBtn").click(function () {
        var text = $("#inp").val().trim();

        if (inp != "") {
            $.ajax({
                url: '/history/getAns',
                type: 'post',
                data: JSON.stringify({ text: text }),
                contentType: "application/json; charset=utf-8",
                success: function (response) { console.log(response); $("#HistAnswer").text(response["ans"]); },
                error: function (jqXHR, exception) { alert('Error ' + jqXHR.responseText) },
            })
        }
    })
});