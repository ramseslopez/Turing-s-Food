const $emailInput = document.querySelector('#inputEmail')
const $passwordInput = document.querySelector('#inputPassword')

function invalidClassHandler() {
  if ($emailInput.classList.contains('is-invalid')) {
    $emailInput.classList.remove('is-invalid')
  }
  if ($passwordInput.classList.contains('is-invalid')) {
    $passwordInput.classList.remove('is-invalid')
  }
}

$emailInput.addEventListener('change', invalidClassHandler)
$emailInput.addEventListener('keydown', invalidClassHandler)
$emailInput.addEventListener('paste', invalidClassHandler)
$emailInput.addEventListener('input', invalidClassHandler)
$passwordInput.addEventListener('change', invalidClassHandler)
$passwordInput.addEventListener('keydown', invalidClassHandler)
$passwordInput.addEventListener('paste', invalidClassHandler)
$passwordInput.addEventListener('input', invalidClassHandler)
