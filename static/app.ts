function submitUsername(event: Event) {
    event.preventDefault();
    const user = <HTMLInputElement>document.getElementById("usernameInput");
    console.log(user.value);
}