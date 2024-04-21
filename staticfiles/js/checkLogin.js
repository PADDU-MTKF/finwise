

// To retrieve the saved data later:
let savedUsername = localStorage.getItem("username");
let savedPassword = localStorage.getItem("password");

if (savedUsername && savedPassword) {
    // Fill the form fields with the saved username and password
    document.querySelector('input[name="username"]').value = savedUsername;
    document.querySelector('input[name="password"]').value = savedPassword;

    // Submit the form
    document.querySelector('form').submit();
}
else{
    document.querySelector('.hide').classList.remove('hide');
}

