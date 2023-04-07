function AddWord(s) {
    var inputs = document.getElementsByClassName('InputsMathematics');
    var lastInput = inputs[inputs.length - 1];

    var newDiv = document.createElement('div');
    newDiv.className = "InputsMathematics";
    var newInput = document.createElement('input');
    newInput.type = "text";
    newInput.className = "InputMathematics";
    newInput.placeholder = "Введите фразу";
    var newButton = document.createElement('button');
    newButton.type = "submit";
    newButton.className = "trash";
    newButton.setAttribute("onclick", "bts(this)");
    var newImg = document.createElement('img');
    newImg.className = "svg";
    newImg.src = '/static/img/trash.svg';
    newButton.appendChild(newImg);
    newDiv.appendChild(newButton);
    newDiv.appendChild(newInput);
    $(newDiv).hide().insertBefore(lastInput.nextSibling).fadeIn(400);
    newDiv = document.createElement('div');
    newDiv.className = "sign_center";
    newInput = document.createElement('a');
    newInput.className = "signs";
    newInput.innerHTML = s
    newInput.setAttribute("onclick", "reverse(this)");
    newDiv.appendChild(newInput);
    $(newDiv).hide().insertBefore(lastInput.nextSibling).fadeIn(400);
}

function reverse(s){
    if($(s).text() == "+"){
        $(s).text("-");
    }
    else{
        $(s).text("+");
    }
}

function reload(){
    var el = document.getElementsByClassName("InputMathematics")[0];
    el.value = "";
}

function bts(s){
    var node = s.parentNode;
    var prev_node = node.previousSibling;
    $(node).fadeOut(400, function(){ $(node).remove(); });
    $(prev_node).fadeOut(400, function(){ $(prev_node).remove(); });
}

function getJson(){
    var inp = document.getElementsByClassName('InputMathematics');
    var s = [];
    var error = inp.length == 1;
    for(let i = 0; i < inp.length; i++){
        error = (error || inp[i].value == "");
        s.push(inp[i].value);
    }

    var sign = document.getElementsByClassName('signs');
    var si = [];
    for(let i = 0; i < sign.length; i++){
        si.push(sign[i].text);
    }

    var data = JSON.stringify({"labels": s, "signs": si});
    return [error, data];
}

$(document).ready(function () {
    $(".DeleteWord").click(function () {
        const [error, data] = getJson();
        if (!error) {
            $.ajax({
                url: '/math/getAns',
                type: 'post',
                data: data,
                contentType: "application/json; charset=utf-8",
                success: function (response) { 
                    $("#MathematicsAnswer").text(response["ans"]);
                 },
                error: function (jqXHR, exception) { alert('Error ' + jqXHR.responseText) },
            })
        }
    })
});