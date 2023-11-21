var popUp = document.getElementById("pop-up");
var inputPassword = document.getElementById("password-input");
var password = document.getElementById("password");

var handleCheckPass = function() {
    popUp.classList.remove("hidden");
}

var handleQuit = function() {
    inputPassword.value = '';
    popUp.classList.add("hidden");
}

var handleFocus = function() {
    inputPassword.placeholder = "";
}

var handleSubmit = function() {
    if (inputPassword.value === "123456") {
        window.location.href ="http://127.0.0.1:5000/add";
    } else {
        inputPassword.value = '';
        inputPassword.placeholder = "Sai mật khẩu";
    }
}