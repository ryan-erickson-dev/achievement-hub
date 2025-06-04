function submitUsername(event: Event) {
    event.preventDefault();
    const user = <HTMLInputElement>document.getElementById("usernameInput");

    /* NOTE: We need two then() calls here because both fetch() and
       json() are asynchronous operations. fetch() obviously obtains data
       from the server gradually via HTTP, thus returning a promise to a 
       response, and json() gets us a promise to the body of the response, 
       which may or may not have arrived already.
    */
   // Might want to check status or return type to see if JSON?
    fetch("/api/playerachievements", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
           username: user.value
        })
    })
    .then(response => response.json()) 
    .then(body => alert(body));
}