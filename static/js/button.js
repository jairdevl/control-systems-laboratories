document.addEventListener("DOMContentLoaded", function() {
    const togglePassword = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");

    togglePassword.addEventListener("click", function() {
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);
        this.textContent = type === "password" ? "👀" : "🙈"; // Cambiar el ícono
    });

    const toggleConfirmation = document.getElementById("toggleConfirmation");
    const confirmationInput = document.getElementById("confirmation");

    toggleConfirmation.addEventListener("click", function() {
        const type = confirmationInput.getAttribute("type") === "password" ? "text" : "password";
        confirmationInput.setAttribute("type", type);
        this.textContent = type === "password" ? "👀" : "🙈"; // Cambiar el ícono
    });
});

/*const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');
const eyeIcon = document.getElementById('eyeIcon');

togglePassword.addEventListener('click', function () {
    // Cambia el tipo de input entre 'password' y 'text'
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
});*/