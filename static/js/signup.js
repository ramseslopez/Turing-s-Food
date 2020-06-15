const $emailInput = document.querySelector('#inputEmail');
const $passwordInput = document.querySelector('#inputPassword');
const $passwordConfirmationInput = document.querySelector(
  '#inputPasswordConfirmation'
);

function emailInvalidClassHandler() {
  if ($emailInput.classList.contains('is-invalid')) {
    $emailInput.classList.remove('is-invalid');
  }
}

function passwordInvalidClassHandler() {
  if ($passwordInput.classList.contains('is-invalid')) {
    $passwordInput.classList.remove('is-invalid');
    $passwordConfirmationInput.classList.remove('is-invalid');
  }
}

$emailInput.addEventListener('change', emailInvalidClassHandler);
$emailInput.addEventListener('keydown', emailInvalidClassHandler);
$emailInput.addEventListener('paste', emailInvalidClassHandler);
$emailInput.addEventListener('input', emailInvalidClassHandler);

$passwordInput.addEventListener('change', passwordInvalidClassHandler);
$passwordInput.addEventListener('keydown', passwordInvalidClassHandler);
$passwordInput.addEventListener('paste', passwordInvalidClassHandler);
$passwordInput.addEventListener('input', passwordInvalidClassHandler);
$passwordConfirmationInput.addEventListener(
  'change',
  passwordInvalidClassHandler
);
$passwordConfirmationInput.addEventListener(
  'keydown',
  passwordInvalidClassHandler
);
$passwordConfirmationInput.addEventListener(
  'paste',
  passwordInvalidClassHandler
);
$passwordConfirmationInput.addEventListener(
  'input',
  passwordInvalidClassHandler
);

function onSubmit() {
  document.querySelector('form').submit();
}
