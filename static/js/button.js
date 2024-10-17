const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

togglePassword.addEventListener('click', function () {
  const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
  passwordInput.setAttribute('type', type);
});

const toggleConfirmation = document.getElementById('toggleConfirmation');
const confirmationInput = document.getElementById('confirmation');

toggleConfirmation.addEventListener('click', function () {
  const type = confirmationInput.getAttribute('type') === 'password' ? 'text' : 'password';
  confirmationInput.setAttribute('type', type);
});