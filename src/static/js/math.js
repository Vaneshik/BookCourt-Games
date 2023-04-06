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
    newImg.src = '/static/img/trash.svg';
    newButton.appendChild(newImg);
    newDiv.appendChild(newButton);
    newDiv.appendChild(newInput);
    lastInput.parentNode.insertBefore(newDiv, lastInput.nextSibling);

    newDiv = document.createElement('div');
    newDiv.className = "sign_center";
    newInput = document.createElement('a');
    newInput.className = "signs";
    newInput.innerHTML = s
    newDiv.appendChild(newInput);
    lastInput.parentNode.insertBefore(newDiv, lastInput.nextSibling);
}

function bts(s){
    var node = s.parentNode;
    var prev_node = node.previousSibling;
    $(node).fadeOut(300, function(){ $(node).remove(); });
    $(prev_node).fadeOut(300, function(){ $(prev_node).remove(); });
}

function getJson(){
    var inp = document.getElementsByClassName('InputMathematics');
    var s = [];
    for(let i = 0; i < inp.length; i++){
        s.push(inp[i].value);
    }
    
    var sign = document.getElementsByClassName('signs');
    var si = [];
    for(let i = 0; i < sign.length; i++){
        si.push(sign[i].text);
    }

    var data = JSON.stringify({"labels": s, "signs": si});
    return data;
}