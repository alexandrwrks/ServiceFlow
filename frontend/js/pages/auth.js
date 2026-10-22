const loginTab = document.getElementById("login-tab");
const registerTab = document.getElementById("register-tab");

const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");


loginTab.addEventListener("click", () => {

    loginForm.classList.remove("hidden");
    registerForm.classList.add("hidden");

    loginForm.classList.remove("active");
    registerTab.classList.add("active");
});


registerTab.addEventListener("click", () => {

    registerForm.classList.remove("hidden");
    loginForm.classList.add("hidden");

    registerTab.classList.add("active");
    loginTab.classList.remove("active");
});