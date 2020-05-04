const $logoInput = document.querySelector('#logo')
const $logoLabel = document.querySelector('#file-label')


$logoInput.addEventListener('change', e => {
  $logoLabel.textContent = e.target.files[0].name
})