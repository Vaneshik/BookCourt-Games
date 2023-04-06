$(document).ready(function () {
    $("#TrueReg").click(function () {
        var email = $("#email").val().trim();
        var password = $("#password").val().trim();

        if (email != "" && password != "") {
            $.ajax({
                url: '/auth/login',
                type: 'post',
                data: { username: email, password: password },
                success: function (response) { window.location.replace("/"); },
                error: function (jqXHR, exception) { alert('Error ' + jqXHR.responseText) },
            })
        }
    })
});