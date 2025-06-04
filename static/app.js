"use strict";
function submitUsername(event) {
    event.preventDefault();
    const user = document.getElementById("usernameInput");
    console.log(user.value);
}
